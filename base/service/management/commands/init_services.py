"""
Django Management Command: init_services
=========================================
EB Dekorasyon hizmet verilerini veritabanına yükler.

Kullanım:
    python manage.py init_services

Veri Yapısı Örneği (SERVICES_DATA):
    [
        {
            "category_name": "Mobilya Boya ve Renk Değişimi",
            "services": [
                {
                    "title": "Mutfak Dolabı Boyama ve Renk Değişimi",
                    "slug": "mutfak-dolabi-boyama-renk-degisimi",  # Opsiyonel
                    "seo_title": "Eski Mutfak Dolabı Boyama...",  # Opsiyonel
                    "seo_description": "Mutfak dolaplarınızı...",  # Opsiyonel
                    "focus_keywords": ["mutfak dolabı boyama", ...],  # Opsiyonel
                    "short_description": "Kısa açıklama...",  # Opsiyonel
                    "description": "<p>HTML içerik</p>",  # Opsiyonel
                    "icon": "fas fa-paint-brush",  # Opsiyonel
                    "custom_features": ["Özellik 1", "Özellik 2"],  # Opsiyonel
                    "steps": [  # Opsiyonel
                        {"title": "Keşif", "description": "Ücretsiz keşif..."},
                    ],
                    "faqs": [  # Opsiyonel
                        {"question": "Soru?", "answer": "Cevap."},
                    ]
                },
            ]
        },
    ]
"""

import re
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from service.models import ServiceCategory, Service, ServiceStep
from core.models import Feature, Faq


# =============================================================================
# PRODUCTION VERİ SETİ
# =============================================================================
SERVICES_DATA = [
    {
        "category_name": "Mobilya Boya ve Renk Değişimi",
        "icon": "fas fa-palette",
        "services": [
            {
                "title": "Mutfak Dolabı Boyama ve Renk Değişimi",
                "slug": "mutfak-dolabi-boyama-renk-degisimi",
                "image": "uploads/services/mutfak-dolabi-boyama-yeni.jpg",
                "seo_title": "Eski Mutfak Dolabı Boyama ve Yenileme | Kırmadan Renk Değişimi",
                "seo_description": "Mutfak dolaplarınızı değiştirmeden yeniliyoruz. Lake, akrilik veya mat boya seçenekleriyle mutfak dolabı renk değişimi hizmeti.",
                "focus_keywords": ["mutfak dolabı boyama", "dolap renk değişimi", "eski mutfak yenileme", "lake boya mutfak"],
                "icon": "fas fa-utensils",
                "short_description": "Mutfak dolaplarınızı değiştirmeden, lake veya mat boya ile istediğiniz renge dönüştürüyoruz. Ekonomik ve hızlı çözüm.",
                "description": """
                    <h2>Mutfak Dolabı Boyama Hizmeti</h2>
                    <p>Eski mutfak dolaplarınızı değiştirmeye gerek yok! Profesyonel ekibimiz ile mutfak dolaplarınızı istediğiniz renge boyuyoruz. Lake, akrilik veya mat boya seçenekleri ile mutfağınıza yepyeni bir görünüm kazandırın.</p>
                    
                    <h3>Neden Bizi Tercih Etmelisiniz?</h3>
                    <ul>
                        <li><strong>Ekonomik Çözüm:</strong> Dolap değiştirmekten %70'e varan tasarruf</li>
                        <li><strong>Hızlı Teslim:</strong> 3-5 iş günü içinde yepyeni mutfak</li>
                        <li><strong>Geniş Renk Paleti:</strong> RAL ve NCS renk kartelasından seçim</li>
                        <li><strong>2 Yıl Garanti:</strong> Tüm boyama işlemlerinde garanti</li>
                    </ul>
                    
                    <h3>Uygulama Süreci</h3>
                    <p>Kapaklar yerinde sökülerek atölyemize götürülür. Profesyonel boya kabininde boyanır ve kuruma sonrası tekrar monte edilir. Tüm süreç boyunca mutfağınızı kullanmaya devam edebilirsiniz.</p>
                """,
                "custom_features": ["Lake Boya", "Mat Boya", "Akrilik Boya", "RAL Renk Seçeneği"],
                "steps": [
                    {"step_number": 1, "title": "Ücretsiz Keşif", "description": "Uzman ekibimiz evinize gelerek dolapları inceler ve size en uygun renk önerilerini sunar."},
                    {"step_number": 2, "title": "Kapak Sökümü", "description": "Dolap kapakları dikkatle sökülür ve koruyucu ambalajla atölyemize taşınır."},
                    {"step_number": 3, "title": "Zımparalama ve Astar", "description": "Yüzeyler titizlikle zımparalanır, boya tutunumu için özel astar uygulanır."},
                    {"step_number": 4, "title": "Boyama İşlemi", "description": "Profesyonel boya kabininde 2 kat boya uygulaması yapılır."},
                    {"step_number": 5, "title": "Montaj ve Teslim", "description": "Kuruyan kapaklar yerine monte edilir ve temizlik yapılarak teslim edilir."}
                ],
                "faqs": [
                    {"question": "Mutfak dolabı boyama ne kadar sürer?", "answer": "Standart bir mutfak için tüm süreç 3-5 iş günü içinde tamamlanır. Bu süre dolap sayısına göre değişebilir."},
                    {"question": "Boyama işlemi sırasında mutfağımı kullanabilir miyim?", "answer": "Evet, kapaklar atölyemizde boyandığı için sadece kapaksız şekilde mutfağınızı kullanmaya devam edebilirsiniz."},
                    {"question": "Hangi boya türlerini kullanıyorsunuz?", "answer": "Lake, akrilik ve mat boya seçeneklerimiz mevcuttur. Tüm boyalarımız leke tutmayan ve silinebilir özelliğe sahiptir."}
                ]
            },
            {
                "title": "Mobilya ve Ahşap Kapı Boyama",
                "slug": "mobilya-ve-ahsap-kapi-boyama",
                "image": "uploads/services/ahsap-kapi-boyama.jpg",
                "seo_title": "Amerikan ve Ahşap Kapı Boyama | Mobilya Cilalama",
                "seo_description": "Evinizdeki ahşap kapıları ve mobilyaları istediğiniz renge dönüştürüyoruz. Amerikan kapı boyama ve mobilya cila işlemleri.",
                "focus_keywords": ["kapı boyama fiyatları", "amerikan kapı boyama", "mobilya boyama", "ahşap kapı yenileme"],
                "icon": "fas fa-door-open",
                "short_description": "Amerikan kapılarınızı ve ahşap mobilyalarınızı profesyonel boyama ile yeniliyoruz. İstediğiniz renk ve finişte.",
                "description": """
                    <h2>Ahşap Kapı ve Mobilya Boyama</h2>
                    <p>Evinizdeki amerikan kapılar ve ahşap mobilyalar zamanla eskir ve soluklaşır. Değiştirmek yerine boyama ile onlara ikinci bir hayat verin!</p>
                    
                    <h3>Hizmet Kapsamı</h3>
                    <ul>
                        <li>Amerikan kapı boyama (iç ve dış yüzey)</li>
                        <li>Ahşap panel kapı boyama</li>
                        <li>Gardırop ve şifonyer boyama</li>
                        <li>Komodin ve sehpa boyama</li>
                        <li>Mobilya cilalama ve vernik işlemi</li>
                    </ul>
                    
                    <h3>Kullandığımız Teknikler</h3>
                    <p>Sprey boya tekniği ile pürüzsüz bir yüzey elde ediyoruz. Fırça izi veya boya kabarcığı oluşmaz. Tüm işlemler atölyemizde kontrollü ortamda yapılır.</p>
                """,
                "custom_features": ["Sprey Boya Tekniği", "Cila ve Vernik", "Renk Değişimi", "Antika Görünüm"],
            },
            {
                "title": "Sandalye ve Masa Boyama",
                "slug": "sandalye-ve-masa-boyama-yenileme",
                "image": "uploads/services/sandalye-masa-boyama.jpg",
                "seo_title": "Yemek Masası ve Sandalye Boyama | Cila ve Yenileme",
                "seo_description": "Eskiyen masa ve sandalyelerinizi atmayın, yenileyelim. Yemek odası takımları için profesyonel boya ve cila hizmeti.",
                "focus_keywords": ["masa boyama", "sandalye boyama", "mobilya geri dönüşüm", "masa sandalye yenileme"],
                "icon": "fas fa-chair",
                "short_description": "Yemek masası ve sandalyelerinizi yeniden canlandırıyoruz. Cila, boya ve döşeme değişimi ile komple yenileme.",
                "description": """
                    <h2>Masa ve Sandalye Yenileme Hizmeti</h2>
                    <p>Değerli yemek odası takımlarınızı atmayın! Profesyonel ekibimiz ile masa ve sandalyelerinizi yepyeni hale getiriyoruz.</p>
                    
                    <h3>Sunduğumuz Hizmetler</h3>
                    <ul>
                        <li><strong>Komple Boyama:</strong> İstediğiniz renkte boyama</li>
                        <li><strong>Cila Yenileme:</strong> Ahşap görünümü koruyarak cila</li>
                        <li><strong>Döşeme Değişimi:</strong> Sandalye kumaş ve sünger değişimi</li>
                        <li><strong>Tamir:</strong> Sallanma ve kırık onarımı</li>
                    </ul>
                """,
            },
            {
                "title": "Döşeme Yüzü Değişimi",
                "slug": "mobilya-doseme-yuzu-degisimi",
                "image": "uploads/services/doseme-degisimi.jpg",
                "seo_title": "Koltuk ve Sandalye Döşeme Yüzü Değişimi",
                "seo_description": "Mobilyalarınızın kumaş ve süngerlerini yeniliyoruz. Sandalye, koltuk ve berjer döşeme yüzü değişimi ile yepyeni görünüm.",
                "focus_keywords": ["koltuk döşeme", "sandalye kılıfı değişimi", "mobilya kumaş değişimi", "döşemelik kumaş"],
                "icon": "fas fa-couch",
                "short_description": "Koltuk, sandalye ve berjer döşemelerinizi değiştiriyoruz. Geniş kumaş seçenekleri ile zevkinize uygun döşeme.",
                "description": """
                    <h2>Döşeme Yüzü Değişimi</h2>
                    <p>Mobilyalarınızın iskeleti sağlam ama kumaşı eskidi mi? Döşeme yüzü değişimi ile mobilyalarınıza yeni bir hayat verin.</p>
                    
                    <h3>Değiştirdiğimiz Döşemeler</h3>
                    <ul>
                        <li>Koltuk takımı döşemesi</li>
                        <li>Sandalye oturma kısmı</li>
                        <li>Berjer ve tekli koltuk</li>
                        <li>Yatak başlığı döşemesi</li>
                        <li>Puf ve ottoman kaplama</li>
                    </ul>
                    
                    <h3>Kumaş Seçenekleri</h3>
                    <p>Kadife, keten, deri ve microfiber gibi geniş kumaş seçeneklerimiz mevcuttur. Leke tutmayan ve kolay temizlenen kumaşlar önerilir.</p>
                """,
            },
            {
                "title": "Yatak Odası Mobilya Boyama",
                "slug": "yatak-odasi-mobilya-boyama",
                "image": "uploads/services/yatak-odasi-boyama-yeni.jpg",
                "seo_title": "Yatak Odası Takımı Boyama ve Renk Değişimi",
                "seo_description": "Gardırop, şifonyer ve başlıklarınızı istediğiniz renge boyuyoruz. Yatak odası mobilya yenileme ve renk değişimi.",
                "focus_keywords": ["yatak odası boyama", "gardırop boyama", "mobilya renk değiştirme", "yatak başlığı yenileme"],
                "icon": "fas fa-bed",
                "short_description": "Yatak odası takımınızı komple yeniliyoruz. Gardırop, şifonyer, komodin ve başlık boyama hizmeti.",
                "description": """
                    <h2>Yatak Odası Mobilya Boyama</h2>
                    <p>Yatak odanızı yenilemek için tüm takımı değiştirmenize gerek yok. Boyama ile aynı etkiyi çok daha ekonomik fiyata alın.</p>
                    
                    <h3>Boyama Yapılan Parçalar</h3>
                    <ul>
                        <li>Gardırop (sürgülü ve kapaklı)</li>
                        <li>Şifonyer ve çekmeceli dolap</li>
                        <li>Komodin</li>
                        <li>Yatak başlığı ve karyola</li>
                        <li>Makyaj masası ve ayna çerçevesi</li>
                    </ul>
                """,
            }
        ]
    },
    {
        "category_name": "Tamirat, Tadilat ve Dekorasyon",
        "icon": "fas fa-tools",
        "services": [
            {
                "title": "Mutfak Tezgahı Değişimi ve Tamiri",
                "slug": "mutfak-tezgahi-degisimi-tamiri",
                "image": "uploads/services/mutfak-tezgahi.jpg",
                "seo_title": "Mutfak Tezgahı Yenileme ve Tamiratı | Granit & Mermerit",
                "seo_description": "Çizilen, kırılan veya eskiyen mutfak tezgahınızı yenisiyle değiştiriyoruz veya tamir ediyoruz. Tezgah arası ve tezgah çözümleri.",
                "focus_keywords": ["mutfak tezgahı değiştirme", "tezgah tamiri", "mutfak tezgah modelleri", "tezgah yenileme"],
                "icon": "fas fa-sink",
                "short_description": "Mutfak tezgahı değişimi ve tamiri. Granit, mermerit ve kompakt lam tezgah seçenekleri.",
                "description": """
                    <h2>Mutfak Tezgahı Değişimi</h2>
                    <p>Çizilen, leke tutan veya kırılan mutfak tezgahınızı yenisiyle değiştiriyoruz. Ölçüye özel üretim ve montaj hizmeti.</p>
                    
                    <h3>Tezgah Türleri</h3>
                    <ul>
                        <li><strong>Granit Tezgah:</strong> Doğal taş görünümü, yüksek dayanıklılık</li>
                        <li><strong>Mermerit Tezgah:</strong> Ekonomik ve şık çözüm</li>
                        <li><strong>Kompakt Lam:</strong> Leke tutmayan, hijyenik</li>
                        <li><strong>Corian:</strong> Derziz görünüm, modern tasarım</li>
                    </ul>
                    
                    <h3>Tezgah Arası Çözümleri</h3>
                    <p>Tezgah arası cam panel, fayans veya kompakt lam uygulaması da yapılmaktadır.</p>
                """,
                "custom_features": ["Granit Tezgah", "Mermerit Tezgah", "Tezgah Arası Cam", "Kompakt Lam"],
            },
            {
                "title": "TV Ünitesi ve Duvar Dekorasyonu",
                "slug": "tv-unitesi-ve-duvar-dekorasyonu",
                "image": "uploads/services/tv-unitesi-dekor.jpg",
                "seo_title": "TV Arkası Duvar Dekorasyonu ve Ünite Tasarımı",
                "seo_description": "Salonunuzun havasını değiştirin. Özel tasarım TV ünitesi, çıtalama ve TV arkası duvar dekorasyon uygulamaları.",
                "focus_keywords": ["tv ünitesi modelleri", "tv arkası dekor", "duvar çıtalama", "tv duvar dekorasyonu"],
                "icon": "fas fa-tv",
                "short_description": "TV ünitesi tasarımı ve duvar dekorasyonu. Çıtalama, LED aydınlatma ve özel tasarım üniteler.",
                "description": """
                    <h2>TV Ünitesi ve Duvar Dekorasyonu</h2>
                    <p>Salonunuzun odak noktası olan TV alanını profesyonelce tasarlıyoruz. Özel üretim TV üniteleri ve dekoratif duvar panelleri.</p>
                    
                    <h3>Uygulama Seçenekleri</h3>
                    <ul>
                        <li>Özel tasarım TV ünitesi</li>
                        <li>Duvar çıtalama (ahşap ve MDF)</li>
                        <li>LED şerit aydınlatma</li>
                        <li>Dekoratif duvar paneli</li>
                        <li>Şömine görünümlü TV ünitesi</li>
                    </ul>
                """,
            },
            {
                "title": "Kafe İçi Dekorasyon ve Tasarım",
                "slug": "kafe-ici-dekorasyon-tasarim",
                "image": "uploads/services/kafe-dekorasyon.jpg",
                "seo_title": "Anahtar Teslim Kafe ve Restoran Dekorasyonu",
                "seo_description": "İşletmeniz için modern ve müşteri çeken tasarımlar. Kafe içi mobilya, duvar ve konsept dekorasyon uygulamaları.",
                "focus_keywords": ["kafe dekorasyonu", "kafe iç mimari", "restoran tasarımı", "konsept kafe dizaynı"],
                "icon": "fas fa-coffee",
                "short_description": "Kafe ve restoran dekorasyonu. Konsept tasarım, mobilya üretimi ve anahtar teslim uygulama.",
                "description": """
                    <h2>Kafe ve Restoran Dekorasyonu</h2>
                    <p>İşletmenizi müşteri çeken bir mekana dönüştürüyoruz. Konsept tasarımdan uygulamaya kadar anahtar teslim hizmet.</p>
                    
                    <h3>Hizmet Kapsamı</h3>
                    <ul>
                        <li>Konsept tasarım ve 3D görselleştirme</li>
                        <li>Özel üretim masa ve sandalye</li>
                        <li>Bar tezgahı ve vitrin</li>
                        <li>Duvar paneli ve aydınlatma</li>
                        <li>Tabela ve branding çalışması</li>
                    </ul>
                """,
                "custom_features": ["3D Tasarım", "Anahtar Teslim", "Özel Üretim Mobilya", "Branding"],
            },
            {
                "title": "Mobilya Tamiratı ve Bakımı",
                "slug": "mobilya-tamirati-ve-bakimi",
                "image": "uploads/services/mobilya-tamir.jpg",
                "seo_title": "Yerinde Mobilya Tamiratı ve Montaj Hizmeti",
                "seo_description": "Kırılan menteşeler, raylar veya ahşap parçalar için tamirat hizmeti. Her türlü mobilya tamiri ve bakımı yapılır.",
                "focus_keywords": ["mobilya tamiri", "dolap tamiri", "ray değişimi", "mobilya ustası"],
                "icon": "fas fa-wrench",
                "short_description": "Mobilya tamiri ve bakımı. Menteşe, ray değişimi, ahşap onarımı ve montaj hizmetleri.",
                "description": """
                    <h2>Mobilya Tamiratı Hizmeti</h2>
                    <p>Kırılan, bozulan veya işlevini yitiren mobilyalarınızı tamir ediyoruz. Yerinde veya atölyede servis.</p>
                    
                    <h3>Tamir Hizmetlerimiz</h3>
                    <ul>
                        <li>Menteşe ve ray değişimi</li>
                        <li>Kapak ayarı ve montajı</li>
                        <li>Ahşap kırık onarımı</li>
                        <li>Çizik ve leke giderme</li>
                        <li>Kilit ve kulp değişimi</li>
                        <li>Mobilya demontaj ve montaj</li>
                    </ul>
                """,
            },
            {
                "title": "Ev İçi Genel Dekorasyon",
                "slug": "ev-ici-genel-dekorasyon",
                "image": "uploads/services/ev-dekorasyon.jpg",
                "seo_title": "Ev İçi Dekorasyon ve Tadilat Çözümleri",
                "seo_description": "Evinizin tüm alanları için dekoratif çözümler. Koridor, antre ve oda dekorasyonları ile yaşam alanınızı güzelleştirin.",
                "focus_keywords": ["ev dekorasyonu", "iç mimari dekorasyon", "ev yenileme fikirleri", "modern ev tasarımı"],
                "icon": "fas fa-home",
                "short_description": "Ev içi dekorasyon çözümleri. Salon, yatak odası, koridor ve antre için özel tasarımlar.",
                "description": """
                    <h2>Ev İçi Dekorasyon</h2>
                    <p>Evinizin her köşesini sizin için tasarlıyoruz. Modern, şık ve fonksiyonel dekorasyon çözümleri.</p>
                    
                    <h3>Uygulama Alanları</h3>
                    <ul>
                        <li>Salon ve oturma odası dekorasyonu</li>
                        <li>Yatak odası tasarımı</li>
                        <li>Antre ve koridor düzenlemesi</li>
                        <li>Çocuk odası tasarımı</li>
                        <li>Banyo dekorasyonu</li>
                    </ul>
                """,
            }
        ]
    },
    {
        "category_name": "Zemin ve Parke Sistemleri",
        "icon": "fas fa-layer-group",
        "services": [
            {
                "title": "Laminant Parke Döşeme",
                "slug": "laminant-parke-doseme",
                "image": "uploads/services/laminant-parke.jpg",
                "seo_title": "Laminant Parke Döşeme ve Tamiratı | Tüm Renkler",
                "seo_description": "Evinizin zeminini baştan yaratın. Geniş renk seçenekleriyle kaliteli laminant parke satışı ve montajı.",
                "focus_keywords": ["parke döşeme", "laminant parke fiyatları", "zemin kaplama", "parke ustası"],
                "icon": "fas fa-th-large",
                "short_description": "Laminant parke satış ve döşeme. AC3, AC4 ve AC5 sınıflarında geniş renk ve desen seçenekleri.",
                "description": """
                    <h2>Laminant Parke Döşeme</h2>
                    <p>Evinizin zeminini yeniden tasarlıyoruz. Kaliteli ve dayanıklı laminant parke çözümleri.</p>
                    
                    <h3>Parke Özellikleri</h3>
                    <ul>
                        <li><strong>AC3:</strong> Ev kullanımı için ekonomik seçenek</li>
                        <li><strong>AC4:</strong> Yoğun ev kullanımı ve hafif ticari alan</li>
                        <li><strong>AC5:</strong> Ticari alanlar için yüksek dayanıklılık</li>
                    </ul>
                    
                    <h3>Uygulama Süreci</h3>
                    <ol>
                        <li>Zemin hazırlığı ve tesviye</li>
                        <li>Nem bariyeri serilmesi</li>
                        <li>Parke döşeme</li>
                        <li>Süpürgelik montajı</li>
                        <li>Eşik profili uygulaması</li>
                    </ol>
                """,
                "custom_features": ["AC3-AC5 Kalite", "Suya Dayanıklı Seçenekler", "Geniş Renk Paleti", "10 Yıl Garanti"],
            },
            {
                "title": "Parke Kurulumu ve Renk Çeşitleri",
                "slug": "parke-kurulumu-renk-cesitleri",
                "image": "uploads/services/parke-renkleri.jpg",
                "seo_title": "İsteğe Göre Parke Kurulumu ve Renk Seçenekleri",
                "seo_description": "Tüm parke renkleri mevcuttur. İsteğinize uygun renk ve modelde profesyonel parke kurulum hizmeti.",
                "focus_keywords": ["parke renkleri", "derzli parke", "suya dayanıklı parke", "parke montajı"],
                "icon": "fas fa-palette",
                "short_description": "İsteğinize uygun parke rengi ve deseni. Meşe, ceviz, kayın ve gri tonlarında seçenekler.",
                "description": """
                    <h2>Parke Renk Seçenekleri</h2>
                    <p>Evinizin dekorasyonuna uygun parke rengini birlikte seçelim. Numune gösterimi ve danışmanlık hizmeti.</p>
                    
                    <h3>Popüler Renkler</h3>
                    <ul>
                        <li><strong>Meşe Tonları:</strong> Açık meşe, koyu meşe, doğal meşe</li>
                        <li><strong>Ceviz Tonları:</strong> Amerikan ceviz, Anadolu cevizi</li>
                        <li><strong>Gri Tonlar:</strong> Açık gri, koyu gri, beton görünüm</li>
                        <li><strong>Beyaz Tonlar:</strong> Akçaağaç, beyazlatılmış meşe</li>
                    </ul>
                    
                    <h3>Özel Talepler</h3>
                    <p>Balıksırtı (herringbone) ve kare parke döşeme de yapılmaktadır. Özel desen talepleri için iletişime geçin.</p>
                """,
            }
        ]
    }
]

# =============================================================================
# VARSAYILAN DEĞERLER
# =============================================================================
DEFAULT_FEATURES = ["Ücretsiz Keşif", "2 Yıl Garanti", "Zamanında Teslim", "Profesyonel Ekip"]

DEFAULT_STEPS = [
    {"step_number": 1, "title": "Ücretsiz Keşif", "description": "Uzman ekibimiz evinize gelerek ihtiyacınızı yerinde değerlendirir ve size en uygun çözümü sunar."},
    {"step_number": 2, "title": "Teklif ve Planlama", "description": "Detaylı fiyat teklifi hazırlanır, renk ve malzeme seçimi yapılır, iş planı oluşturulur."},
    {"step_number": 3, "title": "Uygulama", "description": "Profesyonel ekibimiz işi titizlikle gerçekleştirir. Tüm süreç boyunca bilgilendirilirsiniz."},
    {"step_number": 4, "title": "Kontrol ve Teslim", "description": "İş tamamlandığında birlikte kontrol edilir, temizlik yapılarak teslim edilir."}
]


def turkish_slugify(text: str) -> str:
    """Türkçe karakterleri destekleyen slug üretici."""
    # Türkçe karakter dönüşümleri
    tr_chars = {
        'ı': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's',
        'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c'
    }
    for tr_char, en_char in tr_chars.items():
        text = text.replace(tr_char, en_char)
    return slugify(text)


class Command(BaseCommand):
    help = 'EB Dekorasyon hizmet verilerini veritabanına yükler.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Mevcut tüm hizmet verilerini siler ve yeniden oluşturur.',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n' + '=' * 60))
        self.stdout.write(self.style.WARNING('  EB DEKORASYON - HİZMET VERİLERİ YÜKLEME'))
        self.stdout.write(self.style.WARNING('=' * 60 + '\n'))

        if options['clear']:
            self.clear_existing_data()

        categories_created = 0
        services_created = 0
        services_updated = 0
        features_created = 0
        steps_created = 0
        faqs_created = 0

        for category_data in SERVICES_DATA:
            # 1. Kategori oluştur
            category_name = category_data['category_name']
            category_icon = category_data.get('icon', 'fas fa-cog')
            category_slug = turkish_slugify(category_name)

            category, cat_created = ServiceCategory.objects.get_or_create(
                slug=category_slug,
                defaults={
                    'name': category_name,
                    'icon': category_icon,
                    'is_active': True
                }
            )

            if cat_created:
                categories_created += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Kategori oluşturuldu: {category_name}'))
            else:
                self.stdout.write(self.style.HTTP_INFO(f'  → Kategori mevcut: {category_name}'))

            # 2. Kategorideki hizmetleri oluştur
            for service_data in category_data.get('services', []):
                result = self.create_service(category, service_data)
                
                if result['created']:
                    services_created += 1
                else:
                    services_updated += 1
                
                features_created += result['features_created']
                steps_created += result['steps_created']
                faqs_created += result['faqs_created']

        # Sonuç özeti
        self.stdout.write('\n' + '-' * 60)
        self.stdout.write(self.style.SUCCESS('\n📊 YÜKLEME SONUÇLARI:'))
        self.stdout.write(f'   • Kategoriler: {categories_created} yeni')
        self.stdout.write(f'   • Hizmetler: {services_created} yeni, {services_updated} güncellendi')
        self.stdout.write(f'   • Özellikler: {features_created} yeni')
        self.stdout.write(f'   • Adımlar: {steps_created} yeni')
        self.stdout.write(f'   • SSS: {faqs_created} yeni')
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ VERİ YÜKLEME TAMAMLANDI!'))
        self.stdout.write('=' * 60 + '\n')

    def create_service(self, category, data: dict) -> dict:
        """Hizmet oluşturur ve ilişkili verileri ekler."""
        result = {
            'created': False,
            'features_created': 0,
            'steps_created': 0,
            'faqs_created': 0
        }

        title = data['title']
        slug = data.get('slug') or turkish_slugify(title)

        # SEO alanları (veritabanı limitlerine göre kırp: seo_title max 60, seo_description max 160)
        seo_title = data.get('seo_title') or f"{title} Hizmeti | EB Dekorasyon"
        seo_title = seo_title[:60]  # Veritabanı limiti
        
        seo_description = data.get('seo_description') or f"{title} için profesyonel çözümler. Modoko/Ümraniye bölgesinde garantili hizmet."
        seo_description = seo_description[:160]  # Veritabanı limiti
        
        # Focus keywords
        focus_keywords = data.get('focus_keywords', [])
        if isinstance(focus_keywords, list):
            focus_keywords_str = ', '.join(focus_keywords)
        else:
            focus_keywords_str = focus_keywords or turkish_slugify(title).replace('-', ', ')

        # Açıklamalar
        short_description = data.get('short_description') or f"{title} hizmeti için profesyonel çözümler sunuyoruz."
        description = data.get('description') or self.generate_default_description(title)
        
        # Icon ve Image
        icon = data.get('icon', 'fas fa-cog')
        image = data.get('image', 'uploads/services/service_default.jpg')

        # Hizmeti oluştur veya güncelle
        service, created = Service.objects.get_or_create(
            slug=slug,
            defaults={
                'category': category,
                'title': title,
                'seo_title': seo_title,
                'seo_description': seo_description,
                'short_description': short_description,
                'description': description,
                'icon': icon,
                'image': image,
                'isActive': True,
                'showIndex': True
            }
        )

        result['created'] = created

        if created:
            self.stdout.write(self.style.SUCCESS(f'      ✓ Hizmet oluşturuldu: {title}'))
        else:
            # Güncelle
            service.category = category
            service.seo_title = seo_title
            service.seo_description = seo_description
            service.short_description = short_description
            service.description = description
            service.icon = icon
            service.image = image
            service.save()
            self.stdout.write(self.style.HTTP_INFO(f'      → Hizmet güncellendi: {title}'))

        # 3. Özellikler ekle
        result['features_created'] = self.add_features(service, data.get('custom_features', DEFAULT_FEATURES))

        # 4. Adımlar ekle
        result['steps_created'] = self.add_steps(service, data.get('steps', DEFAULT_STEPS))

        # 5. SSS ekle
        if 'faqs' in data:
            result['faqs_created'] = self.add_faqs(service, data['faqs'])

        return result

    def add_features(self, service, feature_names: list) -> int:
        """Hizmete özellikleri ekler."""
        created_count = 0
        for feature_name in feature_names:
            feature, created = Feature.objects.get_or_create(
                name=feature_name,
                defaults={
                    'description': f'{feature_name} hizmetimizin bir parçasıdır.',
                    'icon': 'fas fa-check-circle'
                }
            )
            service.features.add(feature)
            if created:
                created_count += 1
        return created_count

    def add_steps(self, service, steps_data: list) -> int:
        """Hizmete süreç adımlarını ekler."""
        # Mevcut adımları temizle
        ServiceStep.objects.filter(service=service).delete()
        
        created_count = 0
        for step_data in steps_data:
            ServiceStep.objects.create(
                service=service,
                step_number=step_data.get('step_number', created_count + 1),
                title=step_data['title'],
                description=step_data['description']
            )
            created_count += 1
        return created_count

    def add_faqs(self, service, faqs_data: list) -> int:
        """Hizmete SSS'leri ekler."""
        created_count = 0
        for faq_data in faqs_data:
            faq, created = Faq.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'isActive': True,
                    'showIndex': False
                }
            )
            service.faqs.add(faq)
            if created:
                created_count += 1
        return created_count

    def generate_default_description(self, title: str) -> str:
        """Varsayılan HTML açıklama üretir."""
        return f"""
            <h2>{title}</h2>
            <p>{title} hizmetimiz ile profesyonel çözümler sunuyoruz. Deneyimli ekibimiz ve kaliteli malzemelerimizle işinizi en iyi şekilde gerçekleştiriyoruz.</p>
            
            <h3>Neden Bizi Tercih Etmelisiniz?</h3>
            <ul>
                <li><strong>Profesyonel Ekip:</strong> Alanında uzman kadromuz</li>
                <li><strong>Kaliteli Malzeme:</strong> En iyi markaları kullanıyoruz</li>
                <li><strong>Garanti:</strong> Tüm işlerimiz garantilidir</li>
                <li><strong>Uygun Fiyat:</strong> Rekabetçi fiyatlarla hizmet</li>
            </ul>
            
            <h3>Hizmet Bölgemiz</h3>
            <p>Modoko, Ümraniye ve tüm İstanbul genelinde hizmet vermekteyiz. Ücretsiz keşif için hemen arayın.</p>
        """

    def clear_existing_data(self):
        """Mevcut verileri temizler."""
        self.stdout.write(self.style.WARNING('⚠️  Mevcut veriler temizleniyor...'))
        
        ServiceStep.objects.all().delete()
        Service.objects.all().delete()
        ServiceCategory.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('   Veriler temizlendi.\n'))
