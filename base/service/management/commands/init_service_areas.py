"""
Django Management Command: init_service_areas
==============================================
İstanbul Anadolu Yakası ilçeleri için SEO uyumlu hizmet bölgesi sayfalarını oluşturur.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from service.models import ServiceArea
from core.models import Feature, Faq


class Command(BaseCommand):
    help = 'İstanbul Anadolu Yakası ilçeleri için Hizmet Bölgesi verilerini yükler.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Mevcut hizmet bölgelerini siler ve yeniden oluşturur.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n' + '=' * 60))
        self.stdout.write(self.style.WARNING('  EB DEKORASYON - HİZMET BÖLGELERİ OLUŞTURMA'))
        self.stdout.write(self.style.WARNING('=' * 60 + '\n'))

        if options['clear']:
            self.clear_existing_data()

        districts = [
            "Adalar", "Ataşehir", "Beykoz", "Çekmeköy", "Kadıköy", 
            "Kartal", "Maltepe", "Pendik", "Sancaktepe", "Sultanbeyli", 
            "Şile", "Tuzla", "Ümraniye", "Üsküdar"
        ]

        images = [
            'uploads/service_areas/modern_salon.jpg',
            'uploads/service_areas/luxury_kitchen.jpg',
            'uploads/service_areas/bedroom_remodel.jpg',
            'uploads/service_areas/bathroom_modern.jpg'
        ]

        created_count = 0
        for i, district in enumerate(districts):
            image_path = images[i % len(images)]
            self.create_service_area(district, image_path)
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'\n✅ Toplam {created_count} ilçe başarıyla oluşturuldu.'))

    def create_service_area(self, district, image_path):
        title = f"{district} Boya, Tadilat ve Dekorasyon Hizmetleri"
        slug = slugify(f"{district}-boya-tadilat-dekorasyon".replace('ı', 'i').replace('ş', 's').replace('ö', 'o').replace('ü', 'u').replace('ç', 'c').replace('ğ', 'g'))
        
        # SEO Başlık ve Açıklama
        seo_title = f"{district} Ev Tadilatı ve Dekorasyon | Mutfak & Parke & Boya | EB Dekorasyon"
        seo_description = f"{district} bölgesinde anahtar teslim ev tadilatı, mutfak dolabı boyama ve parke döşeme hizmetleri. {district} dekorasyon firması olarak ücretsiz keşif ile hizmetinizdeyiz."

        short_description = f"{district} ilçesinde profesyonel tadilat, dekorasyon ve mobilya yenileme çözümleri. Mutfak boyama, parke döşeme ve anahtar teslim projeleriniz için yerel uzmanlık."

        # Zengin HTML İçerik Şablonu
        description = f"""
            <h2>{district} Dekorasyon ve Tadilat Hizmetleri</h2>
            <p><strong>EB Dekorasyon</strong> olarak, İstanbul Anadolu Yakası'nın gözde ilçesi <strong>{district}</strong> bölgesinde yıllardır güvenle hizmet veriyoruz. Eskiyen evinizi yenilemek, mutfağınıza modern bir dokunuş katmak veya iş yerinizi baştan aşağı dekore etmek istiyorsanız, doğru yerdesiniz.</p>
            
            <p>{district} genelinde sunduğumuz profesyonel hizmetlerle, kırma-dökme derdi olmadan, ekonomik ve hızlı çözümler üretiyoruz. Hem estetik hem de fonksiyonel yaşam alanları yaratmak bizim işimiz.</p>

            <h3>{district} Bölgesinde Neler Yapıyoruz?</h3>
            
            <h4>1. Mutfak Dolabı Boyama ve Yenileme</h4>
            <p>Mutfak dolaplarınızın renginden sıkıldıysanız, onları komple değiştirmek yerine <strong>profesyonel lake veya akrilik boya</strong> ile yeniliyoruz. {district}'teki atölyemize taşıdığımız kapakları fırça izi olmadan, fabrikasyon kalitesinde boyayarak %70 tasarruf etmenizi sağlıyoruz.</p>
            
            <h4>2. Laminant Parke ve Zemin Çözümleri</h4>
            <p>{district} evlerinin zeminlerine şıklık katıyoruz. AGT, Çamsan gibi lider markaların laminant parke döşemesini, süpürgelik dahil anahtar teslim yapıyoruz. Dilerseniz Balıksırtı veya Macar kesim özel uygulamalarla salonunuza değer katıyoruz.</p>

            <h4>3. Anahtar Teslim Ev Tadilatı</h4>
            <p>Evinizi komple yenilemeyi mi düşünüyorsunuz? Tesisattan boyaya, alçıpandan banyo yenilemeye kadar A'dan Z'ye tüm süreci tek elden yönetiyoruz. Sürpriz maliyetler olmadan, söz verdiğimiz tarihte teslimat yapıyoruz.</p>

            <h4>4. Mobilya Tamiri ve Cila</h4>
            <p>Eski sandalyeleriniz, sallanan masalarınız veya rengi solmuş kapılarınız için yerinde veya atölyede tamir/cila hizmeti veriyoruz. {district} mobilya tamiri ekibimizle eşyalarınızı ilk günkü sağlamlığına kavuşturuyoruz.</p>

            <h3>Neden {district} İçin Bizi Seçmelisiniz?</h3>
            <ul>
                <li><strong>Yerel Uzmanlık:</strong> {district} bölgesinin mimari yapısını ve ihtiyaçlarını iyi biliyoruz.</li>
                <li><strong>Ücretsiz Keşif:</strong> {district} içindeki tüm mahallelere aynı gün ücretsiz keşif ekibimizi yönlendiriyoruz.</li>
                <li><strong>Garantili İşçilik:</strong> Yaptığımız tüm boya ve tadilat işçiliklerine 2 yıl firma garantisi veriyoruz.</li>
                <li><strong>Ekonomik Fiyatlar:</strong> Üretici firma avantajıyla aracı olmadan, en uygun fiyatları sunuyoruz.</li>
            </ul>

            <h3>Sıkça Sorulan Sorular ({district})</h3>
            
            <div class="faq-section">
                <p><strong>{district} içinde keşif ücretli mi?</strong><br>
                Hayır, {district} dahil tüm Anadolu Yakası'na keşif hizmetimiz tamamen ücretsizdir.</p>
                
                <p><strong>Tadilat süresince evde kalabilir miyiz?</strong><br>
                Mutfak boyama veya parke gibi lokal işlemlerde evde kalabilirsiniz. Ancak komple tadilatlarda (banyo, kırım-döküm) evin boş olması daha sağlıklı olacaktır.</p>
                
                <p><strong>{district} ofis dekorasyonu yapıyor musunuz?</strong><br>
                Evet, {district} bölgesindeki iş yerleri, ofisler ve kafeler için kurumsal dekorasyon çözümlerimiz mevcuttur.</p>
            </div>

            <p class="cta-box">
                <strong>{district} bölgesinde hayalinizdeki ev için ilk adımı atın!</strong><br>
                Hemen arayın, ücretsiz keşif randevunuzu oluşturalım: <a href="tel:+905555555555">0 555 555 55 55</a>
            </p>
        """

        # Veritabanına Kayıt
        service_area, created = ServiceArea.objects.update_or_create(
            slug=slug,
            defaults={
                'title': title,
                'seo_title': seo_title[:60],
                'seo_description': seo_description[:160],
                'short_description': short_description,
                'description': description,
                'image': image_path,
                'icon': 'fas fa-map-marker-alt',
                'isActive': True,
                'showIndex': True
            }
        )

        # Özellikler Ekle (Many-to-Many)
        features_list = ["Ücretsiz Keşif", "Yerinde Hizmet", "Zamanında Teslim", "Garantili İşçilik"]
        service_area.features.clear()
        for f_name in features_list:
            feature_obj, _ = Feature.objects.get_or_create(name=f_name, defaults={'description': f'{f_name} hizmeti', 'icon': 'fas fa-check'})
            service_area.features.add(feature_obj)
        
        # SSS Ekle (Opsiyonel: Eğer modele many-to-many bağlıysa)
        # ServiceArea modelinde faqs alanı varsa:
        if hasattr(service_area, 'faqs'):
            service_area.faqs.clear()
            local_faq = Faq.objects.create(
                question=f"{district} bölgesine servisiniz var mı?",
                answer=f"Evet, {district} ve tüm mahallelerine günlük servisimiz vardır.",
                isActive=True,
                showIndex=False
            )
            service_area.faqs.add(local_faq)

        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓ YENİ: {district}'))
        else:
            self.stdout.write(self.style.HTTP_INFO(f'  → GÜNCEL: {district}'))

    def clear_existing_data(self):
        self.stdout.write(self.style.WARNING('⚠️  Mevcut hizmet bölgeleri siliniyor...'))
        ServiceArea.objects.all().delete()
