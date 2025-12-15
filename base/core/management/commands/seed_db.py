import os
import urllib.request
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from core.models import Settings, Counter, Hero, Feature, Comment, Faq, Project
from service.models import Service, ServiceCategory


class Command(BaseCommand):
    help = 'EB Dekorasyon için örnek verileri yükler (eski verileri silerek)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-only',
            action='store_true',
            help='Sadece mevcut verileri sil, yeni veri ekleme',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n🗑️  Eski veriler siliniyor...\n'))
        self.clear_all_data()
        
        if options['clear_only']:
            self.stdout.write(self.style.SUCCESS('\n✅ Tüm veriler silindi!'))
            return
        
        self.stdout.write(self.style.WARNING('\n🚀 EB Dekorasyon verileri yükleniyor...\n'))
        
        # Create data in order
        self.create_settings()
        self.create_counters()
        self.create_features()
        self.create_hero()
        self.create_comments()
        self.create_faqs()
        self.create_categories()
        self.create_services()
        self.create_projects()
        
        self.stdout.write(self.style.SUCCESS('\n✅ Tüm veriler başarıyla yüklendi!'))
        self.stdout.write(self.style.SUCCESS('🌐 Site: http://127.0.0.1:8002/'))
        self.stdout.write(self.style.SUCCESS('👤 Admin: http://127.0.0.1:8002/admin/'))

    def clear_all_data(self):
        """Tüm seed verilerini sil"""
        Project.objects.all().delete()
        self.stdout.write('  ✓ Project silindi')
        
        Service.objects.all().delete()
        self.stdout.write('  ✓ Service silindi')
        
        ServiceCategory.objects.all().delete()
        self.stdout.write('  ✓ ServiceCategory silindi')
        
        Comment.objects.all().delete()
        self.stdout.write('  ✓ Comment silindi')
        
        Faq.objects.all().delete()
        self.stdout.write('  ✓ Faq silindi')
        
        Counter.objects.all().delete()
        self.stdout.write('  ✓ Counter silindi')
        
        Feature.objects.all().delete()
        self.stdout.write('  ✓ Feature silindi')
        
        Hero.objects.all().delete()
        self.stdout.write('  ✓ Hero silindi')

    def download_image(self, url, filename):
        """Unsplash'tan resim indir ve kaydet"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=10)
            image_data = response.read()
            return ContentFile(image_data, name=filename)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'    ⚠ Resim indirilemedi: {e}'))
            return None

    def create_settings(self):
        Settings.objects.update_or_create(
            pk=1,
            defaults={
                'name': 'EB Dekorasyon',
                'domain': 'ebdekorasyon.com',
                'phone': '+90 555 123 45 67',
                'whatsapp': '905551234567',
                'email': 'info@ebdekorasyon.com',
                'adress': 'İstanbul, Türkiye',
                'instagram': 'https://instagram.com/ebdekorasyon',
                'facebook': 'https://facebook.com/ebdekorasyon',
                'alternate_name': 'EB Dekorasyon Boya Tadilat',
                'city': 'İstanbul',
                'founding_date': '2014',
                'average_rating': '4.9',
                'review_count': '150',
                'seo_title': 'EB Dekorasyon | İstanbul Boya Tadilat & Mobilya Yenileme',
                'seo_description': 'İstanbul\'un en prestijli boya, tadilat ve mobilya yenileme hizmetleri.',
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ Settings oluşturuldu'))

    def create_counters(self):
        counters = [
            {'name': 'Tamamlanan Proje', 'count': '500+', 'icon': 'fas fa-check-circle'},
            {'name': 'Mutlu Müşteri', 'count': '450+', 'icon': 'fas fa-smile'},
            {'name': 'Yıllık Tecrübe', 'count': '10+', 'icon': 'fas fa-calendar'},
            {'name': 'Uzman Ekip', 'count': '15+', 'icon': 'fas fa-users'},
        ]
        for data in counters:
            Counter.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('✓ Sayaçlar oluşturuldu'))

    def create_features(self):
        features = [
            {'name': '2 Yıl Garanti', 'description': 'Tüm işlerimize 2 yıl işçilik garantisi.', 'icon': 'fas fa-shield-alt'},
            {'name': 'Ücretsiz Keşif', 'description': 'Yerinizden ücretsiz keşif ve fiyat teklifi.', 'icon': 'fas fa-search-location'},
            {'name': '12 Ay Taksit', 'description': 'Kredi kartına 12 aya varan taksit.', 'icon': 'fas fa-credit-card'},
            {'name': 'Zamanında Teslim', 'description': 'Söz verilen tarihte teslim.', 'icon': 'fas fa-clock'},
            {'name': 'Resmi Sözleşme', 'description': 'Yasal güvence ile çalışıyoruz.', 'icon': 'fas fa-file-contract'},
            {'name': 'Premium Malzeme', 'description': 'A sınıfı markalar kullanıyoruz.', 'icon': 'fas fa-star'},
        ]
        for data in features:
            Feature.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('✓ Özellikler oluşturuldu'))

    def create_hero(self):
        Hero.objects.create(
            title='Mekanlarınıza Altın Dokunuş',
            subtitle='Kaliteli Hizmet • Uygun Fiyat • 12 Ay Taksit',
            description='Mobilya boyama, tadilat ve iç mimarlık hizmetlerinde 10 yılı aşkın tecrübe.',
            primary_button_text='Ücretsiz Teklif Al',
            primary_button_link='tel:+905551234567',
            secondary_button_text='WhatsApp ile Yaz',
            secondary_button_link='https://wa.me/905551234567',
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS('✓ Hero oluşturuldu'))

    def create_comments(self):
        comments = [
            {'name': 'Ayşe K.', 'title': 'Pendik', 'comment': 'Mutfak dolaplarımızı boyattık, sanki yeni mutfak aldık! Fiyat da çok makuldü.'},
            {'name': 'Mehmet Y.', 'title': 'Kartal', 'comment': 'Bütçemiz kısıtlıydı ama harika bir çözüm buldular. Taksit de yaptılar!'},
            {'name': 'Zeynep A.', 'title': 'Ümraniye', 'comment': 'Koltuk döşeme işi mükemmel oldu. Yeni koltuk alsaydık 3 katı tutardı!'},
            {'name': 'Ali R.', 'title': 'Kadıköy', 'comment': 'Anahtar teslim tadilat yaptırdık. Söz verdikleri tarihte tamamladılar.'},
            {'name': 'Fatma S.', 'title': 'Maltepe', 'comment': 'Yatak odası mobilyalarımızı boyattık. Renk tam istediğimiz gibi oldu.'},
            {'name': 'Hasan D.', 'title': 'Ataşehir', 'comment': 'Ofisimizin tüm boya badana işini yaptılar. Hafta sonu çalıştılar.'},
        ]
        for data in comments:
            Comment.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('✓ Müşteri yorumları oluşturuldu'))

    def create_faqs(self):
        faqs = [
            {'question': 'Ücretsiz keşif nasıl yapılır?', 'answer': 'Bizi arayın veya WhatsApp\'tan yazın, size uygun zamanda adresinize gelip ücretsiz keşif yapıp fiyat teklifi sunalım.'},
            {'question': 'Taksit imkanı var mı?', 'answer': 'Evet, kredi kartınıza 12 aya varan taksit imkanı sunuyoruz.'},
            {'question': 'Garanti veriyor musunuz?', 'answer': 'Evet, tüm işlerimize 2 yıl işçilik garantisi veriyoruz.'},
            {'question': 'Hangi bölgelere hizmet veriyorsunuz?', 'answer': 'İstanbul\'un tüm ilçelerine hizmet veriyoruz.'},
            {'question': 'Mobilya boyama ne kadar sürer?', 'answer': 'Projenin büyüklüğüne göre değişir. Ortalama mutfak dolabı 3-5 gün sürer.'},
            {'question': 'Hangi malzemeleri kullanıyorsunuz?', 'answer': 'Jotun, Marshall, DYO gibi A sınıfı markaların ürünlerini kullanıyoruz.'},
        ]
        for data in faqs:
            Faq.objects.create(isActive=True, showIndex=True, **data)
        self.stdout.write(self.style.SUCCESS('✓ SSS oluşturuldu'))

    def create_categories(self):
        categories = [
            {'name': 'Mobilya Boyama', 'slug': 'mobilya-boyama', 'icon': 'fas fa-couch', 'order': 1},
            {'name': 'Tadilat', 'slug': 'tadilat', 'icon': 'fas fa-hammer', 'order': 2},
            {'name': 'Boya Badana', 'slug': 'boya-badana', 'icon': 'fas fa-paint-roller', 'order': 3},
            {'name': 'Döşeme', 'slug': 'doseme', 'icon': 'fas fa-th-large', 'order': 4},
        ]
        for data in categories:
            ServiceCategory.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('✓ Hizmet kategorileri oluşturuldu'))

    def create_services(self):
        # Get categories
        mobilya = ServiceCategory.objects.get(slug='mobilya-boyama')
        tadilat = ServiceCategory.objects.get(slug='tadilat')
        boya = ServiceCategory.objects.get(slug='boya-badana')
        doseme = ServiceCategory.objects.get(slug='doseme')

        # Service data with Unsplash image URLs
        services = [
            {
                'title': 'Mobilya Boyama & Yenileme',
                'slug': 'mobilya-boyama-yenileme',
                'short_description': 'Eski mobilyalarınızı yenilemek artık çok kolay. Profesyonel boyama ile mobilyalarınız sıfır gibi görünsün.',
                'description': '<p>Eski mobilyalarınızı değiştirmek yerine boyatarak hem tasarruf edin hem de çevreye katkı sağlayın.</p>',
                'category': mobilya,
                'image_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80',
            },
            {
                'title': 'Mutfak Dolabı Boyama',
                'slug': 'mutfak-dolabi-boyama',
                'short_description': 'Mutfağınızı yenilemek için dolap değiştirmeye gerek yok. Profesyonel boyama ile mutfağınız baştan yaratılsın.',
                'description': '<p>Mutfak dolabı boyama ile yeni mutfak maliyetinin %70\'ine kadar tasarruf edin.</p>',
                'category': mobilya,
                'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
            },
            {
                'title': 'Yatak Odası Mobilya Boyama',
                'slug': 'yatak-odasi-boyama',
                'short_description': 'Yatak odası mobilyalarınızı istediğiniz renkte yenileyin.',
                'description': '<p>Modern veya klasik, istediğiniz tarza uygun boyama hizmeti.</p>',
                'category': mobilya,
                'image_url': 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80',
            },
            {
                'title': 'Anahtar Teslim Tadilat',
                'slug': 'anahtar-teslim-tadilat',
                'short_description': 'A\'dan Z\'ye tüm tadilat işlerinizi tek elden, anahtar teslim olarak gerçekleştiriyoruz.',
                'description': '<p>Boya, elektrik, tesisat, parke, fayans dahil komple tadilat hizmeti.</p>',
                'category': tadilat,
                'image_url': 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',
            },
            {
                'title': 'Banyo Tadilat',
                'slug': 'banyo-tadilat',
                'short_description': 'Banyonuzu baştan aşağı yenileyin. Fayans, tesisat, dolap dahil.',
                'description': '<p>Komple banyo tadilat ve yenileme hizmetleri.</p>',
                'category': tadilat,
                'image_url': 'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80',
            },
            {
                'title': 'İç Cephe Boya Badana',
                'slug': 'ic-cephe-boya-badana',
                'short_description': 'Evinizin veya ofisinizin iç cephe boya badana işlerini profesyonelce yapıyoruz.',
                'description': '<p>Premium boyalar ve uzman ekibimizle kusursuz sonuçlar elde edin.</p>',
                'category': boya,
                'image_url': 'https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=800&q=80',
            },
            {
                'title': 'Dekoratif Boya',
                'slug': 'dekoratif-boya',
                'short_description': 'Saten, metalik, dokulu boya uygulamaları ile mekanlarınıza farklılık katın.',
                'description': '<p>Özel efekt boyalar ile benzersiz duvarlar.</p>',
                'category': boya,
                'image_url': 'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=800&q=80',
            },
            {
                'title': 'Koltuk Döşeme',
                'slug': 'koltuk-doseme',
                'short_description': 'Eski koltuklarınızı yenisi gibi yapıyoruz. Kumaş ve deri seçenekleri mevcut.',
                'description': '<p>Koltuk döşeme ile yeni koltuk maliyetinin çok altında çözümler.</p>',
                'category': doseme,
                'image_url': 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=800&q=80',
            },
            {
                'title': 'Laminat Parke Döşeme',
                'slug': 'laminat-parke-doseme',
                'short_description': 'Laminat ve masif parke döşeme hizmetleri ile zeminlerinizi yenileyin.',
                'description': '<p>Profesyonel parke döşeme ve cilalama.</p>',
                'category': doseme,
                'image_url': 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80',
            },
        ]
        
        self.stdout.write('  Hizmetler oluşturuluyor (resimlerle birlikte)...')
        
        for data in services:
            image_url = data.pop('image_url')
            
            service = Service.objects.create(
                showIndex=True,
                isActive=True,
                **data
            )
            
            # Download and attach image
            filename = f"{data['slug']}.jpg"
            image_content = self.download_image(image_url, filename)
            if image_content:
                service.image.save(filename, image_content, save=True)
                self.stdout.write(f"    ✓ {data['title']} + resim")
            else:
                self.stdout.write(f"    ✓ {data['title']} (resim yok)")
        
        self.stdout.write(self.style.SUCCESS('✓ Hizmetler oluşturuldu'))

    def create_projects(self):
        """Örnek projeler oluştur"""
        projects = [
            {
                'title': 'Modern Mutfak Dönüşümü',
                'slug': 'modern-mutfak-donusumu',
                'description': 'Kadıköy\'de gerçekleştirdiğimiz komple mutfak dolabı boyama projesi.',
                'location': 'Kadıköy, İstanbul',
                'category': 'Mutfak Dolabı Boyama',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
            },
            {
                'title': 'Klasik Yatak Odası Yenileme',
                'slug': 'klasik-yatak-odasi-yenileme',
                'description': 'Ataşehir\'de tamamladığımız yatak odası mobilya boyama projesi.',
                'location': 'Ataşehir, İstanbul',
                'category': 'Mobilya Boyama',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80',
            },
            {
                'title': 'Komple Ev Renovasyonu',
                'slug': 'komple-ev-renovasyonu',
                'description': 'Beşiktaş\'ta anahtar teslim gerçekleştirdiğimiz komple ev tadilat projesi.',
                'location': 'Beşiktaş, İstanbul',
                'category': 'Anahtar Teslim Tadilat',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',
            },
            {
                'title': 'Lüks Banyo Dönüşümü',
                'slug': 'luks-banyo-donusumu',
                'description': 'Bakırköy\'de gerçekleştirdiğimiz modern banyo tadilat projesi.',
                'location': 'Bakırköy, İstanbul',
                'category': 'Banyo Tadilat',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80',
            },
            {
                'title': 'Antika Koltuk Restorasyonu',
                'slug': 'antika-koltuk-restorasyonu',
                'description': 'Şişli\'de tamamladığımız antika koltuk döşeme ve restorasyon projesi.',
                'location': 'Şişli, İstanbul',
                'category': 'Koltuk Döşeme',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=800&q=80',
            },
            {
                'title': 'Ofis Boya Projesi',
                'slug': 'ofis-boya-projesi',
                'description': 'Levent\'te 500m² ofis alanının iç cephe boya projesi.',
                'location': 'Levent, İstanbul',
                'category': 'Boya Badana',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=800&q=80',
            },
        ]
        
        self.stdout.write('  Projeler oluşturuluyor (resimlerle birlikte)...')
        
        for data in projects:
            image_url = data.pop('image_url')
            
            project = Project.objects.create(
                show_on_index=True,
                is_active=True,
                **data
            )
            
            # Download and attach image
            filename = f"{data['slug']}.jpg"
            image_content = self.download_image(image_url, filename)
            if image_content:
                project.image.save(filename, image_content, save=True)
                self.stdout.write(f"    ✓ {data['title']} + resim")
            else:
                self.stdout.write(f"    ✓ {data['title']} (resim yok)")
        
        self.stdout.write(self.style.SUCCESS('✓ Projeler oluşturuldu'))
