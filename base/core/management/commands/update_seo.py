"""
Django Management Command: update_seo
======================================
icerik.json dosyasından SEO başlık ve açıklamalarını günceller.
"""

import json
from django.core.management.base import BaseCommand
from service.models import Service, ServiceArea, ServiceCategory
from core.models import Project


class Command(BaseCommand):
    help = 'icerik.json dosyasından SEO verilerini günceller'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='../icerik.json',
            help='JSON dosyasının yolu (varsayılan: ../icerik.json)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Değişiklikleri kaydetmeden sadece göster'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.SUCCESS('''
============================================================
  EB DEKORASYON - SEO VERİSİ GÜNCELLEME
============================================================
'''))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Dosya bulunamadı: {file_path}'))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'JSON parse hatası: {e}'))
            return
        
        updated_count = 0
        not_found_count = 0
        
        # 1. Hizmetleri güncelle
        self.stdout.write('\n📦 Hizmetler güncelleniyor...')
        for item in data.get('services', []):
            slug = item.get('slug')
            try:
                obj = Service.objects.get(slug=slug)
                obj.seo_title = item.get('seo_title', obj.seo_title)
                obj.seo_description = item.get('seo_description', obj.seo_description)
                if not dry_run:
                    obj.save()
                self.stdout.write(f'  ✓ {slug}')
                updated_count += 1
            except Service.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ✗ Bulunamadı: {slug}'))
                not_found_count += 1
        
        # 2. Hizmet Bölgelerini güncelle
        self.stdout.write('\n📍 Hizmet Bölgeleri güncelleniyor...')
        for item in data.get('service_areas', []):
            slug = item.get('slug')
            try:
                obj = ServiceArea.objects.get(slug=slug)
                obj.seo_title = item.get('seo_title', obj.seo_title)
                obj.seo_description = item.get('seo_description', obj.seo_description)
                if not dry_run:
                    obj.save()
                self.stdout.write(f'  ✓ {slug}')
                updated_count += 1
            except ServiceArea.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ✗ Bulunamadı: {slug}'))
                not_found_count += 1
        
        # 3. Projeleri güncelle
        self.stdout.write('\n🏗️ Projeler güncelleniyor...')
        for item in data.get('projects', []):
            slug = item.get('slug')
            try:
                obj = Project.objects.get(slug=slug)
                obj.seo_title = item.get('seo_title', obj.seo_title)
                obj.seo_description = item.get('seo_description', obj.seo_description)
                if not dry_run:
                    obj.save()
                self.stdout.write(f'  ✓ {slug}')
                updated_count += 1
            except Project.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ✗ Bulunamadı: {slug}'))
                not_found_count += 1
        
        # 4. Kategorileri güncelle
        self.stdout.write('\n📂 Kategoriler güncelleniyor...')
        for item in data.get('categories', []):
            slug = item.get('slug')
            try:
                obj = ServiceCategory.objects.get(slug=slug)
                # ServiceCategory'de seo alanları yok, atla
                self.stdout.write(f'  ⊘ {slug} (SEO alanı yok)')
            except ServiceCategory.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ✗ Bulunamadı: {slug}'))
                not_found_count += 1
        
        # Özet
        mode = '(DRY RUN - kaydedilmedi)' if dry_run else ''
        self.stdout.write(self.style.SUCCESS(f'''
============================================================
  ÖZET {mode}
============================================================
  ✓ Güncellenen: {updated_count}
  ✗ Bulunamayan: {not_found_count}
============================================================
'''))
