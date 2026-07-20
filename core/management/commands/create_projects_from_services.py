"""
Django Management Command: create_projects_from_services
Hizmetlerdeki öncesi/sonrası resimlerini kullanarak yeni projeler oluşturur
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Project
from service.models import Service
from datetime import date
import random


# İstanbul ilçeleri - gerçekçi proje lokasyonları için
ISTANBUL_LOCATIONS = [
    'Kadıköy, İstanbul',
    'Beşiktaş, İstanbul',
    'Üsküdar, İstanbul',
    'Ataşehir, İstanbul',
    'Maltepe, İstanbul',
    'Kartal, İstanbul',
    'Pendik, İstanbul',
    'Bakırköy, İstanbul',
    'Şişli, İstanbul',
    'Fatih, İstanbul',
    'Beyoğlu, İstanbul',
    'Sarıyer, İstanbul',
    'Beykoz, İstanbul',
    'Çekmeköy, İstanbul',
    'Sancaktepe, İstanbul',
    'Bağcılar, İstanbul',
    'Küçükçekmece, İstanbul',
    'Başakşehir, İstanbul',
]


# Hizmet bazlı proje açıklamaları
PROJECT_TEMPLATES = {
    'Parke Kurulumu ve Renk Çeşitleri': {
        'title': '{location} Parke Döşeme Projesi',
        'description': '''Müşterimizin evinde gerçekleştirdiğimiz parke döşeme projesi, hem estetik hem de dayanıklılık açısından mükemmel sonuçlar verdi.

Proje kapsamında:
• Mevcut zemin kaldırılarak yüzey hazırlandı
• Nem yalıtımı ve ses izolasyonu yapıldı
• Yüksek kaliteli laminat parke döşendi
• Süpürgelik ve geçiş profilleri montajlandı

Müşterimiz, yeni parkesinin modern görünümünden ve kolay temizlenebilirliğinden oldukça memnun kaldı.''',
        'seo_title': '{location} Parke Döşeme | EB Dekorasyon',
        'seo_description': '{location} bölgesinde gerçekleştirdiğimiz profesyonel parke döşeme projesi. Kaliteli malzeme ve uzman işçilik.',
    },
    'Laminant Parke Döşeme': {
        'title': '{location} Laminat Parke Yenileme',
        'description': '''Eski ve yıpranmış zemini tamamen yenileyerek modern bir görünüm kazandırdığımız laminat parke projesi.

Uygulama detayları:
• Eski zemin kaplaması söküldü
• Alt zemin tamir ve tesviye edildi
• Premium kalite laminat parke döşendi
• Duvar kenarları ve geçişler özenle tamamlandı

Proje sonunda müşterimiz, evinin tamamen değiştiğini ve yenilenmiş hissettirdiğini belirtti.''',
        'seo_title': '{location} Laminat Parke | EB Dekorasyon',
        'seo_description': '{location} laminat parke döşeme projesi. Profesyonel uygulama ve kalıcı sonuçlar.',
    },
    'Ev İçi Genel Dekorasyon': {
        'title': '{location} Komple Salon Yenileme',
        'description': '''Müşterimizin oturma odasını tamamen yenileyerek modern ve şık bir yaşam alanına dönüştürdük.

Gerçekleştirilen işlemler:
• Duvar boyası ve dekoratif uygulamalar
• Zemin yenileme ve parke döşeme
• Aydınlatma düzenlemesi
• Mobilya yerleşim planlaması

Bu kapsamlı yenileme projesi, ev sahibinin yaşam kalitesini önemli ölçüde artırdı.''',
        'seo_title': '{location} Salon Yenileme | EB Dekorasyon',
        'seo_description': '{location} komple salon yenileme projesi. Profesyonel dekorasyon hizmeti.',
    },
    'Mobilya Tamiratı ve Bakımı': {
        'title': '{location} Antika Mobilya Restorasyonu',
        'description': '''Değerli antika mobilyanın orijinal güzelliğine kavuşturulduğu titiz bir restorasyon çalışması.

Restorasyon süreci:
• Hasarlı bölgelerin tespiti ve analizi
• Ahşap tamiri ve güçlendirme
• Orijinal renge uygun boya ve vernik
• Koruyucu son kat uygulaması

Müşterimiz, aile yadigârı mobilyasının yeniden hayat bulmasından büyük mutluluk duydu.''',
        'seo_title': '{location} Mobilya Tamiri | EB Dekorasyon',
        'seo_description': '{location} profesyonel mobilya tamiratı ve bakımı. Uzman eller ve kaliteli malzeme.',
    },
    'Kafe İçi Dekorasyon ve Tasarım': {
        'title': '{location} Kafe Dekorasyon Projesi',
        'description': '''Yeni açılacak kafenin iç mekan tasarımı ve dekorasyonunu üstlendiğimiz ticari proje.

Proje kapsamı:
• Konsept tasarımı ve 3D görselleştirme
• Duvar ve tavan dekoratif uygulamaları
• Özel mobilya seçimi ve yerleşimi
• Aydınlatma ve ambiyans düzenleme

Kafe, açılışından itibaren müşterilerden olumlu geri bildirimler aldı.''',
        'seo_title': '{location} Kafe Dekorasyonu | EB Dekorasyon',
        'seo_description': '{location} profesyonel kafe iç mekan tasarımı ve dekorasyonu.',
    },
    'Mutfak Tezgahı Değişimi ve Tamiri': {
        'title': '{location} Mutfak Tezgahı Yenileme',
        'description': '''Eski ve hasarlı mutfak tezgahının modern ve dayanıklı bir tezgahla değiştirildiği proje.

İşlem adımları:
• Mevcut tezgahın sökümü
• Ölçü alma ve malzeme seçimi
• Yeni tezgah montajı
• Evye ve batarya bağlantıları

Yeni tezgah, mutfağın genel görünümünü tamamen değiştirdi ve kullanım konforunu artırdı.''',
        'seo_title': '{location} Mutfak Tezgahı | EB Dekorasyon',
        'seo_description': '{location} mutfak tezgahı değişimi. Kaliteli malzeme ve profesyonel montaj.',
    },
    'Yatak Odası Mobilya Boyama': {
        'title': '{location} Yatak Odası Dolap Boyama',
        'description': '''Yatak odasındaki gardırop ve komodinin modern renge boyanarak yenilendiği proje.

Uygulama aşamaları:
• Yüzey temizliği ve zımparalama
• Astar uygulaması
• Seçilen renkte iki kat boya
• Koruyucu son kat vernik

Müşterimiz, eski mobilyalarına yeni bir hayat verilmesinden çok memnun kaldı.''',
        'seo_title': '{location} Dolap Boyama | EB Dekorasyon',
        'seo_description': '{location} yatak odası mobilya boyama. Profesyonel renk değişimi hizmeti.',
    },
    'Döşeme Yüzü Değişimi': {
        'title': '{location} Koltuk Döşeme Yenileme',
        'description': '''Eskimiş ve yıpranmış koltuğun döşeme yüzünün tamamen yenilendiği dönüşüm projesi.

Yapılan işlemler:
• Eski kumaşın sökümü
• İç dolgu kontrolü ve onarımı
• Yeni kumaş seçimi ve kesimi
• Profesyonel döşeme uygulaması

Yenilenen koltuk, oturma odasının yıldızı haline geldi.''',
        'seo_title': '{location} Koltuk Döşeme | EB Dekorasyon',
        'seo_description': '{location} koltuk döşeme yenileme. Kaliteli kumaş ve profesyonel işçilik.',
    },
    'Sandalye ve Masa Boyama': {
        'title': '{location} Yemek Masası Seti Boyama',
        'description': '''Yemek masası ve sandalyelerin modern bir renkle boyanarak yenilendiği proje.

Proje detayları:
• Eski boyanın sökülmesi
• Ahşap onarımı ve zımparalama
• Seçilen renkte boya uygulaması
• Mat veya parlak finish seçeneği

Set, yemek odasına modern ve şık bir görünüm kazandırdı.''',
        'seo_title': '{location} Masa Sandalye Boyama | EB Dekorasyon',
        'seo_description': '{location} yemek masası ve sandalye boyama hizmeti.',
    },
    'Mutfak Dolabı Boyama ve Renk Değişimi': {
        'title': '{location} Mutfak Dolabı Boyama',
        'description': '''Eski mutfak dolaplarının komple boyanarak mutfağa yeni bir görünüm kazandırıldığı dönüşüm projesi.

Uygulama süreci:
• Kapak ve çekmecelerin sökümü
• Yağ ve kir temizliği
• Astar ve boya uygulaması
• Kolların değişimi ve montaj

Mutfak, yenileme sonrası tamamen farklı ve modern bir görünüm kazandı.''',
        'seo_title': '{location} Mutfak Dolabı Boyama | EB Dekorasyon',
        'seo_description': '{location} mutfak dolabı boyama ve renk değişimi. Uygun fiyat ve kaliteli işçilik.',
    },
}


class Command(BaseCommand):
    help = 'Hizmetlerdeki öncesi/sonrası resimlerini kullanarak yeni projeler oluşturur'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Sadece ne yapılacağını göster, veritabanına kaydetme'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - Değişiklikler kaydedilmeyecek'))
        
        # Before ve after resmi olan hizmetleri al
        services_with_images = Service.objects.exclude(
            before_image=''
        ).exclude(
            before_image__isnull=True
        ).exclude(
            after_image=''
        ).exclude(
            after_image__isnull=True
        )
        
        self.stdout.write(f'Öncesi/sonrası resmi olan {services_with_images.count()} hizmet bulundu')
        
        created_count = 0
        skipped_count = 0
        
        for service in services_with_images:
            self.stdout.write(f'\nİşleniyor: {service.title}')
            
            # Template bul
            template = PROJECT_TEMPLATES.get(service.title)
            if not template:
                self.stdout.write(self.style.WARNING(f'  -> Template bulunamadı, atlanıyor'))
                skipped_count += 1
                continue
            
            # Rastgele lokasyon seç
            location = random.choice(ISTANBUL_LOCATIONS)
            location_short = location.split(',')[0]  # Sadece ilçe adı
            
            # Proje bilgilerini hazırla
            title = template['title'].format(location=location_short)
            slug = slugify(title)
            
            # Aynı slug'a sahip proje var mı kontrol et
            if Project.objects.filter(slug=slug).exists():
                # Slug'a numara ekle
                counter = 1
                while Project.objects.filter(slug=f'{slug}-{counter}').exists():
                    counter += 1
                slug = f'{slug}-{counter}'
            
            description = template['description']
            seo_title = template['seo_title'].format(location=location_short)
            seo_description = template['seo_description'].format(location=location_short)
            
            # Rastgele tamamlanma tarihi (son 1 yıl içinde)
            days_ago = random.randint(7, 365)
            completed_date = date.today().replace(
                year=date.today().year if days_ago < 365 else date.today().year - 1
            ) - __import__('datetime').timedelta(days=days_ago % 365)
            
            if dry_run:
                self.stdout.write(self.style.SUCCESS(f'  -> OLUŞTURULACAK: {title}'))
                self.stdout.write(f'     Slug: {slug}')
                self.stdout.write(f'     Lokasyon: {location}')
                self.stdout.write(f'     Hizmet: {service.title}')
                self.stdout.write(f'     Before: {service.before_image.name}')
                self.stdout.write(f'     After: {service.after_image.name}')
            else:
                # Proje oluştur
                project = Project.objects.create(
                    title=title,
                    slug=slug,
                    description=description,
                    location=location,
                    image=service.after_image.name,  # Ana görsel olarak after kullan
                    before_image=service.before_image.name,
                    after_image=service.after_image.name,
                    service=service,
                    category=service.category.name if service.category else '',  # Kategori adı
                    seo_title=seo_title,
                    seo_description=seo_description,
                    is_active=True,
                    show_on_index=True,
                    is_featured=random.choice([True, False]),
                    completed_date=completed_date
                )
                self.stdout.write(self.style.SUCCESS(f'  -> OLUŞTURULDU: {project.title} (ID: {project.id})'))
            
            created_count += 1
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Toplam {created_count} proje {"oluşturulacak" if dry_run else "oluşturuldu"}'))
        if skipped_count:
            self.stdout.write(self.style.WARNING(f'{skipped_count} hizmet atlandı (template bulunamadı)'))
