import os
import urllib.request
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from core.models import Settings, Counter, Hero, Feature, FeatureArea, Comment, CommentHeader, Faq, Project
from service.models import Service, ServiceCategory
from blog.models import Blog, Category as BlogCategory, Tag


class Command(BaseCommand):
    help = 'EB Dekorasyon için tüm veritabanını sıfırdan oluşturur'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-only',
            action='store_true',
            help='Sadece mevcut verileri sil, yeni veri ekleme',
        )
        parser.add_argument(
            '--skip-images',
            action='store_true',
            help='Resimleri indirme (hızlı test için)',
        )

    def handle(self, *args, **options):
        self.skip_images = options.get('skip_images', False)
        
        self.stdout.write(self.style.WARNING('\n🗑️  Tüm veriler siliniyor...\n'))
        self.clear_all_data()
        
        if options['clear_only']:
            self.stdout.write(self.style.SUCCESS('\n✅ Tüm veriler silindi!'))
            return
        
        self.stdout.write(self.style.WARNING('\n🚀 EB Dekorasyon verileri yükleniyor...\n'))
        
        # Create data in order
        self.create_superuser()
        self.create_settings()
        self.create_counters()
        self.create_features()
        self.create_feature_area()
        self.create_hero()
        self.create_comments()
        self.create_comment_header()
        self.create_faqs()
        self.create_categories()
        self.create_services()
        self.create_projects()
        self.create_blog_data()
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('✅ TÜM VERİLER BAŞARIYLA YÜKLENDİ!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🌐 Site:  http://127.0.0.1:8000/'))
        self.stdout.write(self.style.SUCCESS('👤 Admin: http://127.0.0.1:8000/admin/'))
        self.stdout.write(self.style.SUCCESS('📧 User:  admin / admin123'))
        self.stdout.write('')

    def clear_all_data(self):
        """Tüm seed verilerini sil"""
        # Blog
        Blog.objects.all().delete()
        self.stdout.write('  ✓ Blog silindi')
        
        BlogCategory.objects.all().delete()
        self.stdout.write('  ✓ Blog Category silindi')
        
        Tag.objects.all().delete()
        self.stdout.write('  ✓ Tag silindi')
        
        # Core
        Project.objects.all().delete()
        self.stdout.write('  ✓ Project silindi')
        
        Service.objects.all().delete()
        self.stdout.write('  ✓ Service silindi')
        
        ServiceCategory.objects.all().delete()
        self.stdout.write('  ✓ ServiceCategory silindi')
        
        Comment.objects.all().delete()
        self.stdout.write('  ✓ Comment silindi')
        
        CommentHeader.objects.all().delete()
        self.stdout.write('  ✓ CommentHeader silindi')
        
        Faq.objects.all().delete()
        self.stdout.write('  ✓ Faq silindi')
        
        Counter.objects.all().delete()
        self.stdout.write('  ✓ Counter silindi')
        
        Feature.objects.all().delete()
        self.stdout.write('  ✓ Feature silindi')
        
        FeatureArea.objects.all().delete()
        self.stdout.write('  ✓ FeatureArea silindi')
        
        Hero.objects.all().delete()
        self.stdout.write('  ✓ Hero silindi')
        
        # Settings - sadece güncelle, silme
        Settings.objects.all().delete()
        self.stdout.write('  ✓ Settings silindi')

    def download_image(self, url, filename):
        """Unsplash'tan resim indir ve kaydet"""
        if self.skip_images:
            return None
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=15)
            image_data = response.read()
            return ContentFile(image_data, name=filename)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'    ⚠ Resim indirilemedi: {e}'))
            return None

    def create_superuser(self):
        """Admin kullanıcısı oluştur"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ebdekorasyon.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superuser oluşturuldu (admin/admin123)'))
        else:
            self.stdout.write('  ℹ Superuser zaten mevcut')

    def create_settings(self):
        Settings.objects.create(
            name='EB Dekorasyon',
            domain='ebdekorasyon.com',
            phone='+90 532 123 45 67',
            whatsapp='905321234567',
            email='info@ebdekorasyon.com',
            adress='Maltepe, İstanbul, Türkiye',
            instagram='https://instagram.com/ebdekorasyon',
            facebook='https://facebook.com/ebdekorasyon',
            alternate_name='EB Dekorasyon Boya Tadilat Mobilya Yenileme',
            city='İstanbul',
            region='Anadolu Yakası',
            founding_date='2014',
            average_rating='4.9',
            review_count='247',
            number_of_employees='15-25',
            seo_title='EB Dekorasyon | İstanbul Boya Tadilat & Mobilya Boyama',
            seo_description='İstanbul\'un en güvenilir boya, tadilat ve mobilya yenileme hizmetleri. Mutfak dolabı boyama, koltuk döşeme, anahtar teslim tadilat. 10+ yıl tecrübe, 2 yıl garanti.',
            enable_sitemap=True,
            enable_robots_txt=True,
            enable_structured_data=True,
        )
        self.stdout.write(self.style.SUCCESS('✓ Settings oluşturuldu'))

    def create_counters(self):
        counters = [
            {'name': 'Mutlu Müşteri', 'count': '500+', 'icon': 'fas fa-smile'},
            {'name': 'Yıllık Tecrübe', 'count': '10+', 'icon': 'fas fa-calendar-alt'},
            {'name': 'Sigortalı Ekip', 'count': '%100', 'icon': 'fas fa-shield-alt'},
            {'name': 'Tamamlanan Proje', 'count': '750+', 'icon': 'fas fa-check-circle'},
        ]
        for data in counters:
            Counter.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('✓ Sayaçlar oluşturuldu (4 adet)'))

    def create_features(self):
        features = [
            {'name': '2 Yıl Garanti', 'description': 'Tüm işlerimize 2 yıl işçilik garantisi veriyoruz.', 'icon': 'fas fa-shield-alt'},
            {'name': 'Ücretsiz Keşif', 'description': 'Yerinize gelip ücretsiz keşif ve fiyat teklifi sunuyoruz.', 'icon': 'fas fa-search-location'},
            {'name': '12 Ay Taksit', 'description': 'Kredi kartına 12 aya varan taksit imkanı.', 'icon': 'fas fa-credit-card'},
            {'name': 'Zamanında Teslim', 'description': 'Söz verilen tarihte projenizi teslim ediyoruz.', 'icon': 'fas fa-clock'},
            {'name': 'Resmi Sözleşme', 'description': 'Tüm projeler için yasal güvence sağlıyoruz.', 'icon': 'fas fa-file-contract'},
            {'name': 'Premium Malzeme', 'description': 'Jotun, Marshall gibi A sınıfı markalar kullanıyoruz.', 'icon': 'fas fa-star'},
        ]
        for data in features:
            Feature.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('✓ Özellikler oluşturuldu (6 adet)'))

    def create_feature_area(self):
        """Neden Bizi Seçmelisiniz bölümü için FeatureArea oluştur"""
        # Get first 4 features for Why Choose Us section
        features = Feature.objects.all()[:4]
        
        feature_area = FeatureArea.objects.create(
            header='Neden',
            title='Bizi Seçmelisiniz?',
            short_description='10 yılı aşkın tecrübemiz ve müşteri memnuniyeti odaklı yaklaşımımızla fark yaratıyoruz.',
        )
        
        # Add features to the area
        feature_area.features.add(*features)
        
        self.stdout.write(self.style.SUCCESS('✓ FeatureArea (Neden Bizi Seçmelisiniz) oluşturuldu'))

    def create_hero(self):
        hero = Hero.objects.create(
            title='Mekanlarınıza <span class="text-gold-gradient">Altın Dokunuş</span>',
            subtitle='Kaliteli Hizmet • Uygun Fiyat • 12 Ay Taksit',
            description='Mobilya boyama, tadilat ve iç mimarlık hizmetlerinde 10 yılı aşkın tecrübe. Yeni almaktan %70 daha uygun fiyatlarla mekanlarınızı yenileyin.',
            primary_button_text='Hemen Ara',
            primary_button_link='tel:+905321234567',
            primary_button_icon='fas fa-phone',
            secondary_button_text='WhatsApp ile Yaz',
            secondary_button_link='https://wa.me/905321234567',
            secondary_button_icon='fab fa-whatsapp',
            is_active=True,
        )
        
        # Hero banner image
        image_url = 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1920&q=80'
        image_content = self.download_image(image_url, 'hero_banner.jpg')
        if image_content:
            hero.banner.save('hero_banner.jpg', image_content, save=True)
        
        self.stdout.write(self.style.SUCCESS('✓ Hero oluşturuldu'))

    def create_comments(self):
        comments = [
            {'name': 'Ayşe Kaya', 'title': 'Pendik', 'comment': 'Mutfak dolaplarımızı boyattık, sanki yeni mutfak aldık! Fiyat da çok makuldü. Kesinlikle tavsiye ederim.'},
            {'name': 'Mehmet Yılmaz', 'title': 'Kartal', 'comment': 'Bütçemiz kısıtlıydı ama harika bir çözüm buldular. Taksit de yaptılar! Çok memnun kaldık.'},
            {'name': 'Zeynep Arslan', 'title': 'Ümraniye', 'comment': 'Koltuk döşeme işi mükemmel oldu. Yeni koltuk alsaydık 3 katı tutardı! Ekip çok profesyoneldi.'},
            {'name': 'Ali Demir', 'title': 'Kadıköy', 'comment': 'Anahtar teslim ev tadilatı yaptırdık. Söz verdikleri tarihte tamamladılar ve sonuç beklentilerimizin üzerindeydi.'},
            {'name': 'Fatma Şen', 'title': 'Maltepe', 'comment': 'Yatak odası mobilyalarımızı mat siyah boyattık. Renk tam istediğimiz gibi oldu, harika iş çıkardılar.'},
            {'name': 'Hasan Çelik', 'title': 'Ataşehir', 'comment': 'Ofisimizin tüm boya badana işini hafta sonu yaptılar. İş günü kaybetmedik, çok teşekkürler!'},
        ]
        for data in comments:
            Comment.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('✓ Müşteri yorumları oluşturuldu (6 adet)'))

    def create_comment_header(self):
        CommentHeader.objects.create(
            title='Müşterilerimiz Ne Diyor?',
            description='Binlerce mutlu müşterimizden bazıları'
        )
        self.stdout.write(self.style.SUCCESS('✓ CommentHeader oluşturuldu'))

    def create_faqs(self):
        faqs = [
            {'question': 'Ücretsiz keşif nasıl yapılır?', 'answer': 'Bizi telefonla arayın veya WhatsApp\'tan yazın. Size uygun bir zamanda adresinize gelip ücretsiz keşif yapıp, yerinde fiyat teklifi sunuyoruz. Hiçbir bağlayıcılığı yoktur.'},
            {'question': 'Taksit imkanı var mı?', 'answer': 'Evet! Tüm kredi kartlarına 12 aya varan taksit imkanı sunuyoruz. Ayrıca havale/EFT ile ödeme seçeneğimiz de mevcuttur.'},
            {'question': 'Garanti veriyor musunuz?', 'answer': 'Evet, tüm işlerimize 2 yıl işçilik garantisi veriyoruz. Garanti süresince oluşabilecek sorunları ücretsiz olarak gideriyoruz.'},
            {'question': 'Hangi bölgelere hizmet veriyorsunuz?', 'answer': 'İstanbul\'un tüm ilçelerine, özellikle Anadolu Yakası\'na (Kadıköy, Maltepe, Kartal, Pendik, Ümraniye, Ataşehir) hizmet veriyoruz.'},
            {'question': 'Mobilya boyama ne kadar sürer?', 'answer': 'Projenin büyüklüğüne göre değişir. Ortalama bir mutfak dolabı seti 3-5 iş günü, yatak odası takımı 2-4 iş günü sürmektedir.'},
            {'question': 'Hangi malzemeleri kullanıyorsunuz?', 'answer': 'Jotun, Marshall, DYO, Filli Boya gibi A sınıfı markaların premium ürünlerini kullanıyoruz. Su bazlı, kokusuz ve sağlığa zararsız boyalar tercih ediyoruz.'},
            {'question': 'Eşyalarımı taşımanız gerekiyor mu?', 'answer': 'Mobilya boyama için genellikle eşyaları atölyemize alıyoruz. Yerinde yapılacak işlerde ise gerekli koruma önlemlerini biz alıyoruz.'},
            {'question': 'Hafta sonu çalışıyor musunuz?', 'answer': 'Evet! Cumartesi tam gün, Pazar günü ise randevu ile çalışıyoruz. Acil işler için 7/24 WhatsApp hattımızdan bize ulaşabilirsiniz.'},
        ]
        for data in faqs:
            Faq.objects.create(isActive=True, showIndex=True, **data)
        self.stdout.write(self.style.SUCCESS('✓ SSS oluşturuldu (8 adet)'))

    def create_categories(self):
        categories = [
            {'name': 'Mobilya Boyama', 'slug': 'mobilya-boyama', 'icon': 'fas fa-couch', 'order': 1},
            {'name': 'Tadilat', 'slug': 'tadilat', 'icon': 'fas fa-hammer', 'order': 2},
            {'name': 'Boya Badana', 'slug': 'boya-badana', 'icon': 'fas fa-paint-roller', 'order': 3},
            {'name': 'Döşeme', 'slug': 'doseme', 'icon': 'fas fa-th-large', 'order': 4},
        ]
        for data in categories:
            ServiceCategory.objects.create(is_active=True, **data)
        self.stdout.write(self.style.SUCCESS('✓ Hizmet kategorileri oluşturuldu (4 adet)'))

    def create_services(self):
        mobilya = ServiceCategory.objects.get(slug='mobilya-boyama')
        tadilat = ServiceCategory.objects.get(slug='tadilat')
        boya = ServiceCategory.objects.get(slug='boya-badana')
        doseme = ServiceCategory.objects.get(slug='doseme')

        services = [
            {
                'title': 'Mobilya Boyama & Yenileme',
                'slug': 'mobilya-boyama-yenileme',
                'short_description': 'Eski mobilyalarınızı yenilemek artık çok kolay. Profesyonel boyama ile mobilyalarınız sıfır gibi görünsün.',
                'description': '<h3>Neden Mobilya Boyama?</h3><p>Eski mobilyalarınızı değiştirmek yerine boyatarak hem tasarruf edin hem de çevreye katkı sağlayın. Yeni mobilya almanın %70\'ine kadar daha uygun fiyatlarla aynı görünümü elde edin.</p><h3>Hizmet Kapsamı</h3><ul><li>Ahşap mobilya boyama</li><li>Kaplama yenileme</li><li>Renk değişimi</li><li>Mat, saten veya parlak finish seçenekleri</li></ul>',
                'category': mobilya,
                'image_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80',
                'seo_title': 'Mobilya Boyama Hizmeti | EB Dekorasyon İstanbul',
                'seo_description': 'İstanbul\'da profesyonel mobilya boyama hizmeti. Eski mobilyalarınızı yenisi gibi yapıyoruz.',
            },
            {
                'title': 'Mutfak Dolabı Boyama',
                'slug': 'mutfak-dolabi-boyama',
                'short_description': 'Mutfağınızı yenilemek için dolap değiştirmeye gerek yok. Profesyonel boyama ile mutfağınız baştan yaratılsın.',
                'description': '<h3>Mutfak Dolabı Boyama ile Tasarruf</h3><p>Mutfak dolabı değiştirmek pahalı ve zahmetli bir iş. Bizimle çalışarak mevcut dolaplarınızı istediğiniz renge boyatabilir, modern bir görünüm elde edebilirsiniz.</p><h3>Süreç</h3><ol><li>Ücretsiz keşif ve renk danışmanlığı</li><li>Dolap kapaklarının sökülmesi</li><li>Atölyede profesyonel boyama</li><li>Montaj ve teslimat</li></ol>',
                'category': mobilya,
                'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
                'seo_title': 'Mutfak Dolabı Boyama | EB Dekorasyon İstanbul',
                'seo_description': 'Mutfak dolabı boyama ile mutfağınızı yenileyin. Değiştirmeden, %70 tasarrufla yeni mutfak görünümü.',
            },
            {
                'title': 'Yatak Odası Mobilya Boyama',
                'slug': 'yatak-odasi-mobilya-boyama',
                'short_description': 'Yatak odası mobilyalarınızı istediğiniz renkte yenileyin. Modern veya klasik, hayalinizdeki tarza kavuşun.',
                'description': '<p>Yatak odası takımınız eskidi mi? Değiştirmek yerine boyatarak yenileyin ve evdeki en keyifli odanızı baştan yaratın.</p>',
                'category': mobilya,
                'image_url': 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80',
                'seo_title': 'Yatak Odası Mobilya Boyama | EB Dekorasyon',
                'seo_description': 'Yatak odası mobilya boyama hizmeti. Komidin, gardırop, şifonyer boyama.',
            },
            {
                'title': 'Anahtar Teslim Tadilat',
                'slug': 'anahtar-teslim-tadilat',
                'short_description': 'A\'dan Z\'ye tüm tadilat işlerinizi tek elden, anahtar teslim olarak gerçekleştiriyoruz.',
                'description': '<h3>Komple Ev Tadilatı</h3><p>Boya, elektrik, tesisat, parke, fayans, mutfak, banyo dahil tüm tadilat işlerinizi tek elden yapıyoruz. Sizin hiçbir şeyle uğraşmanıza gerek yok!</p><h3>Dahil Olan İşler</h3><ul><li>İç ve dış cephe boya badana</li><li>Elektrik tesisatı yenileme</li><li>Su tesisatı</li><li>Parke ve seramik döşeme</li><li>Alçı ve kartonpiyer</li><li>Kapı ve pencere değişimi</li></ul>',
                'category': tadilat,
                'image_url': 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',
                'seo_title': 'Anahtar Teslim Tadilat | EB Dekorasyon İstanbul',
                'seo_description': 'İstanbul\'da anahtar teslim ev ve ofis tadilatı. Boya, elektrik, tesisat, parke, fayans dahil.',
            },
            {
                'title': 'Banyo Tadilat',
                'slug': 'banyo-tadilat',
                'short_description': 'Banyonuzu baştan aşağı yenileyin. Fayans, tesisat, vitrifiye, dolap dahil komple çözümler.',
                'description': '<p>Modern, kullanışlı ve şık bir banyo istiyorsanız doğru adrestesiniz. Komple banyo tadilat ve yenileme hizmetleri sunuyoruz.</p>',
                'category': tadilat,
                'image_url': 'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80',
                'seo_title': 'Banyo Tadilat | EB Dekorasyon İstanbul',
                'seo_description': 'İstanbul\'da komple banyo tadilat hizmeti. Seramik, tesisat, vitrifiye dahil.',
            },
            {
                'title': 'İç Cephe Boya Badana',
                'slug': 'ic-cephe-boya-badana',
                'short_description': 'Evinizin veya ofisinizin iç cephe boya badana işlerini profesyonelce yapıyoruz.',
                'description': '<h3>Profesyonel Boya Hizmeti</h3><p>Premium boyalar ve uzman ekibimizle kusursuz sonuçlar elde edin. Jotun, Marshall, DYO gibi A sınıfı markaların ürünlerini kullanıyoruz.</p>',
                'category': boya,
                'image_url': 'https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=800&q=80',
                'seo_title': 'İç Cephe Boya Badana | EB Dekorasyon İstanbul',
                'seo_description': 'İstanbul\'da iç cephe boya badana hizmeti. Premium boyalar, uzman ekip.',
            },
            {
                'title': 'Dekoratif Boya',
                'slug': 'dekoratif-boya',
                'short_description': 'Saten, metalik, dokulu boya uygulamaları ile mekanlarınıza farklılık katın.',
                'description': '<p>Özel efekt boyalar ile benzersiz duvarlar. Saten, metalik, hareli, patina ve dokulu boya seçeneklerimizle evinize karakter katın.</p>',
                'category': boya,
                'image_url': 'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=800&q=80',
                'seo_title': 'Dekoratif Boya Uygulama | EB Dekorasyon İstanbul',
                'seo_description': 'Dekoratif boya uygulamaları. Saten, metalik, dokulu boya çeşitleri.',
            },
            {
                'title': 'Koltuk Döşeme',
                'slug': 'koltuk-doseme',
                'short_description': 'Eski koltuklarınızı yenisi gibi yapıyoruz. Kumaş ve deri seçenekleri mevcut.',
                'description': '<h3>Koltuk Yenileme Hizmeti</h3><p>Sevdiğiniz koltuğunuzu atmayın! Kumaş veya deri değişimi ile yeniden hayat verin. Yeni koltuk maliyetinin çok altında profesyonel çözümler.</p>',
                'category': doseme,
                'image_url': 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=800&q=80',
                'seo_title': 'Koltuk Döşeme | EB Dekorasyon İstanbul',
                'seo_description': 'İstanbul\'da koltuk döşeme hizmeti. Kumaş ve deri seçenekleri.',
            },
            {
                'title': 'Laminat Parke Döşeme',
                'slug': 'laminat-parke-doseme',
                'short_description': 'Laminat ve masif parke döşeme hizmetleri ile zeminlerinizi yenileyin.',
                'description': '<p>Profesyonel parke döşeme ve cilalama hizmetleri. Laminat, masif ve lamine parke seçenekleri mevcuttur.</p>',
                'category': doseme,
                'image_url': 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80',
                'seo_title': 'Laminat Parke Döşeme | EB Dekorasyon İstanbul',
                'seo_description': 'Laminat ve masif parke döşeme hizmeti. Profesyonel zemin kaplama.',
            },
        ]
        
        self.stdout.write('  Hizmetler oluşturuluyor...')
        
        for data in services:
            image_url = data.pop('image_url')
            
            service = Service.objects.create(
                showIndex=True,
                isActive=True,
                **data
            )
            
            filename = f"{data['slug']}.jpg"
            image_content = self.download_image(image_url, filename)
            if image_content:
                service.image.save(filename, image_content, save=True)
                self.stdout.write(f"    ✓ {data['title']}")
            else:
                self.stdout.write(f"    ✓ {data['title']} (resim yok)")
        
        self.stdout.write(self.style.SUCCESS('✓ Hizmetler oluşturuldu (9 adet)'))

    def create_projects(self):
        """Örnek projeler oluştur - öncesi/sonrası resimlerle"""
        projects = [
            {
                'title': 'Modern Mutfak Dönüşümü',
                'slug': 'modern-mutfak-donusumu',
                'description': 'Kadıköy\'de gerçekleştirdiğimiz komple mutfak dolabı boyama projesi. Eski meşe rengi dolaplar mat beyaza dönüştürüldü.',
                'location': 'Kadıköy, İstanbul',
                'category': 'Mutfak Dolabı Boyama',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
                'before_url': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&q=80',
                'after_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
            },
            {
                'title': 'Klasik Yatak Odası Yenileme',
                'slug': 'klasik-yatak-odasi-yenileme',
                'description': 'Ataşehir\'de tamamladığımız yatak odası mobilya boyama projesi. Ceviz takım mat antrasit griye boyandı.',
                'location': 'Ataşehir, İstanbul',
                'category': 'Mobilya Boyama',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80',
                'before_url': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&q=80',
                'after_url': 'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80',
            },
            {
                'title': 'Komple Ev Renovasyonu',
                'slug': 'komple-ev-renovasyonu',
                'description': 'Beşiktaş\'ta anahtar teslim gerçekleştirdiğimiz 3+1 daire komple tadilat projesi. Boya, parke, elektrik, tesisat dahil.',
                'location': 'Beşiktaş, İstanbul',
                'category': 'Anahtar Teslim Tadilat',
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80',
                'before_url': None,
                'after_url': None,
            },
            {
                'title': 'Lüks Banyo Dönüşümü',
                'slug': 'luks-banyo-donusumu',
                'description': 'Bakırköy\'de gerçekleştirdiğimiz modern banyo tadilat projesi. Seramik, vitrifiye ve tesisat komple yenilendi.',
                'location': 'Bakırköy, İstanbul',
                'category': 'Banyo Tadilat',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80',
                'before_url': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=800&q=80',
                'after_url': 'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80',
            },
            {
                'title': 'Antika Koltuk Restorasyonu',
                'slug': 'antika-koltuk-restorasyonu',
                'description': 'Şişli\'de tamamladığımız antika Chester koltuk takımı döşeme ve restorasyon projesi.',
                'location': 'Şişli, İstanbul',
                'category': 'Koltuk Döşeme',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=800&q=80',
                'before_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80',
                'after_url': 'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=800&q=80',
            },
            {
                'title': 'Ofis Boya Projesi',
                'slug': 'ofis-boya-projesi',
                'description': 'Levent\'te 500m² açık ofis alanının iç cephe boya projesi. Hafta sonu çalışarak iş günü kaybı yaşatmadık.',
                'location': 'Levent, İstanbul',
                'category': 'Boya Badana',
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=800&q=80',
                'before_url': None,
                'after_url': None,
            },
        ]
        
        self.stdout.write('  Projeler oluşturuluyor...')
        
        for data in projects:
            image_url = data.pop('image_url')
            before_url = data.pop('before_url')
            after_url = data.pop('after_url')
            
            project = Project.objects.create(
                show_on_index=True,
                is_active=True,
                **data
            )
            
            # Main image
            filename = f"project_{data['slug']}.jpg"
            image_content = self.download_image(image_url, filename)
            if image_content:
                project.image.save(filename, image_content, save=True)
            
            # Before image
            if before_url:
                before_content = self.download_image(before_url, f"before_{data['slug']}.jpg")
                if before_content:
                    project.before_image.save(f"before_{data['slug']}.jpg", before_content, save=True)
            
            # After image
            if after_url:
                after_content = self.download_image(after_url, f"after_{data['slug']}.jpg")
                if after_content:
                    project.after_image.save(f"after_{data['slug']}.jpg", after_content, save=True)
            
            has_comparison = "✓ öncesi/sonrası" if before_url else ""
            self.stdout.write(f"    ✓ {data['title']} {has_comparison}")
        
        self.stdout.write(self.style.SUCCESS('✓ Projeler oluşturuldu (6 adet, 4 öncesi/sonrası)'))

    def create_blog_data(self):
        """Blog kategorileri, etiketler ve yazıları oluştur"""
        # Categories
        categories = {
            'ipuclari': BlogCategory.objects.create(name='İpuçları & Rehberler', slug='ipuclari-rehberler'),
            'trendler': BlogCategory.objects.create(name='Dekorasyon Trendleri', slug='dekorasyon-trendleri'),
            'projeler': BlogCategory.objects.create(name='Proje Hikayeleri', slug='proje-hikayeleri'),
        }
        
        # Tags
        tags = {
            'mobilya': Tag.objects.create(name='Mobilya Boyama', slug='mobilya-boyama'),
            'mutfak': Tag.objects.create(name='Mutfak', slug='mutfak'),
            'tadilat': Tag.objects.create(name='Tadilat', slug='tadilat'),
            'boya': Tag.objects.create(name='Boya Badana', slug='boya-badana'),
            'tasarruf': Tag.objects.create(name='Tasarruf', slug='tasarruf'),
            'diy': Tag.objects.create(name='Kendin Yap', slug='kendin-yap'),
        }
        
        blogs = [
            {
                'title': 'Mutfak Dolabı Boyama: Adım Adım Rehber',
                'slug': 'mutfak-dolabi-boyama-rehber',
                'short_description': 'Mutfak dolaplarınızı boyatmayı düşünüyor musunuz? İşte bilmeniz gereken her şey.',
                'description': '''
                <h2>Mutfak Dolabı Boyama Nedir?</h2>
                <p>Mutfak dolabı boyama, mevcut dolaplarınızın yüzeyini profesyonel tekniklerle yenileyerek tamamen farklı bir görünüm elde etmenizi sağlar.</p>
                
                <h2>Neden Dolap Değiştirmek Yerine Boyatmalısınız?</h2>
                <ul>
                    <li><strong>%70'e varan tasarruf:</strong> Yeni mutfak almanın çok altında maliyetlerle aynı görünümü elde edin.</li>
                    <li><strong>Daha kısa süre:</strong> Mutfak değişimi haftalarca sürerken, boyama 3-5 günde tamamlanır.</li>
                    <li><strong>Çevre dostu:</strong> Atık üretmeden mevcut mobilyalarınızı değerlendirin.</li>
                </ul>
                
                <h2>Süreç Nasıl İşler?</h2>
                <ol>
                    <li>Ücretsiz keşif ve renk danışmanlığı</li>
                    <li>Dolap kapaklarının sökülmesi</li>
                    <li>Atölyede zımparalama ve astar uygulaması</li>
                    <li>Profesyonel sprey boyama</li>
                    <li>Kuruma ve son kat uygulama</li>
                    <li>Montaj ve teslimat</li>
                </ol>
                ''',
                'category': categories['ipuclari'],
                'tag_keys': ['mobilya', 'mutfak', 'tasarruf'],
                'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80',
                'seo_title': 'Mutfak Dolabı Boyama Rehberi | EB Dekorasyon',
                'seo_description': 'Mutfak dolabı boyama hakkında bilmeniz gereken her şey. Maliyet, süreç ve avantajlar.',
            },
            {
                'title': '2024 Ev Dekorasyon Trendleri',
                'slug': '2024-ev-dekorasyon-trendleri',
                'short_description': 'Bu yılın en popüler ev dekorasyon trendlerini ve renk paletlerini keşfedin.',
                'description': '''
                <h2>2024'ün Öne Çıkan Trendleri</h2>
                <p>Bu yıl ev dekorasyonunda doğallık, sadelik ve sıcak tonlar ön plana çıkıyor.</p>
                
                <h3>1. Toprak Tonları Dönüşü</h3>
                <p>Terracotta, bej, krem ve kahverengi tonları bu yılın favorileri arasında.</p>
                
                <h3>2. Mat Siyah Detaylar</h3>
                <p>Mat siyah musluklar, kulplar ve aydınlatma elemanları modern bir kontrast sağlıyor.</p>
                
                <h3>3. Sürdürülebilir Malzemeler</h3>
                <p>Geri dönüştürülmüş ahşap ve doğal lifler popülerliğini koruyor.</p>
                ''',
                'category': categories['trendler'],
                'tag_keys': ['boya', 'diy'],
                'image_url': 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800&q=80',
                'seo_title': '2024 Ev Dekorasyon Trendleri | EB Dekorasyon',
                'seo_description': '2024 yılının en popüler ev dekorasyon trendleri, renk paletleri ve tasarım ipuçları.',
            },
            {
                'title': 'Kadıköy\'de Komple Mutfak Dönüşümü',
                'slug': 'kadikoy-mutfak-donusumu-projesi',
                'short_description': 'Kadıköy\'deki müşterimizin mutfağını nasıl baştan yarattığımızı anlatıyoruz.',
                'description': '''
                <h2>Proje Hikayesi</h2>
                <p>Kadıköy'de yaşayan Ayşe Hanım, 15 yıllık mutfak dolaplarını yenilemek istiyordu ancak bütçesi kısıtlıydı.</p>
                
                <h3>Müşteri İsteği</h3>
                <p>Koyu meşe rengi dolapları mat beyaza çevirmek ve modern bir görünüm elde etmek.</p>
                
                <h3>Çözümümüz</h3>
                <p>Dolap boyama hizmeti ile yeni mutfak maliyetinin %30'una aynı görünümü sağladık.</p>
                
                <h3>Sonuç</h3>
                <p>Ayşe Hanım: "Sanki yeni mutfak aldık, herkes yenilediğimizi sanıyor!"</p>
                ''',
                'category': categories['projeler'],
                'tag_keys': ['mobilya', 'mutfak'],
                'image_url': 'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&q=80',
                'seo_title': 'Kadıköy Mutfak Dönüşümü Projesi | EB Dekorasyon',
                'seo_description': 'Kadıköy\'de gerçekleştirdiğimiz mutfak dolabı boyama projesinin hikayesi.',
            },
        ]
        
        self.stdout.write('  Blog içerikleri oluşturuluyor...')
        
        for data in blogs:
            image_url = data.pop('image_url')
            tag_keys = data.pop('tag_keys')
            
            blog = Blog.objects.create(
                isActive=True,
                showIndex=True,
                **data
            )
            
            # Add tags
            for key in tag_keys:
                blog.tags.add(tags[key])
            
            # Download image
            filename = f"blog_{data['slug']}.jpg"
            image_content = self.download_image(image_url, filename)
            if image_content:
                blog.image.save(filename, image_content, save=True)
                self.stdout.write(f"    ✓ {data['title']}")
            else:
                self.stdout.write(f"    ✓ {data['title']} (resim yok)")
        
        self.stdout.write(self.style.SUCCESS('✓ Blog içerikleri oluşturuldu (3 kategori, 6 etiket, 3 yazı)'))
