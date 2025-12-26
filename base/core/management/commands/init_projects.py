"""
Django Management Command: init_projects
=========================================
EB Dekorasyon proje/portfolyo verilerini gerçekçi içeriklerle doldurur.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Project
from service.models import Service

# =============================================================================
# PROJE VERİ SETİ
# =============================================================================
PROJECTS_DATA = [
    {
        "title": "Ataşehir Lake Mutfak Dönüşümü",
        "slug": "atasehir-lake-mutfak-donusumu",
        "description": "Ataşehir'deki müşterimizin 15 yıllık sararmış meşe kaplama mutfağını, kırmadan dökmeden 5 gün içinde 'Sessiz Beyaz' (Ral 9003) rengine dönüştürdük. Kulplar modern siyah mat kulplarla değiştirildi ve menteşeler frenli sisteme geçirildi.",
        "location": "Ataşehir, İstanbul",
        "category": "Mobilya Boya ve Renk Değişimi",
        "service_slug": "mutfak-dolabi-boyama-renk-degisimi",
        "images": {
            "main": "uploads/projects/project_kitchen_main.jpg",
            "before": "uploads/projects/project_kitchen_before.jpg",
            "after": "uploads/projects/project_kitchen_after.jpg"
        },
        "is_featured": True
    },
    {
        "title": "Bağdat Caddesi Komple Daire Renovasyonu",
        "slug": "bagdat-caddesi-komple-daire-renovasyonu",
        "description": "Bağdat Caddesi'ndeki 3+1 dairenin banyo, zemin, boya ve elektrik tesisatı dahil olmak üzere A'dan Z'ye anahtar teslim tadilatı. Modern, minimalist ve ferah bir yaşam alanı tasarlandı. Mutfak ve salon birleştirilerek açık plan konsepti uygulandı.",
        "location": "Kadıköy, İstanbul",
        "category": "Tamirat, Tadilat ve Dekorasyon",
        "service_slug": "ev-ici-genel-dekorasyon",
        "images": {
            "main": "uploads/projects/project_renovation_main.jpg",
            "before": "uploads/projects/project_renovation_before.jpg",
            "after": "uploads/projects/project_renovation_after.jpg"
        },
        "is_featured": True
    },
    {
        "title": "Suadiye Balıksırtı Parke Uygulaması",
        "slug": "suadiye-baliksirti-parke-uygulamasi",
        "description": "Suadiye'deki bir villanın salon ve koridor zeminlerine, mekanın klasik ruhuna uygun olarak 'Meşe' rengi Balıksırtı (Herringbone) parke uygulaması yaptık. Şilte üzeri yüzer sistem döşeme ile ısı ve ses yalıtımı sağlandı.",
        "location": "Suadiye, İstanbul",
        "category": "Zemin ve Parke Sistemleri",
        "service_slug": "parke-kurulumu-renk-cesitleri",
        "images": {
            "main": "uploads/projects/project_flooring_main.jpg",
            "before": "uploads/projects/project_flooring_before.jpg",
            "after": "uploads/projects/project_flooring_after.jpg"
        },
        "is_featured": True
    },
    {
        "title": "Çekmeköy Villa Banyo Yenileme",
        "slug": "cekmekoy-villa-banyo-yenileme",
        "description": "20 yıllık eski fayansları ve küveti sökerek, yerine duşakabin, gömme rezervuar ve 60x120 granit seramik uygulaması yaptık. Banyo dolabı, özel ölçü olarak neme dayanıklı lake malzemeden üretildi.",
        "location": "Çekmeköy, İstanbul",
        "category": "Tamirat, Tadilat ve Dekorasyon",
        "service_slug": "ev-ici-genel-dekorasyon",
        "images": {
            "main": "uploads/projects/project_bathroom_main.jpg",
            "before": "uploads/projects/project_bathroom_before.jpg",
            "after": "uploads/projects/project_bathroom_after.jpg"
        },
        "is_featured": False
    },
    {
        "title": "Beşiktaş Yatak Odası Boyama",
        "slug": "besiktas-yatak-odasi-boyama",
        "description": "Koyu ceviz rengindeki yatak odası takımını, müşterimizin isteği üzerine 'Antik Beyaz' rengine boyadık. Yatak başlığı kumaş değişimi yapıldı ve gardırop içine sensörlü LED aydınlatma eklendi.",
        "location": "Beşiktaş, İstanbul",
        "category": "Mobilya Boya ve Renk Değişimi",
        "service_slug": "yatak-odasi-mobilya-boyama",
        "images": {
            "main": "uploads/projects/project_bedroom_main.jpg",
            "before": "uploads/projects/project_bedroom_before.jpg",
            "after": "uploads/projects/project_bedroom_after.jpg"
        },
        "is_featured": False
    },
    {
        "title": "Kadıköy Ofis Zemin Yenileme",
        "slug": "kadikoy-ofis-zemin-yenileme",
        "description": "Eski ve lekeli halıflex kaplamayı sökerek, yerine yoğun trafiğe dayanıklı 33. Sınıf (AC5) derzli laminant parke döşedik. Süpürgelikler 10cm antrasit lake olarak tercih edildi. Ofis ortamı modern bir görünüme kavuştu.",
        "location": "Kadıköy, İstanbul",
        "category": "Zemin ve Parke Sistemleri",
        "service_slug": "laminant-parke-doseme",
        "images": {
            "main": "uploads/projects/project_office_flooring_main.jpg",
            "before": "uploads/projects/project_office_flooring_before.jpg",
            "after": "uploads/projects/project_office_flooring_after.jpg"
        },
        "is_featured": False
    }
]

def turkish_slugify(text: str) -> str:
    """Türkçe karakterleri destekleyen slug üretici."""
    tr_chars = {'ı': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g', 'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's', 'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c'}
    for tr_char, en_char in tr_chars.items():
        text = text.replace(tr_char, en_char)
    return slugify(text)

class Command(BaseCommand):
    help = 'Gerçekçi proje verilerini yükler.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Mevcut projeleri siler.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n' + '=' * 60))
        self.stdout.write(self.style.WARNING('  EB DEKORASYON - PROJE YÜKLEME'))
        self.stdout.write(self.style.WARNING('=' * 60 + '\n'))

        if options['clear']:
            self.stdout.write(self.style.WARNING('⚠️  Tüm projeler siliniyor...'))
            Project.objects.all().delete()

        count = 0
        for p_data in PROJECTS_DATA:
            # İlgili hizmeti bul
            service = None
            if p_data.get('service_slug'):
                try:
                    service = Service.objects.get(slug=p_data['service_slug'])
                except Service.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Hizmet bulunamadı: {p_data['service_slug']}"))
            
            # Proje oluştur
            project, created = Project.objects.update_or_create(
                slug=p_data['slug'],
                defaults={
                    'title': p_data['title'],
                    'description': p_data['description'],
                    'location': p_data['location'],
                    'category': p_data['category'], # CharField, şablondaki filtrelerle eşleşmeli
                    'service': service,
                    'image': p_data['images']['main'],
                    'before_image': p_data['images']['before'],
                    'after_image': p_data['images']['after'],
                    'is_featured': p_data['is_featured'],
                    'is_active': True,
                    'show_on_index': True
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ YENİ PROJE: {project.title}'))
            else:
                self.stdout.write(self.style.HTTP_INFO(f'  → GÜNCELLENDİ: {project.title}'))
            count += 1

        self.stdout.write(self.style.SUCCESS(f'\nTopam {count} proje işlendi.\n'))
