"""
Django Management Command: import_service_content
==================================================
hizmet-icerik/ klasöründeki JSON dosyalarından hizmet içeriklerini
veritabanına aktarır. SEO alanlarına (seo_title, seo_description) dokunmaz.
"""

import json
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from service.models import Service, ServiceStep
from core.models import Feature, Faq


class Command(BaseCommand):
    help = 'JSON dosyalarından hizmet içeriklerini içe aktarır (SEO alanları korunur)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Değişiklikleri kaydetmeden simülasyon yapar'
        )
        parser.add_argument(
            '--slug',
            type=str,
            help='Sadece belirtilen slug için işlem yapar'
        )

    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.target_slug = options.get('slug')
        
        # JSON dosyalarının bulunduğu klasör
        base_dir = Path(settings.BASE_DIR).parent
        json_dir = base_dir / 'hizmet-icerik'
        
        if not json_dir.exists():
            self.stderr.write(self.style.ERROR(f'❌ Klasör bulunamadı: {json_dir}'))
            return

        self.stdout.write(self.style.WARNING('\n' + '=' * 60))
        self.stdout.write(self.style.WARNING('  HİZMET İÇERİK AKTARIMI'))
        if self.dry_run:
            self.stdout.write(self.style.WARNING('  🔍 DRY-RUN MODU (değişiklik yapılmayacak)'))
        self.stdout.write(self.style.WARNING('=' * 60 + '\n'))

        stats = {
            'processed': 0,
            'updated': 0,
            'skipped': 0,
            'not_found': 0,
            'errors': 0,
            'features': 0,
            'steps': 0,
            'faqs': 0
        }

        # JSON dosyalarını işle
        json_files = list(json_dir.glob('*.json'))
        self.stdout.write(f'📁 {len(json_files)} JSON dosyası bulundu\n')

        for json_file in sorted(json_files):
            slug = json_file.stem  # Dosya adından .json uzantısını kaldır
            
            # Belirli bir slug hedefleniyorsa, diğerlerini atla
            if self.target_slug and slug != self.target_slug:
                continue
                
            stats['processed'] += 1
            result = self.process_json_file(json_file, slug)
            
            if result == 'updated':
                stats['updated'] += 1
            elif result == 'skipped':
                stats['skipped'] += 1
            elif result == 'not_found':
                stats['not_found'] += 1
            elif result == 'error':
                stats['errors'] += 1
            
            if isinstance(result, dict):
                stats['updated'] += 1
                stats['features'] += result.get('features', 0)
                stats['steps'] += result.get('steps', 0)
                stats['faqs'] += result.get('faqs', 0)

        self.print_summary(stats)

    def process_json_file(self, json_file: Path, slug: str) -> str | dict:
        """Tek bir JSON dosyasını işler."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    self.stdout.write(self.style.WARNING(f'  ⚠️  {slug}: Boş dosya, atlanıyor'))
                    return 'skipped'
                data = json.loads(content)
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f'  ❌ {slug}: JSON parse hatası - {e}'))
            return 'error'
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'  ❌ {slug}: Dosya okuma hatası - {e}'))
            return 'error'

        # JSON yapısını çöz
        fields = data.get('fields', data)
        json_slug = fields.get('slug', slug)

        # Veritabanında Service'i bul
        try:
            service = Service.objects.get(slug=json_slug)
        except Service.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'  ❌ {json_slug}: Veritabanında bulunamadı'))
            return 'not_found'

        if self.dry_run:
            self.stdout.write(self.style.SUCCESS(f'  ✓ {json_slug}: Güncellenecek (dry-run)'))
            return 'updated'

        # İçerikleri güncelle (SEO alanları HARİÇ)
        updated_fields = []
        
        # description_html -> description
        if 'description_html' in fields:
            service.description = fields['description_html']
            updated_fields.append('description')
        
        # short_description
        if 'short_description' in fields:
            service.short_description = fields['short_description']
            updated_fields.append('short_description')
        
        # icon
        if 'icon' in fields:
            service.icon = fields['icon']
            updated_fields.append('icon')
        
        # is_active -> isActive
        if 'is_active' in fields:
            service.isActive = fields['is_active']
            updated_fields.append('isActive')
        
        # show_index -> showIndex  
        if 'show_index' in fields:
            service.showIndex = fields['show_index']
            updated_fields.append('showIndex')

        service.save()

        # İlişkili verileri işle
        result = {'features': 0, 'steps': 0, 'faqs': 0}
        
        related_data = fields.get('related_data', {})
        
        # Features
        if 'features_to_tag' in related_data:
            result['features'] = self.update_features(service, related_data['features_to_tag'])
        
        # Steps
        if 'steps' in related_data:
            result['steps'] = self.update_steps(service, related_data['steps'])
        
        # FAQs
        if 'faqs' in related_data:
            result['faqs'] = self.update_faqs(service, related_data['faqs'])

        self.stdout.write(self.style.SUCCESS(
            f'  ✓ {json_slug}: Güncellendi '
            f'({len(updated_fields)} alan, '
            f'{result["features"]} özellik, '
            f'{result["steps"]} adım, '
            f'{result["faqs"]} SSS)'
        ))
        
        return result

    def update_features(self, service: Service, features_list: list) -> int:
        """Hizmetin özelliklerini günceller."""
        service.features.clear()
        count = 0
        for feature_name in features_list:
            feature, _ = Feature.objects.get_or_create(
                name=feature_name,
                defaults={'description': f'{feature_name} özelliği.'}
            )
            service.features.add(feature)
            count += 1
        return count

    def update_steps(self, service: Service, steps_list: list) -> int:
        """Hizmetin süreç adımlarını günceller."""
        ServiceStep.objects.filter(service=service).delete()
        count = 0
        for step_data in steps_list:
            ServiceStep.objects.create(
                service=service,
                step_number=step_data.get('step_number', count + 1),
                title=step_data['title'],
                description=step_data['description']
            )
            count += 1
        return count

    def update_faqs(self, service: Service, faqs_list: list) -> int:
        """Hizmetin SSS'lerini günceller."""
        service.faqs.clear()
        count = 0
        for faq_data in faqs_list:
            faq, _ = Faq.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'isActive': True,
                    'showIndex': False
                }
            )
            service.faqs.add(faq)
            count += 1
        return count

    def print_summary(self, stats: dict):
        """İşlem özetini yazdırır."""
        self.stdout.write('\n' + '-' * 60)
        if self.dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY-RUN TAMAMLANDI (değişiklik yapılmadı)'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ İÇE AKTARIM TAMAMLANDI'))
        
        self.stdout.write(f'   • İşlenen dosya: {stats["processed"]}')
        self.stdout.write(f'   • Güncellenen: {stats["updated"]}')
        self.stdout.write(f'   • Atlanan (boş): {stats["skipped"]}')
        self.stdout.write(f'   • Bulunamayan: {stats["not_found"]}')
        self.stdout.write(f'   • Hata: {stats["errors"]}')
        self.stdout.write(f'   • Özellik: {stats["features"]}')
        self.stdout.write(f'   • Adım: {stats["steps"]}')
        self.stdout.write(f'   • SSS: {stats["faqs"]}')
        self.stdout.write('=' * 60 + '\n')
