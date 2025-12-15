from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from core.models import Hero, Settings, Counter, Feature
from service.models import Service, ServiceCategory
from core.models import Project
import requests
import os

class Command(BaseCommand):
    help = 'Populates the database with data from index.html'

    def handle(self, *args, **options):
        self.stdout.write('Starting data population...')
        
        # 1. Settings
        self.stdout.write('Creating Settings...')
        settings, _ = Settings.objects.get_or_create(id=1)
        settings.phone = "+905551234567"
        settings.whatsapp = "+905551234567"
        settings.save()

        # 2. Hero
        self.stdout.write('Creating Hero...')
        hero, _ = Hero.objects.get_or_create(id=1)
        hero.title = 'Mekanlarınıza Altın Dokunuş'
        hero.description = 'Mobilya boyama, tadilat ve iç mimarlık hizmetlerinde 10 yılı aşkın tecrübe. Yeni almaktan %70 daha uygun!'
        hero.primary_button_text = 'Ücretsiz Teklif Al'
        hero.primary_button_link = 'tel:+905551234567'
        hero.save()
        
        # Download Hero Image
        self._download_and_save_image(hero.banner, 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1920&q=80', 'hero_bg.jpg')
        hero.save()

        # 3. Features (Trust Badges)
        features_data = [
            {'name': '2 Yıl Garanti', 'icon': 'fas fa-shield-alt'},
            {'name': 'Ücretsiz Keşif', 'icon': 'fas fa-search'},
            {'name': '12 Ay Taksit', 'icon': 'fas fa-credit-card'},
        ]
        for f_data in features_data:
            Feature.objects.get_or_create(name=f_data['name'], defaults={'icon': f_data['icon']})

        # 4. Counters
        counters_data = [
            {'name': 'Mutlu Müşteri', 'count': '500+', 'icon': 'fas fa-smile'},
            {'name': 'Yıl Tecrübe', 'count': '15+', 'icon': 'fas fa-clock'},
            {'name': 'Sigortalı Ekip', 'count': '%100', 'icon': 'fas fa-hard-hat'},
            {'name': 'Keşif & Teklif', 'count': 'Ücretsiz', 'icon': 'fas fa-check'},
        ]
        for c_data in counters_data:
            Counter.objects.get_or_create(name=c_data['name'], defaults={'count': c_data['count'], 'icon': c_data['icon']})

        # 5. Service Categories
        categories = {
            'mobilya': ServiceCategory.objects.get_or_create(name='Mobilya', slug='mobilya')[0],
            'tadilat': ServiceCategory.objects.get_or_create(name='Tadilat', slug='tadilat')[0],
            'boya': ServiceCategory.objects.get_or_create(name='Boya Badana', slug='boya')[0],
            'doseme': ServiceCategory.objects.get_or_create(name='Döşeme', slug='doseme')[0],
        }

        # 6. Services
        services_data = [
            {
                'title': 'Mobilya Boyama',
                'desc': 'Eski mobilyalarınızı yenilemek artık çok kolay.',
                'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=800',
                'category': categories['mobilya']
            },
            {
                'title': 'Mutfak Dolabı Boyama',
                'desc': 'Mutfağınızı yenilemek için dolap değiştirmeye gerek yok.',
                'image': 'https://images.unsplash.com/photo-1556909114-44e3e70034e2?auto=format&fit=crop&w=800',
                'category': categories['mobilya']
            },
            {
                'title': 'Anahtar Teslim Tadilat',
                'desc': 'A\'dan Z\'ye tüm tadilat işlerinizi tek elden yapıyoruz.',
                'image': 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800',
                'category': categories['tadilat']
            },
            {
                'title': 'İç Cephe Boya Badana',
                'desc': 'Premium boyalar ve uzman ekibimizle kusursuz sonuçlar.',
                'image': 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=800',
                'category': categories['boya']
            },
             {
                'title': 'Koltuk Döşeme',
                'desc': 'Eski koltuklarınızı yenisi gibi yapıyoruz.',
                'image': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=800',
                'category': categories['doseme']
            },
            {
                'title': 'Parke Döşeme',
                'desc': 'Laminat ve masif parke döşeme hizmetleri.',
                'image': 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=800',
                'category': categories['doseme']
            },
        ]

        for s_data in services_data:
            service, created = Service.objects.get_or_create(
                title=s_data['title'],
                defaults={
                    'short_description': s_data['desc'],
                    'slug': slugify(s_data['title']),
                    'category': s_data['category'],
                    'description': s_data['desc']
                }
            )
            if created or not service.image:
                self._download_and_save_image(service.image, s_data['image'], f"service_{slugify(s_data['title'])}.jpg")
                service.save()

        # 7. Projects
        projects_data = [
            {
                'title': 'Modern Mutfak Dönüşümü',
                'location': 'Kadıköy, İstanbul',
                'category': 'Mutfak Dolabı Boyama',
                'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600',
                'before': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&q=80',
                'after': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80'
            },
             {
                'title': 'Klasik Yatak Odası Yenileme',
                'location': 'Ataşehir, İstanbul',
                'category': 'Yatak Odası Mobilya',
                'image': 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=600',
                'before': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&q=80',
                'after': 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80'
            },
             {
                'title': 'Komple Ev Renovasyonu',
                'location': 'Beşiktaş, İstanbul',
                'category': 'Anahtar Teslim Tadilat',
                'image': 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=600',
                'before': None,
                'after': None,
                'is_featured': True
            },
             {
                'title': 'Lüks Banyo Dönüşümü',
                'location': 'Bakırköy, İstanbul',
                'category': 'Banyo Tadilat',
                'image': 'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=600',
                'before': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80',
                'after': 'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80'
            },
             {
                'title': 'Antika Koltuk Restorasyonu',
                'location': 'Şişli, İstanbul',
                'category': 'Koltuk Döşeme',
                'image': 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=600',
                'before': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80',
                'after': 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=800&q=80'
            },
             {
                'title': 'Ofis Boya Projesi',
                'location': 'Levent, İstanbul',
                'category': 'Boya Badana',
                'image': 'https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=600',
                'before': None,
                'after': None
            },
        ]

        for p_data in projects_data:
            project, created = Project.objects.get_or_create(
                title=p_data['title'],
                defaults={
                    'location': p_data['location'],
                    'category': p_data['category'], # String category for Project model
                    'slug': slugify(p_data['title']),
                    'description': f"{p_data['title']} projemiz.",
                    'is_featured': p_data.get('is_featured', False)
                }
            )
            
            if created or not project.image:
                self._download_and_save_image(project.image, p_data['image'], f"project_main_{slugify(p_data['title'])}.jpg")
                project.save()

            if p_data.get('before') and (created or not project.before_image):
                 self._download_and_save_image(project.before_image, p_data['before'], f"project_before_{slugify(p_data['title'])}.jpg")
            
            if p_data.get('after') and (created or not project.after_image):
                 self._download_and_save_image(project.after_image, p_data['after'], f"project_after_{slugify(p_data['title'])}.jpg")
            
            project.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))

    def _download_and_save_image(self, field, url, filename):
        if not url:
            return
        try:
            response = requests.get(url)
            if response.status_code == 200:
                field.save(filename, ContentFile(response.content), save=False)
                self.stdout.write(f"Downloaded {filename}")
            else:
                self.stdout.write(self.style.WARNING(f"Failed to download {filename}: Status {response.status_code}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error downloading {filename}: {e}"))
