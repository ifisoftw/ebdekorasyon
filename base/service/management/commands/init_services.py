"""
Django Management Command: init_services
=========================================
EB Dekorasyon hizmet verilerini detaylı SEO içerikleriyle veritabanına yükler.
"""

import re
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from service.models import ServiceCategory, Service, ServiceStep
from core.models import Feature, Faq


# =============================================================================
# SEO & İÇERİK VERİ SETİ
# =============================================================================
SERVICES_DATA = [
    # -------------------------------------------------------------------------
    # KATEGORİ 1: Mobilya Boya ve Renk Değişimi
    # -------------------------------------------------------------------------
    {
        "category_name": "Mobilya Boya ve Renk Değişimi",
        "icon": "fas fa-palette",
        "services": [
            {
                "title": "Mutfak Dolabı Boyama ve Renk Değişimi",
                "slug": "mutfak-dolabi-boyama-renk-degisimi",
                "image": "uploads/services/mutfak-dolabi-boyama-yeni.jpg",
                "seo_title": "Mutfak Dolabı Boyama ve Renk Değişimi | %70 Tasarruf | EB Dekorasyon",
                "seo_description": "Eskiyen mutfağınızı kırmadan yeniliyoruz! İstanbul/Modoko profesyonel mutfak dolabı boyama hizmeti. Lake & mat seçenekler, 2 yıl garanti. Ücretsiz keşif.",
                "focus_keywords": ["mutfak dolabı boyama", "dolap renk değişimi", "lake mutfak boyama", "mutfak yenileme", "modoko mobilya boya"],
                "icon": "fas fa-brush",
                "short_description": "Mutfak dolaplarınızı değiştirmek yerine boyatarak %70 tasarruf edin. 3-5 günde, kırmadan dökmeden, fabrika kalitesinde lake veya mat boya ile yepyeni bir mutfağa kavuşun.",
                "description": """
                    <h2>Mutfak Dolabı Boyama Nedir?</h2>
                    <p>Mutfak dolabı boyama, mevcut sağlam dolap gövdelerinin ve kapaklarının korunarak, sadece yüzeylerinin profesyonel endüstriyel boyalarla (lake, akrilik, poliüretan) renginin değiştirilmesi işlemidir. Bu yöntem, komple mutfak tadilatına göre çok daha hızlı, ekonomik ve çevrecidir.</p>

                    <h3>Neden Mutfak Boyamayı Tercih Etmelisiniz?</h3>
                    <p>Mutfak dolaplarınızın işlevi hala yerindeyse ancak rengi demode olduysa veya sarardıysa, onları çöpe atmanıza gerek yok.</p>
                    <ul>
                        <li><strong>Ekonomik Çözüm:</strong> Yeni bir mutfak yaptırmanın maliyetinin %30'una mal olur.</li>
                        <li><strong>Hızlı Teslimat:</strong> İnşaat süreci yoktur. Ortalama 3-5 iş günü içinde tamamlanır.</li>
                        <li><strong>Kırmadan Dökmeden:</strong> Fayanslarınız, tezgahınız veya zeminine zarar gelmez.</li>
                        <li><strong>Sınırsız Renk Seçeneği:</strong> RAL ve NCS kartelasından dilediğiniz rengi seçebilirsiniz.</li>
                    </ul>

                    <h3>Kullandığımız Boya Teknolojileri</h3>
                    <p>Sıradan duvar boyaları değil, mobilya sanayisinde kullanılan özel sertleştiricili boyalar kullanıyoruz.</p>
                    <ul>
                        <li><strong>Lake Boya:</strong> Pürüzsüz, ipeksi dokunuş ve yüksek kalite.</li>
                        <li><strong>Akrilik Boya:</strong> Sararmaya karşı dirençli, uzun ömürlü.</li>
                        <li><strong>Mat ve İpek Mat:</strong> Modern ve parmak izi bırakmayan yüzeyler.</li>
                    </ul>
                """,
                "custom_features": ["Lake & Akrilik Boya", "Tozsuz Boya Kabini", "Renk Garantisi", "Ücretsiz Keşif", "Sararmazlık Garantisi"],
                "steps": [
                    {"step_number": 1, "title": "Ücretsiz Keşif ve Renk Seçimi", "description": "Ekibimiz mutfağınızı inceler, kapak yapısına (MDF, Masif, Kaplama) uygun boyayı belirler ve renk kartelasından seçim yapmanıza yardımcı olur."},
                    {"step_number": 2, "title": "Demontaj ve Numaralandırma", "description": "Kapaklar ve çekmeceler sökülür, numaralandırılır. Menteşeler korumaya alınır. Gövdeler için evinizde maskeleme yapılır."},
                    {"step_number": 3, "title": "Atölye Süreci (Zımpara & Astar)", "description": "Kapaklar atölyemize alınır. Yağ ve kirden arındırılır, zımparalanır ve boya tutuculuğunu artıran özel astar atılır."},
                    {"step_number": 4, "title": "Profesyonel Boyama", "description": "Tozsuz boya kabinimizde, pistole (sprey) tekniği ile son kat boya uygulanır. Fırça izi olmaz, fabrikasyon bitiş sağlanır."},
                    {"step_number": 5, "title": "Montaj ve Teslimat", "description": "Kuruyan kapaklar tekrar monte edilir, menteşe ayarları yapılır ve mutfağınız tertemiz teslim edilir."}
                ],
                "faqs": [
                    {"question": "Mutfak dolabı boyama işleminde koku olur mu?", "answer": "Kapaklar atölyede boyandığı için evinizde koku olmaz. Sadece gövdeler boyanırken minimal bir koku olabilir, ancak kullandığımız yeni nesil boyalar hızla havalanır."},
                    {"question": "Boya sonrası boya atması veya soyulma yaşar mıyım?", "answer": "Hayır. Doğru zımpara, kaliteli astar ve sertleştiricili son kat boya kullanıldığında boya yüzeye kemikleşir. İşçiliğimize 2 yıl garanti veriyoruz."},
                    {"question": "Boyama işlemi ne kadar sürer?", "answer": "Ortalama boyutta bir mutfak için süreç 3 ile 5 iş günü arasında tamamlanır."},
                    {"question": "Hangi yüzeyler boyanabilir?", "answer": "MDF, Ham Ahşap, Kaplama, Membran ve hatta uygun astar ile Laminat yüzeyler boyanabilir."},
                    {"question": "Renk seçeneği sınırlı mı?", "answer": "Hayır, RAL ve NCS kartelasındaki binlerce renk arasından seçim yapabilirsiniz. Renk sınırımız yoktur."}
                ]
            },
            {
                "title": "Mobilya ve Ahşap Kapı Boyama",
                "slug": "mobilya-ve-ahsap-kapi-boyama",
                "image": "uploads/services/ahsap-kapi-boyama.jpg",
                "seo_title": "Amerikan ve Ahşap Kapı Boyama Fiyatları | Mobilya Cila",
                "seo_description": "Sararmış amerikan kapılarınızı ve ahşap mobilyalarınızı ilk günkü haline getiriyoruz. Profesyonel kapı boyama ve mobilya cila hizmeti.",
                "focus_keywords": ["kapı boyama", "amerikan kapı boyama", "mobilya boyama fiyatları", "lake kapı boyama", "ahşap kapı yenileme"],
                "icon": "fas fa-door-open",
                "short_description": "Sararmış, çizilmiş kapılarınızı ve mobilyalarınızı atölyemizde yeniliyoruz. Amerikan panel kapı boyama ve mobilya lake cila işlemleriyle evinize ışıltı katın.",
                "description": """
                    <h2>Kapı ve Mobilyalarınızı Neden Boyatmalısınız?</h2>
                    <p>Zamanla sararan Amerikan panel kapılar veya cilası bozulan ahşap mobilyalar evinizin enerjisini düşürür. Kapı değiştirmek maliyetli ve tadilat gerektiren bir iştir. Oysa boyama işlemi ile kapılarınız fabrika çıkışı gibi pürüzsüz ve bembeyaz olabilir.</p>

                    <h3>Hizmet Kapsamımız</h3>
                    <ul>
                        <li><strong>Amerikan Panel Kapı Boyama:</strong> Sararmış kapıları özel panel kapı boyası ile yeniliyoruz.</li>
                        <li><strong>Ahşap Kapı Cila ve Boya:</strong> Masif kapıları vernikleyerek koruyor veya lake boya ile renk değiştiriyoruz.</li>
                        <li><strong>Mobilya Renk Değişimi:</strong> Koyu renkli vitrin, konsol veya ünitelerinizi modern renklere (gri, beyaz, antrasit) dönüştürüyoruz.</li>
                    </ul>

                    <h3>Pistole (Sprey) Boya Farkı</h3>
                    <p>Kapı ve mobilyaları evde fırça ile boyamak genellikle fırça izi ve dalgalanma yaratır. Biz, kapılarınızı söküp atölyemize götürüyor ve endüstriyel boya tabancaları ile pürüzsüz boyuyoruz.</p>
                """,
                "custom_features": ["Pistole Boya Tekniği", "Amerikan Kapı Uzmanlığı", "Leke Tutmayan Yüzey", "Nakliye Dahil Hizmet", "Kısa Sürede Teslim"],
                "steps": [
                    {"step_number": 1, "title": "Kapıların Sökülmesi", "description": "Ekibimiz kapı kanatlarını menteşelerinden ayırır ve kasaları yerinde boyamak üzere hazırlar. Kanatlar atölyeye taşınır."},
                    {"step_number": 2, "title": "Tamirat ve Zımpara", "description": "Kapı yüzeyindeki çarpma izleri, delikler veya kabarmalar çelik macun ile tamir edilir. Yüzey zımparalanıp pürüzsüzleştirilir."},
                    {"step_number": 3, "title": "Astar Uygulaması", "description": "Eski boyanın kusmasını engellemek ve yeni boyanın tutunması için güçlü bir astar katı atılır."},
                    {"step_number": 4, "title": "Boya Uygulaması", "description": "İstenilen renkte (genelde Amerikan Kapı Beyazı veya Kırık Beyaz) 2-3 kat boya uygulanır."},
                    {"step_number": 5, "title": "Montaj", "description": "Kuruyan kapılar ambalajlanarak getirilir ve yerlerine takılır. Kapı kolları ve kilit karşılıkları monte edilir."}
                ],
                "faqs": [
                    {"question": "Kapı kolları ve menteşeler de değişiyor mu?", "answer": "Hizmetimiz boyama odaklıdır ancak talep ederseniz tedarik ettiğiniz yeni kulp ve kilitlerin montajını ücretsiz yapıyoruz."},
                    {"question": "Sadece kanatları mı boyuyorsunuz, kasalar ne oluyor?", "answer": "Hayır, bütünlük bozulmaması için kasalar (pervazlar) da evinizde aynı boya ile boyanmaktadır."},
                    {"question": "Amerikan kapı boyası ne kadar dayanıklı?", "answer": "Kullandığımız boyalar silinebilir, darbelere karşı dirençli ve sararmaya karşı garantilidir."},
                    {"question": "Kaç günde teslim ediyorsunuz?", "answer": "Kapı adedine göre değişmekle birlikte genellikle 3-4 iş günü sürmektedir."},
                    {"question": "Evim çok kirlenir mi?", "answer": "Kasalara boya yapılırken maskeleme bandı ve örtü kullanıyoruz. Minimum kirlilikle işlem tamamlanır."}
                ]
            },
            {
                "title": "Sandalye ve Masa Boyama",
                "slug": "sandalye-ve-masa-boyama-yenileme",
                "image": "uploads/services/sandalye-masa-boyama.jpg",
                "seo_title": "Yemek Masası ve Sandalye Boyama | Gomalak Cila ve Lake",
                "seo_description": "Eskiyen yemek odası takımınızı yeniliyoruz. Masa sandalye boyama, ayak renk değişimi ve kırık tamiratı. Modoko ustalarından profesyonel çözüm.",
                "focus_keywords": ["sandalye boyama", "masa boyama", "yemek odası yenileme", "mobilya cila", "sandalye ayak boyama"],
                "icon": "fas fa-chair",
                "short_description": "Yemek masası ve sandalyelerinizi atmayın! Kırıklarını onarıyor, cilasını yeniliyor veya modern renklere boyayarak takımınızı baştan yaratıyoruz.",
                "description": """
                    <h2>Yemek Odası Takımlarınızı Yeniliyoruz</h2>
                    <p>Kaliteli ahşap masa ve sandalyeler günümüzde servet değerinde. Eskiyen veya renginden sıkıldığınız yemek odası takımınızı değiştirmek yerine yenileyerek hem bütçenizi koruyun hem de antika değerindeki eşyalarınıza sahip çıkın.</p>

                    <h3>Neler Yapıyoruz?</h3>
                    <ul>
                        <li><strong>Masa Yüzey Yenileme:</strong> Masanızın üstündeki sıcak bardak izlerini, çizikleri ve vernik yanıklarını yok ediyoruz.</li>
                        <li><strong>Renk Değişimi:</strong> Koyu kahve takımları beyaz, krem veya antrasit gibi modern renklere dönüştürüyoruz.</li>
                        <li><strong>Sandalye Sağlamlaştırma:</strong> Sallanan sandalye ayaklarını tutkallayıp işkence ile sıkıştırarak ilk günkü sağlamlığına getiriyoruz.</li>
                        <li><strong>Torna Ayak Boyama:</strong> Klasik oymalı ayaklara varak, eskitme veya lake uygulamaları yapıyoruz.</li>
                    </ul>
                """,
                "custom_features": ["Gomalak ve Lake Cila", "Sandalye Tutkallama", "Torna Ayak İşçiliği", "Masa Üstü Koruyucu Vernik", "Nakliye Hizmeti"],
                "steps": [
                    {"step_number": 1, "title": "Teslim Alma", "description": "Masa ve sandalyelerinizi evinizden teslim alıp atölyemize götürüyoruz."},
                    {"step_number": 2, "title": "Ham Haline Getirme", "description": "Eski vernik ve boya tamamen kazınarak (sistre) ahşabın ham dokusu ortaya çıkarılır."},
                    {"step_number": 3, "title": "Tamirat", "description": "Sallanan ayaklar sağlamlaştırılır, derin çizikler dolgu verniği veya macun ile kapatılır."},
                    {"step_number": 4, "title": "Renk ve Cila", "description": "Seçtiğiniz renkte boyama yapılır veya ahşabın doğal rengini koruyan şeffaf koruyucu cila atılır."},
                    {"step_number": 5, "title": "Paketleme ve Teslim", "description": "Ürünler çizilmeye karşı balonlu naylonla paketlenir ve evinize teslim edilir."}
                ],
                "faqs": [
                    {"question": "Masamın üzerindeki beyaz halka lekeleri geçer mi?", "answer": "Evet, zımpara ve sistre işlemi ile yüzey tamamen temizlendiği için tüm lekeler yok olur."},
                    {"question": "Sandalyelerim çok sallanıyor, tamir edilebilir mi?", "answer": "Evet, boya öncesi iskelet tamiri yapıyor, birleşim yerlerini yeniden tutkallıyoruz."},
                    {"question": "Sadece ayakları boyatabilir miyim?", "answer": "Evet, örneğin masa tab tablası ahşap kalıp, ayakları beyaza boyanarak 'Country' tarzı elde edilebilir."},
                    {"question": "Döşeme değişimi de yapıyor musunuz?", "answer": "Evet, 'Döşeme Yüzü Değişimi' hizmetimizle kombine olarak kumaş değişimi de yapıyoruz."},
                    {"question": "Nakliye ücretli mi?", "answer": "İstanbul Anadolu yakası ve belirli bölgelere ücretsiz nakliye hizmetimiz vardır."}
                ]
            },
            {
                "title": "Döşeme Yüzü Değişimi",
                "slug": "mobilya-doseme-yuzu-degisimi",
                "image": "uploads/services/doseme-degisimi.jpg",
                "seo_title": "Koltuk ve Sandalye Döşeme Yüzü Değişimi | Kumaş Yenileme",
                "seo_description": "Eskiyen koltuk ve sandalyelerinizin kumaşını değiştiriyoruz. Modoko kalitesinde döşeme işçiliği, nubuk, keten, kadife kumaş seçenekleri.",
                "focus_keywords": ["koltuk döşeme", "sandalye yüz değişimi", "berjer kaplama", "döşemelik kumaş", "koltuk yenileme"],
                "icon": "fas fa-couch",
                "short_description": "Mobilyalarınızın iskeleti sağlamsa, sadece yüzünü değiştirerek yeni gibi yapın. Yüzlerce kumaş seçeneği ve sünger değişimi ile konforu artırın.",
                "description": """
                    <h2>Mobilyalarınıza Yeni Bir Dokunuş</h2>
                    <p>Koltuklarınızın kumaşı yıprandı mı? Kediniz tırmaladı mı? Yoksa renginden mi sıkıldınız? EB Dekorasyon olarak, koltuk, berjer ve sandalyelerinizin döşemesini profesyonelce yeniliyoruz.</p>

                    <h3>Kumaş Seçeneklerimiz</h3>
                    <ul>
                        <li><strong>Silinebilir Kumaşlar:</strong> Leke tutmayan, teknolojik kumaşlar.</li>
                        <li><strong>Keten Dokular:</strong> Doğal ve ferah bir görünüm için.</li>
                        <li><strong>Nubuk ve Deri:</strong> Şık ve ağır duruşlu mekanlar için.</li>
                        <li><strong>Kadife:</strong> Yumuşak ve lüks bir his için.</li>
                    </ul>

                    <h3>Sünger Değişimi</h3>
                    <p>Sadece kumaşı değil, çökmüş oturma süngerlerini de yüksek dansiteli (32 DNS ve üzeri) gri süngerlerle değiştirerek konforunuzu ilk günkü haline getiriyoruz.</p>
                """,
                "custom_features": ["32 DNS Sünger", "Silinebilir Kumaşlar", "İskelet Güçlendirme", "Beriye ve Kapitone İşçiliği", "Adresten Alım Teslim"],
                "steps": [
                    {"step_number": 1, "title": "Kumaş Seçimi", "description": "Evinize kumaş kartelaları ile geliyoruz. Işık altında mobilyanıza en uygun rengi seçiyorsunuz."},
                    {"step_number": 2, "title": "Atölyeye Alım", "description": "Mobilyalarınız randevu günü evinizden alınır."},
                    {"step_number": 3, "title": "Söküm ve Kontrol", "description": "Eski kumaş ve süngerler sökülür. İskelet kontrol edilir, gerekirse tamir edilir."},
                    {"step_number": 4, "title": "Dikim ve Çakım", "description": "Usta terzilerimizce dikilen yeni kumaşlar, döşeme ustalarımız tarafından gergin ve düzgün şekilde çakılır."},
                    {"step_number": 5, "title": "Kalite Kontrol ve Teslim", "description": "Son kontroller yapıldıktan sonra paketlenerek teslim edilir."}
                ],
                "faqs": [
                    {"question": "Süngerleri de değiştiriyor musunuz?", "answer": "Evet, çökmüş süngerler isteğiniz üzerine HR veya gri sünger ile yenilenir."},
                    {"question": "Kumaşı kendim alabilir miyim?", "answer": "Evet, kumaşı siz temin edebilirsiniz, biz sadece işçilik hizmeti verebiliriz."},
                    {"question": "Ne kadar sürer?", "answer": "Sandalye yüz değişimi 3-4 gün, koltuk takımı değişimi 7-10 gün sürmektedir."},
                    {"question": "Chester koltuk kaplıyor musunuz?", "answer": "Evet, kapitone (düğmeli) işçiliği gerektiren Chester koltuklarda uzman ekibimiz vardır."},
                    {"question": "Fiyata kumaş dahil mi?", "answer": "Fiyat tekliflerimiz genellikle 'kumaş dahil' veya 'hariç' olarak ayrı ayrı belirtilir."}
                ]
            },
            {
                "title": "Yatak Odası Mobilya Boyama",
                "slug": "yatak-odasi-mobilya-boyama",
                "image": "uploads/services/yatak-odasi-boyama-yeni.jpg",
                "seo_title": "Yatak Odası Takımı Boyama ve Renk Değişimi | Gardırop Yenileme",
                "seo_description": "Yatak odası mobilyalarınızı boyayarak yeniliyoruz. Gardırop, şifonyer, komodin ve başlık boyama. Koyu renk mobilyadan beyaza dönüş.",
                "focus_keywords": ["yatak odası boyama", "gardırop boyama", "mobilya renk değiştirme", "yatak başlığı yenileme", "şifonyer boyama"],
                "icon": "fas fa-bed",
                "short_description": "Karanlık yatak odanızı aydınlatın! Eski takımınızı satmakla uğraşmayın, boyatarak modern, ferah ve 'Country' tarzı bir yatak odasına sahip olun.",
                "description": """
                    <h2>Yatak Odanızda Ferah Bir Başlangıç</h2>
                    <p>Yatak odası mobilyaları genellikle büyük ve hantal parçalardır. Koyu renkli mobilyalar odayı daha küçük ve basık gösterir. Yatak odası takımı boyama hizmetimizle, mobilyalarınızı mat beyaz, krem, gri veya pastel tonlara boyayarak odanızın havasını tamamen değiştiriyoruz.</p>

                    <h3>Dönüşüm Kapsamı</h3>
                    <ul>
                        <li><strong>Gardırop Boyama:</strong> Sürgülü veya kapaklı gardıropların dış yüzeyleri ve görünür yan panelleri.</li>
                        <li><strong>Şifonyer ve Komodinler:</strong> Çekmece klapaları ve gövdeleri.</li>
                        <li><strong>Yatak Başlığı:</strong> Ahşap kısımların boyanması veya kumaş kısımlarının değişimi.</li>
                        <li><strong>Makyaj Masası:</strong> Ayna çerçevesi ve masa yenileme.</li>
                    </ul>
                """,
                "custom_features": ["Mat/Parlak Seçeneği", "Kulp Değişimi Desteği", "Antibakteriyel Boya", "Çekmece İçi Temizlik", "Yerinde Montaj"],
                "steps": [
                    {"step_number": 1, "title": "Söküm İşlemi", "description": "Dolap kapakları, çekmece önleri ve sökülebilir parçalar kodlanarak sökülür."},
                    {"step_number": 2, "title": "Atölye Boyama", "description": "Parçalar atölyede zımpara, astar ve son kat boya işlemlerinden geçer."},
                    {"step_number": 3, "title": "Gövde Boyama (Yerinde)", "description": "Taşınması zor olan büyük gardırop kasaları, evinizde maskeleme yapılarak rulo veya pistole ile boyanır."},
                    {"step_number": 4, "title": "Kulp Montajı", "description": "Yeni tarzınıza uygun satın aldığınız kulpların delikleri açılır ve takılır."},
                    {"step_number": 5, "title": "Final", "description": "Tüm parçalar birleştirilir, odanız temizlenerek teslim edilir."}
                ],
                "faqs": [
                    {"question": "Gardırobun içi de boyanıyor mu?", "answer": "Standart hizmetimizde sadece dış görünür yüzeyler boyanır. İç kısımlar genellikle orijinal halinde bırakılır, çünkü eşya sürtünmesi fazladır. Ancak talep edilirse boyanabilir."},
                    {"question": "Boya kıyafetlerime bulaşır mı?", "answer": "Kesinlikle hayır. Boya tam kuruma sağladıktan sonra teslim edilir ve vernik katı sayesinde hiçbir şey bulaşmaz."},
                    {"question": "Sürgülü dolap mekanizması bozulur mu?", "answer": "Hayır, mekanizmalar maskelenir veya sökülür, boya temas etmez."},
                    {"question": "Çocuk odası için boya güvenli mi?", "answer": "Evet, su bazlı ve EN71-3 (oyuncak güvenliği) standartlarına uygun boyalarla çocuk odalarını da boyuyoruz."},
                    {"question": "Ne kadar sürede biter?", "answer": "Takımın büyüklüğüne göre 3 ile 5 iş günü arasında."}
                ]
            }
        ]
    },
    # -------------------------------------------------------------------------
    # KATEGORİ 2: Tamirat, Tadilat ve Dekorasyon
    # -------------------------------------------------------------------------
    {
        "category_name": "Tamirat, Tadilat ve Dekorasyon",
        "icon": "fas fa-tools",
        "services": [
            {
                "title": "Mutfak Tezgahı Değişimi ve Tamiri",
                "slug": "mutfak-tezgahi-degisimi-tamiri",
                "image": "uploads/services/mutfak-tezgahi.jpg",
                "seo_title": "Mutfak Tezgahı Değişimi | Granit, Cimstone, Belenco, Mermerit",
                "seo_description": "Çizilen, kırılan mutfak tezgahınızı değiştiriyoruz. Granit, mermerit, çimstone ve ahşap masif tezgah modelleri. Ölçüye özel üretim ve montaj.",
                "focus_keywords": ["mutfak tezgahı değişimi", "tezgah modelleri", "granit tezgah fiyatları", "belenco tezgah", "ahşap tezgah", "tezgah tamiri"],
                "icon": "fas fa-layer-group",
                "short_description": "Mutfağınızın havasını tezgah değişimi ile yenileyin. Granit, Kuvars, Çimstone veya Mermerit seçenekleri. Eskiyi söküp yenisini 1 günde takıyoruz.",
                "description": """
                    <h2>Mutfak Tezgahı Çözümleri</h2>
                    <p>Mutfak dolaplarınız sağlam ama tezgahınız lekeli, çizik veya modası geçmiş mi? Dolapları kırmadan sadece tezgahı değiştirerek mutfağınıza lüks bir görünüm kazandırabilirsiniz.</p>

                    <h3>Tezgah Çeşitlerimiz</h3>
                    <ul>
                        <li><strong>Kuvars (Çimstone, Belenco):</strong> Çizilmez, leke tutmaz, hijyenik ve modern görünümlü yapay taşlar.</li>
                        <li><strong>Granit:</strong> Doğal, ısıya dayanıklı ve eşsiz desenli.</li>
                        <li><strong>Mermerit:</strong> Ekonomik, döküm yekpare evye ve tezgah seçeneği.</li>
                        <li><strong>Masif Ahşap:</strong> Doğal ağaçtan (Meşe, İroko) sıcak bir görünüm, özel yağ bakımlı.</li>
                    </ul>

                    <h3>Tezgah Tamiri</h3>
                    <p>Mermerit veya corian tezgahlarınızdaki çatlakları, yanıkları özel dolgu malzemeleri ve polisaj (zımpara-cila) işlemi ile tamir ediyoruz.</p>
                """,
                "custom_features": ["Eski Tezgah Sökümü", "Leke Tutmaz Yüzeyler", "Gömme Evye Seçeneği", "Süpürgelik Dahil", "Su Sızdırmazlık Garantisi"],
                "steps": [
                    {"step_number": 1, "title": "Ölçü Alımı", "description": "Mevcut dolaplarınızın üzerine lazer metre ile milimetrik ölçü alınır. Evye ve ocak yerleri belirlenir."},
                    {"step_number": 2, "title": "Kesim ve Hazırlık", "description": "Seçilen taş plakası atölyede CNC makinelerde kesilir, kenar pahlamaları yapılır."},
                    {"step_number": 3, "title": "Söküm", "description": "Eski tezgahınız dolaplara zarar vermeden dikkatlice sökülür ve evden uzaklaştırılır."},
                    {"step_number": 4, "title": "Montaj", "description": "Yeni tezgah yerleştirilir. Ekyerleri (varsa) özel yapıştırıcılarla birleştirilir, evye ve ocak montajı yapılır."},
                    {"step_number": 5, "title": "Silikon ve Teslim", "description": "Duvar dipleri antibakteriyel silikon ile kapatılır ve kullanıma hazır teslim edilir."}
                ],
                "faqs": [
                    {"question": "Tezgah değişimi ne kadar sürer?", "answer": "Ölçü alındıktan sonra imalat 3-7 gün sürer. Evinizdeki montaj işlemi ise sadece 2-3 saatte biter."},
                    {"question": "Hangi tezgah daha dayanıklı?", "answer": "Kuvars (Çimstone/Belenco) ve Granit en dayanıklı malzemelerdir. Mermerit daha ekonomiktir ancak ısıya karşı daha hassastır."},
                    {"question": "Evyeyi de değiştiriyor musunuz?", "answer": "Evet, isterseniz yeni krom veya granit evye temin edip montajını yapıyoruz."},
                    {"question": "Tezgah arası fayanslar zarar görür mü?", "answer": "Genellikle zarar görmeden sökülür. Ancak tezgah kalınlığı değişirse süpürgelik ile aradaki boşluk kapatılır."},
                    {"question": "Masif tezgah suya dayanıklı mı?", "answer": "Özel tik yağı (teak oil) ve vernik uygulamaları ile suya dayanıklı hale getirilir ancak düzenli bakım ister."}
                ]
            },
            {
                "title": "TV Ünitesi ve Duvar Dekorasyonu",
                "slug": "tv-unitesi-ve-duvar-dekorasyonu",
                "image": "uploads/services/tv-unitesi-dekor.jpg",
                "seo_title": "Özel Tasarım TV Ünitesi ve Çıtalama Duvar Dekorasyonu",
                "seo_description": "Salonunuz için modern TV ünitesi tasarımları, duvar çıtalama, LED ışıklı paneller ve dekoratif boya uygulamaları. Kişiye özel üretim.",
                "focus_keywords": ["tv ünitesi modelleri", "duvar çıtalama", "tv arkası duvar kağıdı", "tv ünitesi tasarım", "salon dekorasyonu"],
                "icon": "fas fa-tv",
                "short_description": "Salonunuzun odak noktasını tasarlıyoruz. Size özel ölçülerde TV ünitesi, duvar çıtalama, mermer görünümlü paneller ve şömine uygulamaları.",
                "description": """
                    <h2>Salonunuzun Havasını Değiştirin</h2>
                    <p>Standart mobilya mağazalarındaki hazır ölçü TV üniteleri salonunuza uymuyor mu? Duvarınızın boydan boya değerlendirildiği, depolama alanı sunan ve estetik duran özel tasarım çözümler sunuyoruz.</p>

                    <h3>Neler Yapıyoruz?</h3>
                    <ul>
                        <li><strong>Duvar Çıtalama:</strong> Klasik ve modern tarzda poliüretan veya ahşap çıta uygulamaları.</li>
                        <li><strong>Özel Üretim TV Ünitesi:</strong> Yerinize tam ölçü, kapaklı dolaplar, raflar ve çekmeceler.</li>
                        <li><strong>TV Arkası Dekorasyon:</strong> Doğal taş, mermer görünümlü PVC panel, patlatma taş veya duvar kağıdı uygulamaları.</li>
                        <li><strong>Elektrikli Şömine Entegrasyonu:</strong> TV ünitesinin altına yapay alevli şömine hazneleri.</li>
                        <li><strong>Gizli LED Aydınlatma:</strong> Raf altlarında veya panel arkasında ambiyans ışıklandırması.</li>
                    </ul>
                """,
                "custom_features": ["3D Çizim ve Sunum", "Gizli Kablo Kanalları", "LED Aydınlatma Entegrasyonu", "Özel Ölçü Üretim", "Duvar Güçlendirme"],
                "steps": [
                    {"step_number": 1, "title": "Keşif ve Tasarım", "description": "Duvarınızın ölçüsü alınır. İsteklerinize göre 3 boyutlu tasarım çizilir ve onayınıza sunulur."},
                    {"step_number": 2, "title": "Üretim", "description": "Onaylanan proje, atölyemizde MDF veya istenilen malzemeden üretilir. Boya işlemi yapılır."},
                    {"step_number": 3, "title": "Altyapı Hazırlığı", "description": "Duvarınızda gerekli elektrik priz yerleri taşınır, TV askı aparatı için güçlendirme yapılır."},
                    {"step_number": 4, "title": "Montaj", "description": "Ünitelerin ve duvar panellerinin montajı titizlikle yapılır."},
                    {"step_number": 5, "title": "TV Kurulumu", "description": "Televizyonunuz yerine asılır, kablolar gizlenir ve sistem çalışır halde teslim edilir."}
                ],
                "faqs": [
                    {"question": "TV ünitesi duvara mı monte ediliyor?", "answer": "Modeline göre değişir; bazıları tamamen asma (yüzer) modüllerdir, bazıları zeminle temas eder. Duvarınızın sağlamlığı (tuğla, alçıpan) kontrol edilir."},
                    {"question": "Çıtalama işlemi boya gerektirir mi?", "answer": "Evet, çıtalar yapıştırıldıktan sonra duvarla bütünleşmesi için komple boyanırsa en iyi sonuç alınır."},
                    {"question": "Kablolar nasıl gizleniyor?", "answer": "Panel arkasından veya duvar içinden kanal açılarak tüm kablo karmaşası yok edilir."},
                    {"question": "Ne kadar sürede teslim edilir?", "answer": "Özel imalat mobilyalar 10-15 gün, sadece çıtalama veya panel işlemleri 1-2 gün sürer."},
                    {"question": "Şömine ısıtıyor mu?", "answer": "Kullandığımız elektrikli şöminelerin hem görsel alev efekti hem de ısıtma fanı özelliği vardır."}
                ]
            },
            {
                "title": "Kafe İçi Dekorasyon ve Tasarım",
                "slug": "kafe-ici-dekorasyon-tasarim",
                "image": "uploads/services/kafe-dekorasyon.jpg",
                "seo_title": "Anahtar Teslim Kafe ve Restoran Dekorasyonu | İç Mimarlık",
                "seo_description": "Kafe, restoran ve ofisler için konsept tasarım ve uygulama. Mobilya, sedir, bar bankosu ve duvar dekorasyonu. Müşteri çeken mekanlar yaratıyoruz.",
                "focus_keywords": ["kafe dekorasyonu", "restoran iç mimarı", "kafe mobilyaları", "sedir koltuk", "bar bankosu yapımı", "konsept kafe tasarım"],
                "icon": "fas fa-coffee",
                "short_description": "İşletmenizi müşterilerin fotoğraf çekip paylaşacağı bir mekana dönüştürüyoruz. Konsept proje, özel otuma grupları, aydınlatma ve anahtar teslim uygulama.",
                "description": """
                    <h2>Başarılı Bir Mekan Tasarımla Başlar</h2>
                    <p>Yiyecek ve içecek kalitesi kadar, mekanın atmosferi de müşteri sadakati için kritiktir. EB Dekorasyon olarak, işletmenizin kimliğini yansıtan, ergonomik ve instagram-dostu mekanlar tasarlıyoruz.</p>

                    <h3>Hizmetlerimiz</h3>
                    <ul>
                        <li><strong>Konsept Geliştirme:</strong> Industrial, Bohemian, Minimalist veya Klasik tarzda kimlik oluşturma.</li>
                        <li><strong>Özel Mobilya Üretimi:</strong> Ölçüye özel sedir koltuklar, mermer veya ahşap masalar, sandalyeler.</li>
                        <li><strong>Bar ve Servis Bankosu:</strong> Fonksiyonel ve şık bar bölümleri.</li>
                        <li><strong>Zemin ve Tavan:</strong> Epoksi zemin, asma tavan, sarkıt aydınlatma sistemleri.</li>
                        <li><strong>Tabela ve Branding:</strong> İç mekan yönlendirmeleri ve logo uygulamaları.</li>
                    </ul>
                """,
                "custom_features": ["Ticari Alan Uzmanlığı", "Ergonomik Yerleşim Planı", "Akustik Çözümler", "Hızlı Uygulama (Gece Çalışması)", "Dayanıklı Malzeme Seçimi"],
                "steps": [
                    {"step_number": 1, "title": "Bütçe ve İhtiyaç Analizi", "description": "Menünüze, hedef kitlenize ve bütçenize uygun konsepti belirliyoruz."},
                    {"step_number": 2, "title": "Projelendirme", "description": "Mekanın 2D yerleşimi ve 3D görselleri hazırlanır. Malzeme seçimleri yapılır."},
                    {"step_number": 3, "title": "İmalat", "description": "Mobilyalar atölyemizde, metal ve ahşap aksamlar fabrikamızda üretilir."},
                    {"step_number": 4, "title": "Şantiye Uygulaması", "description": "Tadilat, boya, elektrik ve su tesisatı işlemleri yürütülür."},
                    {"step_number": 5, "title": "Kurulum ve Açılış", "description": "Mobilya montajı, detay temizlik ve son dekoratif dokunuşlar yapılarak mekan açılışa hazır hale getirilir."}
                ],
                "faqs": [
                    {"question": "Sadece mobilya yapıyor musunuz?", "answer": "Evet, projeniz hazırsa sadece masa, sandalye, sedir imalatı da yapıyoruz."},
                    {"question": "Mevcut kafemi yenilemek istiyorum, dükkanı kapatmam gerekir mi?", "answer": "Kısmi yenilemelerde (sandalye yüz değişimi, boya vb.) gece çalışarak dükkanın çalışmasına engel olmadan ilerleyebiliriz."},
                    {"question": "Proje çizim ücreti var mı?", "answer": "Uygulamayı biz yapacaksak proje ücreti almıyoruz veya fiyattan düşüyoruz."},
                    {"question": "Hangi şehirlerde hizmet veriyorsunuz?", "answer": "Ağırlıklı İstanbul olmak üzere çevre illere de proje bazlı hizmet veriyoruz."},
                    {"question": "Küçük m2 dükkanlar için çözümünüz var mı?", "answer": "Evet, dar alanları ayna ve doğru yerleşimle daha ferah ve kapasiteli hale getirmekte uzmanız."}
                ]
            },
            {
                "title": "Mobilya Tamiratı ve Bakımı",
                "slug": "mobilya-tamirati-ve-bakimi",
                "image": "uploads/services/mobilya-tamir.jpg",
                "seo_title": "Yerinde Mobilya Tamiri ve Montajı | Dolap Ray Kapak Tamiri",
                "seo_description": "Kırılan menteşeler, düşen kapaklar, bozulan çekmece rayları... Mobilyalarınızdaki her türlü arızayı evinizde veya atölyemizde tamir ediyoruz.",
                "focus_keywords": ["mobilya tamiri", "dolap tamircisi", "sürgülü dolap tamiri", "çekmece ray değişimi", "mobilya montaj ustası"],
                "icon": "fas fa-wrench",
                "short_description": "Kırık sandalye bacağı, çalışmayan çekmece, kapanmayan dolap kapağı... Ufak sorunlar için mobilyanızı atmayın. Profesyonel tamir ekibimizle hızlı çözüm.",
                "description": """
                    <h2>Mobilyalarınızın Ömrünü Uzatın</h2>
                    <p>Mobilyalar zamanla mekanik arızalar verebilir. Sürgülü dolap kapaklarının raydan çıkması, menteşelerin yerinden oynaması veya çekmecelerin takılması sık görülen sorunlardır. Bu sorunlar için mobilyanızı değiştirmenize gerek yok.</p>

                    <h3>Tamir Hizmetlerimiz</h3>
                    <ul>
                        <li><strong>Sürgülü Dolap Tamiri:</strong> Tekerlek mekanizması değişimi, ray değişimi, stop ayarı.</li>
                        <li><strong>Menteşe Değişimi:</strong> Bozulan, ses yapan menteşelerin frenli menteşelerle değişimi.</li>
                        <li><strong>Çekmece Rayı Değişimi:</strong> Teleskopik veya bilyalı yeni ray montajı.</li>
                        <li><strong>Kırık Onarımı:</strong> Sandalye bacağı, masa ayağı gibi ahşap kırıklarının tutkallanması.</li>
                        <li><strong>Montaj/Demontaj:</strong> Taşınma veya oda değişikliği için dolapların sökülüp kurulması.</li>
                    </ul>
                """,
                "custom_features": ["Yerinde Servis", "Orijinal Yedek Parça", "Frenli Menteşe Dönüşümü", "Hızlı Müdahale", "Ekonomik Fiyat"],
                "steps": [
                    {"step_number": 1, "title": "Sorun Tespiti", "description": "WhatsApp üzerinden gönderdiğiniz fotoğraf/video ile veya yerinde sorun tespit edilir."},
                    {"step_number": 2, "title": "Malzeme Temini", "description": "Gerekli mekanizma, tekerlek, kulp veya menteşeler tedarik edilir."},
                    {"step_number": 3, "title": "Tamir İşlemi", "description": "Uzman ustamız evinizde tamiratı gerçekleştirir. Atölye gerektiren işlerde parça alınır."},
                    {"step_number": 4, "title": "Ayar ve Yağlama", "description": "Sadece bozuk parça değil, diğer hareketli aksamların da ayarları yapılır ve yağlanır."},
                    {"step_number": 5, "title": "Teslim", "description": "Mobilya sorunsuz çalışır vaziyette teslim edilir."}
                ],
                "faqs": [
                    {"question": "Servis ücretiniz var mı?", "answer": "Evet, yerinde tespit ve küçük tamirler için standart bir servis ücretimiz vardır. Parça değişimi ekstra ücretlendirilir."},
                    {"question": "Ray dolap kapaklarım çok ağır, kapanmıyor. Çözüm var mı?", "answer": "Evet, mekanizmalar zamanla yorulur. Yüksek taşıma kapasiteli yeni nesil tekerleklerle kapakları kuş tüyü gibi hafifletiyoruz."},
                    {"question": "IKEA mobilyası montajı yapıyor musunuz?", "answer": "Evet, kutulu mobilyaların kurulumunu profesyonelce yapıyoruz."},
                    {"question": "Hemen geliyor musunuz?", "answer": "Randevu sistemi ile çalışıyoruz ancak acil durumlar için (kapağın üzerine düşmesi vb.) aynı gün servis vermeye çalışıyoruz."},
                    {"question": "Tamir edilen yer garanti kapsamında mı?", "answer": "Değiştirdiğimiz mekanik parçalara üretici garantisi, işçiliğimize de servis garantisi veriyoruz."}
                ]
            },
            {
                "title": "Ev İçi Genel Dekorasyon",
                "slug": "ev-ici-genel-dekorasyon",
                "image": "uploads/services/ev-dekorasyon.jpg",
                "seo_title": "Anahtar Teslim Ev Tadilatı ve Dekorasyon | İç Mimar Desteği",
                "seo_description": "Komple ev tadilatı, banyo & mutfak yenileme, boya badana, alçıpan ve parke işleri. Tek muhatap, garantili işçilik ve zamanında teslimat.",
                "focus_keywords": ["ev tadilatı", "anahtar teslim dekorasyon", "komple ev yenileme", "iç mimarlık ofisi", "ev dekorasyon fikirleri"],
                "icon": "fas fa-home",
                "short_description": "Evinizi baştan aşağı yeniliyoruz. Projelendirme, kırım-döküm, tesisat, boya, mobilya ve temizlik... Tüm süreç tek elden, profesyonel yönetimle.",
                "description": """
                    <h2>Hayalinizdeki Eve Kavuşun</h2>
                    <p>Parça parça ustalarla uğraşmak, maliyet hesaplarını şaşırmak ve uzayan tadilat süreçleri kabusunuz olmasın. EB Dekorasyon, "Anahtar Teslim" mantığıyla, A'dan Z'ye tüm ev yenileme sürecinizi yönetir.</p>

                    <h3>Neler Yapıyoruz?</h3>
                    <p>Banyo yenilemeden salona, mutfaktan yatak odasına kadar komple çözüm:</p>
                    <ul>
                        <li><strong>İnşaat İşleri:</strong> Duvar kırma, örme, moloz atımı.</li>
                        <li><strong>Tesisat:</strong> Elektrik ve su tesisatının yenilenmesi.</li>
                        <li><strong>Yüzeyler:</strong> Seramik, fayans, parke, boya ve duvar kağıdı.</li>
                        <li><strong>Tavan:</strong> Asma tavan, gergi tavan, kartonpiyer ve LED havuzları.</li>
                        <li><strong>Mobilya:</strong> Mutfak dolabı, banyo dolabı, portmanto ve kapılar.</li>
                    </ul>

                    <h3>Neden Anahtar Teslim?</h3>
                    <p>Tek bir sorumlu ile muhatap olursunuz. İş programı bellidir, sürpriz maliyetler çıkmaz. Uyumlu bir ekip çalıştığı için işler birbirini beklemez, hızlı biter.</p>
                """,
                "custom_features": ["3D Görselleştirme", "Sabit Fiyat Garantisi", "Sözleşmeli Çalışma", "Zamanında Teslim", "İş Sonrası Temizlik"],
                "steps": [
                    {"step_number": 1, "title": "Keşif ve İstekler", "description": "Evinizi geziyor, ihtiyaçlarınızı ve hayallerinizi dinliyoruz. Bütçe aralığınızı belirliyoruz."},
                    {"step_number": 2, "title": "Planlama ve Teklif", "description": "Yapılacak işlerin listesi, kullanılacak malzemeler ve net fiyat teklifi sunulur."},
                    {"step_number": 3, "title": "Sözleşme ve Başlangıç", "description": "Karar verildikten sonra iş takvimi ve ödeme planını içeren sözleşme imzalanır."},
                    {"step_number": 4, "title": "Uygulama", "description": "Kırım işleriyle başlar, sırasıyla tesisat, alçı, boya, zemin ve mobilya montajı ile devam eder."},
                    {"step_number": 5, "title": "Teslim", "description": "İnşaat temizliği yapılır, tüm sistemler test edilir ve anahtarınız size teslim edilir."}
                ],
                "faqs": [
                    {"question": "2+1 ev tadilatı ne kadar tutar?", "answer": "Kullanılacak malzemenin kalitesine (fayans, parke, dolap vb.) ve yapılacak işin kapsamına göre çok değişkenlik gösterir. Ücretsiz keşif sonrası net fiyat verebiliriz."},
                    {"question": "Tadilat ne kadar sürer?", "answer": "Komple ev tadilatları genellikle 30-45 gün arasında tamamlanır."},
                    {"question": "Taksit imkanı var mı?", "answer": "Kredi kartına taksit seçeneklerimiz veya anlaşmalı bankalarla finansman çözümlerimiz mevcuttur."},
                    {"question": "Evde eşya varken tadilat olur mu?", "answer": "Komple tadilatta eşyaların boşaltılması gerekir. Kısmi tadilatta (sadece banyo gibi) eşyalar korunarak çalışılabilir."},
                    {"question": "Garanti veriyor musunuz?", "answer": "Evet, yaptığımız tüm uygulamalar (tesisat, boya, mobilya) firmamız garantisi altındadır."}
                ]
            }
        ]
    },
    # -------------------------------------------------------------------------
    # KATEGORİ 3: Zemin ve Parke Sistemleri
    # -------------------------------------------------------------------------
    {
        "category_name": "Zemin ve Parke Sistemleri",
        "icon": "fas fa-layer-group",
        "services": [
            {
                "title": "Laminant Parke Döşeme",
                "slug": "laminant-parke-doseme",
                "image": "uploads/services/laminant-parke.jpg",
                "seo_title": "Laminant Parke Döşeme Fiyatları ve Modelleri | Zemin Kaplama",
                "seo_description": "Ev ve ofisler için AGT, Çamsan, Vario marka laminant parke satışı ve montajı. Derzli, derzsiz, suya dayanıklı parke seçenekleri. Ücretsiz keşif.",
                "focus_keywords": ["laminant parke çeşitleri", "parke döşeme ustası", "derzli parke modelleri", "suya dayanıklı parke", "zemin yenileme"],
                "icon": "fas fa-th-large",
                "short_description": "Zemininizi ısıtın ve güzelleştirin. En kaliteli markaların yüzlerce renk seçeneği ile anahtar teslim parke döşeme hizmeti. Süpürgelik ve şilte dahil.",
                "description": """
                    <h2>Zeminde Şıklık ve Dayanıklılık</h2>
                    <p>Laminant parke, hem ekonomik hem de estetik olması nedeniyle en çok tercih edilen zemin malzemesidir. EB Dekorasyon olarak, Türkiye'nin en iyi markalarının (AGT, Çamsan, Yıldız Entegre) bayiliğini ve uygulamasını yapıyoruz.</p>

                    <h3>Parke Seçerken Nelere Dikkat Edilmeli?</h3>
                    <ul>
                        <li><strong>Sınıfı (Devir):</strong> Evler için 31. Sınıf (AC3), ofisler için 32. Sınıf (AC4) veya 33. Sınıf (AC5) tercih edilmelidir.</li>
                        <li><strong>Derzli/Derzsiz:</strong> Derzli (V oluklu) parkeler ahşap hissiyatını daha çok verir ve mekanı geniş gösterir.</li>
                        <li><strong>Kalınlık:</strong> 8mm standarttır, 10mm ve 12mm daha tok bir ses ve ısı yalıtımı sağlar.</li>
                    </ul>

                    <h3>Hizmet Paketimiz</h3>
                    <p>Parke m2 fiyatlarımıza genellikle; parke, 2mm şilte, 6cm süpürgelik ve profesyonel montaj işçiliği dahildir. Kapı altı kesimi ve pervaz düzeltmeleri de ekibimizce yapılır.</p>
                """,
                "custom_features": ["AGT & Çamsan Bayi", "Tozsuz Süpürgelik Kesimi", "Kapı Altı Kesimi Dahil", "Şilte ve Süpürgelik Hediye", "Hızlı Montaj (1 Günde)"],
                "steps": [
                    {"step_number": 1, "title": "Keşif ve Ölçü", "description": "Oda ölçüleri alınır, fire payı hesaplanır. Zemin düzgünlüğü kontrol edilir."},
                    {"step_number": 2, "title": "Model Seçimi", "description": "Karteladan renk ve model beğenilir. Süpürgelik rengine karar verilir."},
                    {"step_number": 3, "title": "Zemin Hazırlığı", "description": "Mevcut halıflex vb. sökülür. Zemin temizlenir ve şilte (ses yalıtımı) serilir."},
                    {"step_number": 4, "title": "Döşeme", "description": "Kilitli sistem parkeler boşluk bırakılarak (yaz-kış genleşmesi için) döşenir."},
                    {"step_number": 5, "title": "Süpürgelik ve Geçişler", "description": "Süpürgelikler monte edilir, kapı eşik profilleri takılır ve işlem tamamlanır."}
                ],
                "faqs": [
                    {"question": "Eşyalı evde parke yapılır mı?", "answer": "Evet, eşyaları oda oda kaydırarak uygulama yapıyoruz. Biraz zahmetli olsa da mümkündür."},
                    {"question": "Parke üzerine parke olur mu?", "answer": "Eski parke düzgünse ve kapı yükseklikleri kurtarıyorsa yapılabilir. Ancak tavsiyemiz eskinin sökülmesidir."},
                    {"question": "Suya dayanıklı parke var mı?", "answer": "Evet, yeni nesil 'Aqua' serisi parkeler suya karşı 24-48 saat dayanıklıdır, mutfaklarda bile kullanılabilir."},
                    {"question": "Süpürgelikler fiyata dahil mi?", "answer": "Kampanyalarımızda genellikle standart 6cm süpürgelik dahildir. 8cm veya 10cm lake süpürgelikler fark oluşturabilir."},
                    {"question": "Ne kadar sürede biter?", "answer": "Ortalama bir daire (80-100 m2) 1 gün içinde tamamlanır."}
                ]
            },
            {
                "title": "Parke Kurulumu ve Renk Çeşitleri",
                "slug": "parke-kurulumu-renk-cesitleri",
                "image": "uploads/services/parke-renkleri.jpg",
                "seo_title": "Balıksırtı ve Macar Parke Uygulamaları | Özel Tasarım Zemin",
                "seo_description": "Klasik düz döşemenin ötesine geçin. Balıksırtı (Herringbone) ve Macar (Chevron) parke montajı. Özel renk ve desen seçenekleri.",
                "focus_keywords": ["balıksırtı parke", "macar kesim parke", "herringbone parke", "özel tasarım parke", "laminant parke renkleri"],
                "icon": "fas fa-palette",
                "short_description": "Zeminde fark yaratmak isteyenler için Balıksırtı ve Macar kesim parke uygulamaları. Gri, meşe, ceviz ve antrasit tonlarında modern seçenekler.",
                "description": """
                    <h2>Zeminde Sanat: Özel Döşeme Teknikleri</h2>
                    <p>Standart parke döşemesi size sıradan mı geliyor? Evinize saray havası katan Balıksırtı (Herringbone) veya modern mimarinin gözdesi Macar (Chevron) döşeme teknikleri ile tanışın.</p>

                    <h3>Döşeme Şekilleri</h3>
                    <ul>
                        <li><strong>Balıksırtı (Herringbone):</strong> Parkelerin 90 derece açıyla birbirine kilitlendiği, klasik ve zamansız bir tarz.</li>
                        <li><strong>Macar (Chevron):</strong> Parkelerin uçlarının 45 veya 60 derece kesilerek birleştiği, ok yönü oluşturan modern tarz.</li>
                        <li><strong>Kare/Sepet Örgü:</strong> Nostaljik ve geometrik bir görünüm.</li>
                    </ul>

                    <h3>Renk Trendleri</h3>
                    <ul>
                        <li><strong>Gri ve Gümüş Meşe:</strong> Modern ve minimalist evler için.</li>
                        <li><strong>Doğal Meşe:</strong> İskandinav ve sıcak bir atmosfer için.</li>
                        <li><strong>Koyu Ceviz:</strong> Klasik ve ağırbaşlı salonlar için.</li>
                    </ul>
                """,
                "custom_features": ["Balıksırtı Uzmanlığı", "Lazer Hizalama", "Fire Hesabı Danışmanlığı", "Özel Ebat Parke Temini", "Mimari Destek"],
                "steps": [
                    {"step_number": 1, "title": "Mekanın Analizi", "description": "Odanın ışık alışı ve geometrisine göre döşeme yönüne (ışığa dik veya paralel) karar verilir."},
                    {"step_number": 2, "title": "Lazerli Başlangıç", "description": "Balıksırtı döşemede ilk sıranın düzgünlüğü kritiktir. Lazer hizalama ile merkez hattı oluşturulur."},
                    {"step_number": 3, "title": "Hassas Kesim", "description": "Duvar dipleri ve köşeler milimetrik hesapla kesilir."},
                    {"step_number": 4, "title": "Uygulama", "description": "Parça parça desen oluşturularak ilerlenir."},
                    {"step_number": 5, "title": "Final", "description": "Süpürgelikler takılır ve zemin temizlenir."}
                ],
                "faqs": [
                    {"question": "Balıksırtı parke daha mı pahalı?", "answer": "Evet, hem malzeme m2 fiyatı daha yüksektir hem de uygulama işçiliği standart döşemeye göre daha zor ve zaman alıcıdır."},
                    {"question": "Fire oranı neden yüksek?", "answer": "Özel kesimli döşemelerde (köşelere gelen parçalar nedeniyle) standart döşemeye göre %10-15 daha fazla fire verilebilir."},
                    {"question": "Her parke balıksırtı döşenir mi?", "answer": "Hayır, kilit sistemleri buna uygun üretilmiş özel seriler (A ve B kutuları) gerekir."},
                    {"question": "Küçük odalarda yapılmalı mı?", "answer": "Balıksırtı desen mekanı hareketlendirir ancak çok küçük odalarda göz yorabilir. Genellikle salon ve koridorlarda tercih edilir."},
                    {"question": "Tamiri mümkün mü?", "answer": "Evet, kilitli sistem olduğu için hasar gören parçalar lokal olarak değiştirilebilir."}
                ]
            }
        ]
    }
]

# =============================================================================
# VARSAYILAN DEĞERLER (Yedek)
# =============================================================================
DEFAULT_FEATURES = ["Ücretsiz Keşif", "2 Yıl Garanti", "Zamanında Teslim", "Profesyonel Ekip"]
DEFAULT_STEPS = [
    {"step_number": 1, "title": "Ücretsiz Keşif", "description": "Uzman ekibimiz evinize gelerek ihtiyacınızı yerinde değerlendirir."},
    {"step_number": 2, "title": "Teklif ve Planlama", "description": "Detaylı fiyat teklifi ve iş takvimi sunulur."},
    {"step_number": 3, "title": "Uygulama", "description": "Profesyonel ekibimiz işi titizlikle gerçekleştirir."},
    {"step_number": 4, "title": "Kontrol ve Teslim", "description": "İş tamamlandığında birlikte kontrol edilir ve teslim edilir."}
]


def turkish_slugify(text: str) -> str:
    """Türkçe karakterleri destekleyen slug üretici."""
    tr_chars = {'ı': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g', 'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's', 'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c'}
    for tr_char, en_char in tr_chars.items():
        text = text.replace(tr_char, en_char)
    return slugify(text)


class Command(BaseCommand):
    help = 'EB Dekorasyon hizmet verilerini detaylı SEO içerikleriyle veritabanına yükler.'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Mevcut verileri siler ve yeniden oluşturur.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n' + '=' * 60))
        self.stdout.write(self.style.WARNING('  EB DEKORASYON - SEO İÇERİK YÜKLEME'))
        self.stdout.write(self.style.WARNING('=' * 60 + '\n'))

        if options['clear']:
            self.clear_existing_data()

        stats = {'cats': 0, 'new_serv': 0, 'upd_serv': 0, 'features': 0, 'steps': 0, 'faqs': 0}

        for category_data in SERVICES_DATA:
            # 1. Kategori
            cat_name = category_data['category_name']
            category, created = ServiceCategory.objects.get_or_create(
                slug=turkish_slugify(cat_name),
                defaults={'name': cat_name, 'icon': category_data.get('icon', 'fas fa-cog'), 'is_active': True}
            )
            if created: stats['cats'] += 1
            
            self.stdout.write(self.style.SUCCESS(f'📂 {cat_name}'))

            # 2. Hizmetler
            for service_data in category_data.get('services', []):
                result = self.create_service(category, service_data)
                
                if result['created']:
                    stats['new_serv'] += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ YENİ: {service_data["title"]}'))
                else:
                    stats['upd_serv'] += 1
                    self.stdout.write(self.style.HTTP_INFO(f'  → GÜNCEL: {service_data["title"]}'))
                
                stats['features'] += result['features_created']
                stats['steps'] += result['steps_created']
                stats['faqs'] += result['faqs_created']

        self.print_summary(stats)

    def create_service(self, category, data: dict) -> dict:
        result = {'created': False, 'features_created': 0, 'steps_created': 0, 'faqs_created': 0}

        title = data['title']
        slug = data.get('slug') or turkish_slugify(title)
        
        # Temel Alanlar
        defaults = {
            'category': category,
            'title': title,
            'seo_title': data.get('seo_title', title)[:60],
            'seo_description': data.get('seo_description', '')[:160],
            'short_description': data.get('short_description', ''),
            'description': data.get('description', ''),
            'icon': data.get('icon', 'fas fa-cog'),
            'image': data.get('image', 'uploads/service_default.jpg'),
            'isActive': True,
            'showIndex': True
        }

        # Hizmet oluştur/güncelle
        service, created = Service.objects.update_or_create(
            slug=slug,
            defaults=defaults
        )
        result['created'] = created

        # Focus keywords (Tagging yapılabilir ama modelde field yok, şimdilik atlıyoruz veya description içine gömüldü saysayıyoruz)
        
        # İlişkili Veriler
        result['features_created'] = self.add_items(service, Feature, data.get('custom_features', DEFAULT_FEATURES), 'features', 'name')
        result['steps_created'] = self.add_steps(service, data.get('steps', DEFAULT_STEPS))
        result['faqs_created'] = self.add_faqs(service, data.get('faqs', []))

        return result

    def add_items(self, service, model, items, relation_name, field_name):
        """Many-to-Many generic ekleme (Feature vb için)"""
        count = 0
        # ServiceBase modelinde features alanı ManyToMany.
        # Önce mevcutları temizlemeyelim, sadece yeni varsa ekleyelim veya clear() yapıp set edelim?
        # Temiz bir başlangıç için clear yapmak mantıklı, ama global feature'lar silinmemeli.
        # Bu yüzden service.features.clear() diyerek bu hizmetin ilişkilerini koparalım.
        getattr(service, relation_name).clear()
        
        for item in items:
            obj, _ = model.objects.get_or_create(**{field_name: item}, defaults={'description': f'{item} özelliği.'})
            getattr(service, relation_name).add(obj)
            count += 1
        return count

    def add_steps(self, service, steps_data):
        ServiceStep.objects.filter(service=service).delete()
        count = 0
        for step in steps_data:
            ServiceStep.objects.create(
                service=service,
                step_number=step.get('step_number', count + 1),
                title=step['title'],
                description=step['description']
            )
            count += 1
        return count

    def add_faqs(self, service, faqs_data):
        service.faqs.clear()
        count = 0
        for faq_data in faqs_data:
            # FAQ'lar genellikle unique sorulardır.
            faq, _ = Faq.objects.get_or_create(
                question=faq_data['question'],
                defaults={'answer': faq_data['answer'], 'isActive': True, 'showIndex': False}
            )
            service.faqs.add(faq)
            count += 1
        return count

    def clear_existing_data(self):
        self.stdout.write(self.style.WARNING('⚠️  Tablolar temizleniyor...'))
        ServiceStep.objects.all().delete()
        Service.objects.all().delete()
        ServiceCategory.objects.all().delete()
    
    def print_summary(self, stats):
        self.stdout.write('\n' + '-' * 60)
        self.stdout.write(self.style.SUCCESS(f'✅ İŞLEM TAMAMLANDI'))
        self.stdout.write(f'   • Kategoriler: {stats["cats"]}')
        self.stdout.write(f'   • Hizmetler: {stats["new_serv"]} yeni, {stats["upd_serv"]} güncellendi')
        self.stdout.write(f'   • Alt Veriler: {stats["features"]} özellik, {stats["steps"]} adım, {stats["faqs"]} SSS eklendi.')
        self.stdout.write('=' * 60 + '\n')
