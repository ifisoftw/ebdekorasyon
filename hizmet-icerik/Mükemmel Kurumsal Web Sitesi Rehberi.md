İFİ Yazılım - Kurumsal Web Sitesi Mükemmellik Kılavuzu (2025 Standartları)

Bu doküman, sıradan bir web sitesi ile "mükemmel" bir dijital varlık arasındaki farkı belirleyen teknik, tasarımsal ve stratejik kriterleri içerir. Tüm maddeler 2025 yılı son çeyrek verilerine, Google algoritmalarına (SGE), Avrupa Birliği yasal standartlarına (EAA) ve Sürdürülebilir Web (Green Web) manifestosuna göre derlenmiştir.

1. Teknik Performans ve Altyapı (Hızın Ötesinde Tepkisellik)

Google ve kullanıcılar artık sadece "yükleme" hızına değil, "etkileşim" ve "işleme" hızına odaklanmaktadır.

1.1. Core Web Vitals (2025 Q4 Metrikleri)

INP (Interaction to Next Paint) < 200ms:

Nedir: Kullanıcının tıklaması ile tarayıcının görsel tepki vermesi arasındaki süre. Mart 2024'te FID'nin yerini aldı.

Kritik Aksiyon: Ana thread'i bloklayan JavaScript görevleri (Long Tasks) parçalanmalı (Task Splitting). requestIdleCallback kullanılarak işlemci rahatlatılmalı.

LCP (Largest Contentful Paint) < 2.5s:

Nedir: Ekrandaki en büyük içeriğin yüklenme süresi.

Kritik Aksiyon: Hero görseli asla "Lazy Load" yapılmamalı; fetchpriority="high" etiketi ile önceliklendirilmelidir.

CLS (Cumulative Layout Shift) < 0.1:

Nedir: Görsel kararlılık.

Kritik Aksiyon: Tüm medya ögeleri (<img>, <video>, <iframe>) için HTML içinde width ve height değerleri rezerve edilmeli. Font yüklemesinde font-display: swap standart olmalı.

1.2. Modern Dağıtım ve Sıkıştırma

Edge Caching & CDN: Statik dosyalar sadece sunucudan değil, kullanıcının konumuna en yakın "Edge" sunucusundan (Cloudflare, AWS CloudFront) sunulmalıdır.

Görsel Formatı: AVIF: JPEG/PNG yerine, WebP'den %20 daha verimli olan AVIF formatı "varsayılan" olmalı, WebP "fallback" olarak sunulmalıdır.

Sıkıştırma: Metin tabanlı dosyalar (HTML/CSS/JS) için Gzip yerine Brotli (br) algoritması kullanılmalıdır.

2. AI-Ready SEO ve SGE (Search Generative Experience)

Arama motorları artık "arama" değil "cevaplama" motoruna dönüştü. Siteniz, Google'ın Yapay Zeka özetlerinde (AI Snapshots) yer alacak şekilde optimize edilmelidir.

2.1. Zero-Click Optimizasyonu ve Varlıklar

Google SGE, kullanıcı siteye girmeden cevabı verir. Markanızın orada görünmesi "Otorite" sinyalidir.

Soru-Cevap Yapısı: İçerikler, "Nedir?", "Nasıl Yapılır?" gibi sorulara net, doğrudan paragraflarla (40-60 kelime) cevap vermelidir.

Entity (Varlık) Güçlendirme: Hakkımızda sayfasında firmanın uzmanlık alanları, "Entity" olarak tanımlanmalı ve sektörel terminoloji ile desteklenmelidir.

2.2. İleri Seviye Schema Markup (JSON-LD)

Organization: sameAs ile tüm sosyal medya, LinkedIn ve Wikipedia profilleri bağlanarak bilgi grafiği (Knowledge Graph) beslenmelidir.

Service & Product: Her hizmet sayfası, areaServed (Hizmet Bölgesi) ve audience (Hedef Kitle) özelliklerini içeren Service şemasına sahip olmalıdır.

2.3. Bilgi Kazancı (Information Gain)

Kural: İçerik, internetteki diğer 10 makalenin kopyası olamaz. Masaya "yeni" bir veri, vaka analizi veya uzman görüşü koymalıdır.

3. Evrensel Erişim ve Yasal Uyum (Global Standartlar)

2025 itibarıyla erişilebilirlik, özellikle AB pazarı için hukuki bir zorunluluktur (European Accessibility Act).

3.1. WCAG 2.2 (Level AA) Uyumluluğu

Odak Görünürlüğü (Focus Appearance): Site sadece klavye (Tab tuşu) ile gezilebilmelidir. Odaklanılan ögenin çevresindeki kontur belirgin olmalıdır.

Hedef Boyutları: Dokunmatik ekranlarda tıklanabilir alanlar en az 24x24 CSS piksel olmalıdır.

3.2. Yasal Metinler ve Rıza

EAA (European Accessibility Act): Haziran 2025'te yürürlüğe girdi. AB müşterisi olan siteler tam uyumlu olmak zorundadır.

Consent Mode v2: Google Ads/Analytics verileri için "Advanced Consent Mode" kurulumu zorunludur.

4. Dijital Sürdürülebilirlik (Green Web)

Kurumsal itibarın yeni göstergesi "Dijital Karbon Ayak İzi"dir.

Eco-Friendly Design:

Karanlık Mod (Dark Mode) varsayılan veya kolay erişilebilir olmalı (OLED ekranlarda enerji tasarrufu sağlar).

Gereksiz ağır scriptler ve otomatik oynayan videolar kaldırılmalı.

Sürdürülebilirlik Sayfası: Sitenin "Düşük Karbonlu" tasarlandığına dair bir bilgilendirme rozeti (Website Carbon Badge) footer'a eklenebilir.

5. Siber Güvenlik ve Kod Hijyeni (OWASP 2025)

5.1. HTTP Güvenlik Başlıkları

Sunucu yanıtında şu başlıklar zorunludur:

Strict-Transport-Security (HSTS)

Content-Security-Policy (CSP) (XSS koruması için beyaz liste)

Permissions-Policy (Kamera/Mikrofon erişimini kısıtlar)

5.2. Tedarik Zinciri ve API Güvenliği

SRI (Subresource Integrity): CDN kütüphaneleri için hash kontrolü.

Dependency Audit: Canlıya çıkmadan önce pip audit veya npm audit ile paket güvenlik taraması.

Rate Limiting: Django tarafında API ve form gönderimlerine IP tabanlı kısıtlama (django-ratelimit) uygulanmalı.

6. İFİ Yazılım Django Altyapısı ile Entegrasyon

Mevcut Django (4.2 / 5.x / 6.x) altyapınız için özelleştirilmiş aksiyonlar:

6.1. Backend (Django) Yapılandırması

Middleware: django-csp ve django-feature-policy paketleri middleware sıralamasında en üstlere eklenmeli.

Görsel Motoru: django-image-optimizer paketinin arka planda libavif kütüphanesini kullandığından emin olunmalı. Sunucuda sudo apt-get install libavif-bin gerekebilir.

Cache Stratejisi: Dinamik olmayan sayfalar (Hakkımızda, İletişim) için UpdateCacheMiddleware ve FetchFromCacheMiddleware aktif edilmeli.

6.2. Frontend & AI Prompting Stratejisi

AI araçları (Cursor/Windsurf) ile çalışırken şu prompt'u kullanın:

"Django Template oluştururken;

Görseller için picture etiketi ile AVIF öncelikli yapı kur.

Service modelinden gelen veriyi Google 'Service' JSON-LD şemasına uygun olarak head bloğuna bas.

Butonları WCAG 2.2 AA (min 44x44px fiziksel, 24px CSS) standardına uygun boyutlandır."

7. Kalite Kontrol (QA) ve CI/CD

Manuel testler artık yeterli değildir. Süreç otomatize edilmelidir.

Lighthouse CI: Her Git push işleminde Google Lighthouse skorunun (SEO, Performance, Accessibility) 90'ın altına düşmediğini kontrol eden bir GitHub Action/Gitlab CI pipeline'ı kurulmalı.

Otomatik Güvenlik Taraması: OWASP ZAP veya Snyk, CI sürecine entegre edilmeli.

Son Kontrol:

[ ] Google PageSpeed > 90 (Mobil)

[ ] Rich Results Test: Hata Yok

[ ] Console Errors: Temiz

Hazırlayan: İFİ Yazılım Dijital Mükemmeliyet Asistanı