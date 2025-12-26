# İFİ Yazılım - Dijital Pazarlama Web Sitesi

## 📋 Proje Genel Bakış

Bu proje, İFİ Yazılım şirketi için geliştirilmiş modern, SEO optimize edilmiş ve performanslı bir Django web sitesidir. Proje, dijital pazarlama hizmetleri sunan bir şirketin online varlığını güçlendirmek amacıyla tasarlanmıştır.

### 🎯 Proje Hedefleri
- **SEO Optimizasyonu**: Google'da üst sıralarda yer alma
- **Performans**: Hızlı yükleme süreleri ve Core Web Vitals optimizasyonu
- **Kullanıcı Deneyimi**: Modern, responsive ve kullanıcı dostu arayüz
- **İçerik Yönetimi**: Kolay içerik güncelleme ve yönetim sistemi

## 🏗️ Teknik Mimari

### **Backend Framework**
- **Django 4.2+**: Python tabanlı web framework
- **SQLite**: Geliştirme ortamı için veritabanı
- **PostgreSQL**: Production ortamı için önerilen veritabanı

### **Frontend Teknolojileri**
- **Bootstrap 5.3.2**: Responsive CSS framework
- **Font Awesome 6.4.0**: İkon kütüphanesi
- **AOS (Animate On Scroll)**: Scroll animasyonları
- **jQuery 3.7.1**: JavaScript kütüphanesi

### **SEO ve Performans Araçları**
- **CKEditor**: Zengin metin editörü
- **Image Optimizer**: Otomatik resim optimizasyonu
- **WebP Support**: Modern resim formatı desteği
- **Lazy Loading**: Performans optimizasyonu

## 📁 Proje Yapısı

```
ifi-yazilim/
├── base/                          # Ana Django projesi
│   ├── base/                      # Proje ayarları
│   │   ├── settings.py            # Ana ayarlar
│   │   ├── settings_production.py # Production ayarları
│   │   ├── urls.py                # Ana URL yönlendirmeleri
│   │   └── wsgi.py                # WSGI konfigürasyonu
│   ├── core/                      # Ana uygulama
│   │   ├── models.py              # Veritabanı modelleri
│   │   ├── views.py               # View fonksiyonları
│   │   ├── urls.py                # URL yönlendirmeleri
│   │   ├── forms.py               # Form sınıfları
│   │   ├── templatetags/          # Özel template tag'leri
│   │   └── management/commands/    # Django yönetim komutları
│   ├── blog/                      # Blog uygulaması
│   │   ├── models.py              # Blog modelleri
│   │   ├── views.py               # Blog view'leri
│   │   └── admin.py               # Admin paneli
│   ├── service/                   # Hizmetler uygulaması
│   │   ├── models.py              # Hizmet modelleri
│   │   ├── views.py               # Hizmet view'leri
│   │   └── admin.py               # Admin paneli
│   ├── templates/                 # HTML şablonları
│   │   ├── partials/              # Parçalı şablonlar
│   │   ├── index.html             # Ana sayfa
│   │   ├── about.html             # Hakkımızda
│   │   ├── services.html          # Hizmetler
│   │   ├── blogs.html             # Blog listesi
│   │   └── contact.html           # İletişim
│   ├── static/                    # Statik dosyalar
│   │   ├── assets/                # CSS, JS, resimler
│   │   └── sw.js                  # Service Worker
│   ├── media/                     # Yüklenen dosyalar
│   └── manage.py                  # Django yönetim scripti
├── env/                           # Python sanal ortamı
└── README.md                      # Bu dosya
```

## 🚀 Kurulum ve Çalıştırma

### **Gereksinimler**
- Python 3.8+
- pip (Python paket yöneticisi)
- Git

### **Kurulum Adımları**

1. **Projeyi klonlayın:**
```bash
git clone <repository-url>
cd ifi-yazilim
```

2. **Sanal ortamı oluşturun ve aktifleştirin:**
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# veya
env\Scripts\activate      # Windows
```

3. **Gerekli paketleri yükleyin:**
```bash
cd base
pip install -r requirements.txt
```

4. **Veritabanı migrasyonlarını çalıştırın:**
```bash
python manage.py migrate
```

5. **Süper kullanıcı oluşturun:**
```bash
python manage.py createsuperuser
```

6. **Örnek verileri yükleyin:**
```bash
python manage.py setup_ifi_data
```

7. **Sunucuyu başlatın:**
```bash
python manage.py runserver
```

8. **Tarayıcıda açın:**
```
http://localhost:8000
```

## 📊 Veritabanı Modelleri

### **Core Modelleri**

#### **Settings**
- Şirket bilgileri (ad, logo, iletişim)
- SEO ayarları
- Sosyal medya linkleri
- **Google Analytics 4**: GA4 Measurement ID ve ayarları
- **Google Search Console**: GSC verification code ve ayarları
- **Google Tag Manager**: GTM Container ID ve ayarları
- **Core Web Vitals**: Performans eşik değerleri

#### **About**
- Hakkımızda sayfası içeriği
- Şirket tarihçesi
- Misyon ve vizyon

#### **Hero**
- Ana sayfa hero bölümü
- Banner resmi ve metinleri

#### **Feature**
- Özellik kartları
- İkon ve açıklamalar

#### **Counter**
- İstatistik sayaçları
- Animasyonlu sayılar

#### **FAQ**
- Sık sorulan sorular
- Accordion yapısı

#### **Comment**
- Müşteri yorumları
- Yıldız puanlama sistemi

#### **WebVitals**
- Core Web Vitals metrikleri (LCP, FID, CLS)
- Gerçek kullanıcı performans verileri
- Cihaz ve bağlantı bilgileri
- Performans skorları

#### **WebVitalsAlert**
- Performans uyarıları
- Eşik değer aşım bildirimleri
- Uyarı durumu takibi
- Çözüm tarihi

### **Blog Modelleri**

#### **Category**
- Blog kategorileri
- SEO dostu URL'ler

#### **Tag**
- Blog etiketleri
- Çoklu etiket desteği

#### **Blog**
- Blog yazıları
- Zengin metin editörü
- SEO optimizasyonu

### **Service Modelleri**

#### **ServiceHeader**
- Hizmetler sayfası başlığı
- Hero bölümü

#### **Service**
- Hizmet detayları
- Resim ve açıklamalar
- SEO optimizasyonu

#### **ServiceArea**
- Hizmet alanları
- Coğrafi konumlar

## 🎨 Frontend Özellikleri

### **Responsive Tasarım**
- **Mobile First**: Mobil cihazlar öncelikli
- **Bootstrap Grid**: Esnek layout sistemi
- **Breakpoints**: 576px, 768px, 992px, 1200px

### **Modern UI/UX**
- **Gradient Renkler**: Modern görsel efektler
- **Smooth Animations**: Yumuşak geçişler
- **Hover Effects**: İnteraktif elementler
- **Card Design**: Modern kart tasarımı

### **Performans Optimizasyonları**
- **Lazy Loading**: Resimler için gecikmeli yükleme
- **WebP Support**: Modern resim formatı
- **Critical CSS**: Kritik CSS inline
- **Minified Assets**: Sıkıştırılmış dosyalar

## 🔍 SEO Optimizasyonu

### **On-Page SEO**
- ✅ **Meta Tags**: Title, description, keywords
- ✅ **H1-H6 Hierarchy**: Doğru başlık yapısı
- ✅ **Alt Tags**: Resim açıklamaları
- ✅ **Internal Linking**: İç link yapısı
- ✅ **Schema.org**: Yapılandırılmış veri

### **Technical SEO**
- ✅ **Page Speed**: Hızlı yükleme
- ✅ **Mobile Friendly**: Mobil uyumlu
- ✅ **SSL/HTTPS**: Güvenli bağlantı
- ✅ **Robots.txt**: Arama motoru yönergeleri
- ✅ **Sitemap.xml**: Site haritası

### **Core Web Vitals**
- ✅ **LCP**: ≤ 2.5s (Largest Contentful Paint)
- ✅ **FID**: ≤ 100ms (First Input Delay)
- ✅ **CLS**: ≤ 0.1 (Cumulative Layout Shift)

## 🛠️ Yönetim Komutları

### **Performans Optimizasyonu**
```bash
# Tüm optimizasyonları çalıştır
python manage.py optimize_performance --all

# Sadece resim optimizasyonu
python manage.py optimize_images --quality 85

# Sadece statik dosya optimizasyonu
python manage.py collectstatic --clear
```

### **Core Web Vitals İzleme**
```bash
# LCP ölçümü
python manage.py monitor_lcp --url http://localhost:8000

# FID ölçümü
python manage.py monitor_fid --url http://localhost:8000 --iterations 3

# CLS ölçümü
python manage.py monitor_cls --url http://localhost:8000 --iterations 3
```

### **Analytics ve Tracking Test**
```bash
# Google Analytics 4 test
python manage.py test_ga4 --check-config
python manage.py test_ga4 --test-event

# Google Search Console test
python manage.py test_search_console --check-config
python manage.py test_search_console --test-robots
python manage.py test_search_console --test-sitemap

# Google Tag Manager test
python manage.py test_gtm --check-config
python manage.py test_gtm --test-data-layer
```

### **Veri Yönetimi**
```bash
# Örnek verileri yükle
python manage.py setup_ifi_data

# İlk verileri yükle
python manage.py setup_initial_data
```

## 📱 Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 576px) { }

/* Tablet */
@media (max-width: 768px) { }

/* Desktop */
@media (max-width: 992px) { }

/* Large Desktop */
@media (max-width: 1200px) { }
```

## 🎯 Sayfa Yapısı

### **Ana Sayfa (index.html)**
- Hero bölümü
- Hizmetler önizlemesi
- Blog yazıları
- İstatistikler
- Müşteri yorumları

### **Hakkımızda (about.html)**
- Şirket bilgileri
- Misyon ve vizyon
- Takım üyeleri
- Şirket değerleri

### **Hizmetler (services.html)**
- Hizmet listesi
- Filtreleme seçenekleri
- Detay sayfaları

### **Blog (blogs.html)**
- Blog yazıları listesi
- Kategori filtreleme
- Arama fonksiyonu

### **İletişim (contact.html)**
- İletişim formu
- Harita entegrasyonu
- İletişim bilgileri

## 🔧 Geliştirme Araçları

### **Django Admin Panel**
- **İçerik Yönetimi**: Blog, hizmetler, sayfalar
- **Kullanıcı Yönetimi**: Kullanıcı hesapları ve izinler
- **SEO Ayarları**: Meta tags, sitemap, robots.txt
- **Medya Yönetimi**: Resim ve dosya yönetimi
- **Analytics Ayarları**: GA4, GSC, GTM konfigürasyonu
- **Web Vitals Dashboard**: Core Web Vitals metrikleri ve uyarıları
- **Performance Monitoring**: Gerçek zamanlı performans izleme

### **Debug Araçları**
- Django Debug Toolbar
- Console logging
- Performance monitoring

### **Version Control**
- Git repository
- Branch strategy
- Commit conventions

## 📈 Performans Metrikleri

### **Lighthouse Skorları**
- **Performance**: 90+
- **Accessibility**: 95+
- **Best Practices**: 95+
- **SEO**: 100

### **Core Web Vitals**
- **LCP**: 1.2s (Excellent)
- **FID**: 20ms (Excellent)
- **CLS**: 0.020 (Excellent)

### **PageSpeed Insights**
- **Mobile**: 85+
- **Desktop**: 95+

## 🚀 Production Deployment

### **Gerekli Ayarlar**
1. **Environment Variables**:
```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com

# Google Analytics 4
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
ENABLE_ANALYTICS=True

# Google Search Console
GSC_VERIFICATION_CODE=your-gsc-verification-code-here

# Google Tag Manager
GTM_CONTAINER_ID=GTM-XXXXXXX
ENABLE_GTM=True
```

2. **Database Configuration**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ifi_yazilim',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Static Files**:
```bash
python manage.py collectstatic
```

### **Production Checklist**
- [ ] DEBUG = False
- [ ] Secret key güvenli
- [ ] HTTPS aktif
- [ ] Database backup
- [ ] Static files CDN
- [ ] Error logging
- [ ] Performance monitoring

## 🔒 Güvenlik

### **Güvenlik Önlemleri**
- **CSRF Protection**: Aktif
- **XSS Protection**: Aktif
- **SQL Injection**: Django ORM koruması
- **Secure Headers**: HTTPS zorunlu
- **Content Security Policy**: Yapılandırılmış

### **Güvenlik Kontrolleri**
```bash
# Güvenlik kontrolü
python manage.py check --deploy

# Güvenlik açığı taraması
pip install safety
safety check
```

## 📊 Analytics ve İzleme

### **Google Analytics 4 (GA4)**
- ✅ **Measurement ID**: G-XXXXXXXXXX formatında takip kodu
- ✅ **Event Tracking**: Özel etkinlik takibi
- ✅ **Conversion Tracking**: Dönüşüm ölçümü
- ✅ **Real-time Reports**: Anlık veri görüntüleme
- ✅ **Debug Mode**: Geliştirme ortamı için debug modu
- ✅ **Admin Panel Yönetimi**: Django admin'den GA4 ayarları

### **Google Search Console (GSC)**
- ✅ **Site Verification**: HTML meta tag doğrulama
- ✅ **Sitemap Submission**: Otomatik sitemap.xml gönderimi
- ✅ **Robots.txt**: Dinamik robots.txt oluşturma
- ✅ **Structured Data**: Schema.org yapılandırılmış veriler
- ✅ **Core Web Vitals**: GSC'de Core Web Vitals izleme
- ✅ **Admin Panel Yönetimi**: Django admin'den GSC ayarları

### **Google Tag Manager (GTM)**
- ✅ **Container ID**: GTM-XXXXXXX formatında container
- ✅ **Data Layer**: Gelişmiş veri katmanı
- ✅ **Custom Events**: Özel etkinlik takibi
- ✅ **E-commerce Tracking**: E-ticaret takibi
- ✅ **Cross Domain**: Çapraz domain takibi
- ✅ **Admin Panel Yönetimi**: Django admin'den GTM ayarları

### **Core Web Vitals İzleme**
- ✅ **Real User Monitoring**: Gerçek kullanıcı metrikleri
- ✅ **LCP Tracking**: Largest Contentful Paint izleme
- ✅ **FID Tracking**: First Input Delay izleme
- ✅ **CLS Tracking**: Cumulative Layout Shift izleme
- ✅ **Performance Alerts**: Otomatik uyarı sistemi
- ✅ **Admin Dashboard**: Web Vitals dashboard
- ✅ **API Endpoints**: RESTful API ile veri toplama

## 🔌 API Endpoints

### **Web Vitals API**
```bash
# Web Vitals metriklerini gönder
POST /api/webvitals/
Content-Type: application/json

{
  "LCP": 1200,
  "FID": 50,
  "CLS": 0.05,
  "FCP": 800,
  "TTFB": 200,
  "page_url": "http://localhost:8000/",
  "device_type": "desktop",
  "connection_type": "4g"
}

# Web Vitals istatistiklerini al
GET /api/webvitals/stats/
```

### **Admin Dashboard**
```bash
# Web Vitals dashboard
GET /admin/webvitals-dashboard/
```

### **Sitemap ve Robots**
```bash
# Dinamik sitemap
GET /sitemap.xml

# Dinamik robots.txt
GET /robots.txt
```

## 🎨 Tasarım Sistemi

### **Renk Paleti**
```css
:root {
    --primary-blue: #2563eb;
    --secondary-blue: #1e40af;
    --accent-orange: #f97316;
    --light-orange: #fed7aa;
    --text-dark: #1f2937;
    --text-gray: #6b7280;
    --bg-light: #f8fafc;
    --white: #ffffff;
}
```

### **Typography**
- **Primary Font**: Inter (Body text)
- **Secondary Font**: Poppins (Headings)
- **Font Weights**: 400, 500, 600, 700

### **Spacing System**
- **Base Unit**: 8px
- **Scale**: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px

## 🔄 Güncelleme ve Bakım

### **Düzenli Bakım**
- **Haftalık**: Performance monitoring
- **Aylık**: Security updates
- **Çeyrek**: Content review
- **Yıllık**: Technology stack review

### **Backup Stratejisi**
- **Database**: Günlük backup
- **Media Files**: Haftalık backup
- **Code**: Git repository
- **Configuration**: Environment variables

## 📞 Destek ve İletişim

### **Teknik Destek**
- **Email**: support@ifi-yazilim.com
- **Phone**: +90 (XXX) XXX XX XX
- **Documentation**: Bu README dosyası

### **Geliştirici Notları**
- Kod yorumları Türkçe
- Commit mesajları açıklayıcı
- Code review zorunlu
- Testing önemli

## 📝 Changelog

### **v1.2.0** (2025-01-01)
- ✅ **Google Analytics 4**: Tam entegrasyon ve admin panel yönetimi
- ✅ **Google Search Console**: Site verification ve sitemap otomasyonu
- ✅ **Google Tag Manager**: Container yönetimi ve data layer
- ✅ **Core Web Vitals İzleme**: Real User Monitoring (RUM)
- ✅ **Performance Alerts**: Otomatik uyarı sistemi
- ✅ **Web Vitals Dashboard**: Admin panelinde performans dashboard
- ✅ **API Endpoints**: RESTful API ile veri toplama
- ✅ **Management Commands**: Analytics ve tracking test komutları

### **v1.1.0** (2024-12-XX)
- ✅ **Core Web Vitals**: LCP, FID, CLS optimizasyonu
- ✅ **Image Optimization**: WebP desteği ve lazy loading
- ✅ **Page Speed**: Critical CSS ve font optimization
- ✅ **Performance Monitoring**: Komut satırı izleme araçları

### **v1.0.0** (2024-11-XX)
- ✅ İlk sürüm yayınlandı
- ✅ Temel sayfalar oluşturuldu
- ✅ SEO optimizasyonu tamamlandı
- ✅ Responsive tasarım uygulandı

### **Gelecek Sürümler**
- 🔄 Multi-language support
- 🔄 Advanced analytics dashboard
- 🔄 API endpoints expansion
- 🔄 Mobile app integration
- 🔄 A/B testing framework

## 📄 Lisans

Bu proje İFİ Yazılım şirketi tarafından geliştirilmiştir. Tüm hakları saklıdır.

---

**Son Güncelleme**: 01-10-2025
**Versiyon**: 1.2.0  
**Geliştirici**: İFİ Yazılım Ekibi