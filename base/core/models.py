from django.db import models
from django_summernote.fields import SummernoteTextField
from image_optimizer.fields import OptimizedImageField
from django.utils import timezone


class BaseSEOModel(models.Model):
    seo_title = models.CharField(max_length=60,blank=True, verbose_name="SEO Başlık")
    seo_description = models.CharField(max_length=160,blank=True, verbose_name="SEO Açıklama")

    class Meta:
        abstract = True

class Settings(BaseSEOModel):
    name = models.CharField(max_length=100 ,blank=True, verbose_name='Şirket Adı')
    domain = models.CharField(max_length=100 ,blank=True, verbose_name='Domain Adresi')
    logo = OptimizedImageField(upload_to='uploads',blank=True,verbose_name='Logo')
    logowhite = OptimizedImageField(upload_to='uploads',blank=True,verbose_name='Logo(Beyaz Yüzey)')
    favicon = OptimizedImageField(upload_to='uploads',blank=True,verbose_name='Favicon')
    phone = models.CharField(max_length=100, blank=True, verbose_name='Telefon')
    whatsapp = models.CharField(max_length=100, blank=True, verbose_name='Whatsapp')
    email = models.EmailField(max_length=254, blank=True, verbose_name='E Posta')
    adress = models.TextField(blank=True, verbose_name='Adres')
    facebook = models.URLField(max_length=200, blank=True, verbose_name='Facebook')
    instagram = models.URLField(max_length=200, blank=True, verbose_name='Instagram')
    twitter = models.URLField(max_length=200, blank=True, verbose_name='Twitter')
    
    # Schema Markup için dinamik alanlar
    alternate_name = models.CharField(max_length=200, blank=True, verbose_name='Alternatif İsim', default='İFİ Yazılım Dijital Pazarlama')
    city = models.CharField(max_length=100, blank=True, verbose_name='Şehir', default='İstanbul')
    region = models.CharField(max_length=100, blank=True, verbose_name='Bölge', default='İstanbul')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Posta Kodu', default='34000')
    country = models.CharField(max_length=10, blank=True, verbose_name='Ülke Kodu', default='TR')
    latitude = models.CharField(max_length=20, blank=True, verbose_name='Enlem', default='41.0082')
    longitude = models.CharField(max_length=20, blank=True, verbose_name='Boylam', default='28.9784')
    opening_hours = models.JSONField(default=list, blank=True, verbose_name='Çalışma Saatleri', help_text='JSON formatında çalışma saatleri (örn: ["Mo-Fr 09:00-18:00"])')
    price_range = models.CharField(max_length=10, blank=True, verbose_name='Fiyat Aralığı', default='$$')
    payment_accepted = models.CharField(max_length=200, blank=True, verbose_name='Kabul Edilen Ödeme Yöntemleri', default='Cash, Credit Card, Bank Transfer')
    currencies_accepted = models.CharField(max_length=50, blank=True, verbose_name='Kabul Edilen Para Birimleri', default='TRY, USD, EUR')
    founding_date = models.CharField(max_length=10, blank=True, verbose_name='Kuruluş Tarihi', default='2021')
    founder_name = models.CharField(max_length=200, blank=True, verbose_name='Kurucu Adı', default='İFİ Yazılım Kurucuları')
    number_of_employees = models.CharField(max_length=50, blank=True, verbose_name='Çalışan Sayısı', default='5-10')
    service_radius = models.CharField(max_length=20, blank=True, verbose_name='Hizmet Yarıçapı (metre)', default='100000')
    average_rating = models.CharField(max_length=10, blank=True, verbose_name='Ortalama Puan', default='4.8')
    review_count = models.CharField(max_length=10, blank=True, verbose_name='Yorum Sayısı', default='25')
    contact_type = models.CharField(max_length=50, blank=True, verbose_name='İletişim Türü', default='customer service')
    price_currency = models.CharField(max_length=10, blank=True, verbose_name='Para Birimi', default='TRY')
    country_name = models.CharField(max_length=50, blank=True, verbose_name='Ülke Adı', default='Turkey')
    city_name = models.CharField(max_length=50, blank=True, verbose_name='Şehir Adı', default='İstanbul')
    
    # Takip Kodları
    head_scripts = models.TextField(blank=True, verbose_name="Head Kodları", help_text="<head> etiketi içine eklenecek kodlar (Google Analytics, Meta Pixel vb.)")
    body_scripts = models.TextField(blank=True, verbose_name="Body Kodları", help_text="<body> etiketinin sonuna eklenecek kodlar")

    # Google Search Console Settings - Sadece doğrulama ve site haritası ayarları kalsın

    enable_sitemap = models.BooleanField(
        default=True, 
        verbose_name='Sitemap Aktif',
        help_text='Otomatik sitemap.xml oluşturmayı aktifleştir'
    )
    enable_robots_txt = models.BooleanField(
        default=True, 
        verbose_name='Robots.txt Aktif',
        help_text='Otomatik robots.txt oluşturmayı aktifleştir'
    )
    enable_structured_data = models.BooleanField(
        default=True, 
        verbose_name='Structured Data Aktif',
        help_text='Schema.org yapılandırılmış verilerini aktifleştir'
    )
    

    created= models.DateTimeField(auto_now_add= True, verbose_name="Oluşturulma Tarihi")
    updated = models.DateTimeField(auto_now=True,verbose_name="Güncellenme Tarihi" )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Ayar'
        verbose_name_plural = 'Genel Ayarlar'

class Counter(models.Model):
    name = models.CharField(max_length=100, verbose_name='Sayaç Adı')
    count = models.CharField(max_length=10, verbose_name='Sayaç Değeri')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Sayaç İkonu', help_text='FontAwesome ikon adı (örn: fas fa-info)')
    created= models.DateTimeField(auto_now_add= True, verbose_name="Oluşturulma Tarihi")
    updated = models.DateTimeField(auto_now=True,verbose_name="Güncellenme Tarihi" )

    def __str__(self) :
        return self.name
    
    class Meta:
        verbose_name = 'Sayaç'
        verbose_name_plural = 'Sayaçlar'

class Hero(models.Model):
    # Ana başlık ve alt başlık
    title = models.CharField(max_length=250, verbose_name='Ana Başlık', default='')
    subtitle = models.CharField(max_length=250, verbose_name='Alt Başlık', default='')
    description = models.TextField(verbose_name='Açıklama', default='')
    
    # Birincil buton
    primary_button_text = models.CharField(max_length=100, blank=True, verbose_name='Birincil Buton Yazısı')
    primary_button_link = models.URLField(max_length=200, blank=True, verbose_name='Birincil Buton Linki')
    primary_button_icon = models.CharField(max_length=50, blank=True, verbose_name='Birincil Buton İkonu', help_text='FontAwesome ikon adı (örn: fas fa-rocket)')
    
    # İkincil buton
    secondary_button_text = models.CharField(max_length=100, blank=True, verbose_name='İkincil Buton Yazısı')
    secondary_button_link = models.URLField(max_length=200, blank=True, verbose_name='İkincil Buton Linki')
    secondary_button_icon = models.CharField(max_length=50, blank=True, verbose_name='İkincil Buton İkonu', help_text='FontAwesome ikon adı (örn: fas fa-play)')
    
    # Hero resmi
    banner = OptimizedImageField(upload_to='uploads/Hero', blank=True, verbose_name='Hero Resmi')
    
    # İstatistikler
    counters = models.ManyToManyField(Counter, verbose_name='Sayaçlar', related_name='hero_counters') 
    # Durum ve tarihler
    is_active = models.BooleanField(default=True, verbose_name='Aktif mi?')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Hero'
        verbose_name_plural = 'Herolar'

#FEATURE AREA
class Feature(models.Model):
    name = models.CharField(max_length=100, verbose_name='Başlık')
    description = models.TextField(verbose_name='Açıklama', blank=True)
    icon = models.CharField(max_length=50, verbose_name='İcon', blank=True, help_text='FontAwesome ikon adı (örn: fas fa-info)')
    created= models.DateTimeField(auto_now_add= True, verbose_name="Oluşturulma Tarihi")
    updated = models.DateTimeField(auto_now=True,verbose_name="Güncellenme Tarihi" )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Özellik'
        verbose_name_plural = 'Özellikler'

class FeatureArea(models.Model):
    header = models.CharField(max_length=100, verbose_name='Üst Başlık')
    title = models.CharField(max_length=100, verbose_name='Başlık')
    short_description = models.TextField(verbose_name='Kısa Açıklama')
    features = models.ManyToManyField(Feature, verbose_name='Özellikler')
    created= models.DateTimeField(auto_now_add= True, verbose_name="Oluşturulma Tarihi")
    updated = models.DateTimeField(auto_now=True,verbose_name="Güncellenme Tarihi" )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Neden Bizi Seçmelisiniz'
        verbose_name_plural = 'Neden Bizi Seçmelisiniz'
#FEATURE AREA

class About(BaseSEOModel):
    header = models.CharField(max_length=100 ,blank=True, null=True, verbose_name='Başlık')
    title = models.CharField(max_length=100 ,blank=True, null=True, verbose_name='Slogan')
    description = SummernoteTextField(verbose_name='Açıklama')
    short_description = models.TextField(verbose_name='Kısa Açıklama')
    features = models.ManyToManyField(Feature, verbose_name='Özellikler')
    counters = models.ManyToManyField(Counter, verbose_name='Sayaçlar', related_name='about_counters') 
    mission = models.TextField(verbose_name='Misyon')
    vision = models.TextField(verbose_name='Vizyon')
    image = OptimizedImageField(upload_to='uploads/about',blank=True, null=True,verbose_name='Hakkımızda Resim')
    created= models.DateTimeField(auto_now_add= True, verbose_name="Oluşturulma Tarihi")
    updated = models.DateTimeField(auto_now=True,verbose_name="Güncellenme Tarihi")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Hakkımızda'
        verbose_name_plural = 'Hakkımızda'

class Comment(models.Model):
    name = models.CharField(max_length=100, verbose_name='İsim')
    title = models.CharField(max_length=100, verbose_name='Ünvan')
    comment = models.TextField(verbose_name="Yorum")
    created= models.DateTimeField(auto_now_add= True, verbose_name="Oluşturulma Tarihi")
    updated = models.DateTimeField(auto_now=True,verbose_name="Güncellenme Tarihi")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Müşteri Yorumu'
        verbose_name_plural = 'Müşteri Yorumları'

class CommentHeader(models.Model):
    title = models.CharField(max_length=100, verbose_name='Başlık')
    description = models.CharField(max_length=100, verbose_name='Açıklama')
    created= models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Müşteri Yorumu Alanı'
        verbose_name_plural = 'Müşteri Yorumu Alanı'

class Contact(models.Model):
    name = models.CharField(max_length=100 , verbose_name='İsim Soyisim')
    email = models.EmailField(max_length=254,blank=True,verbose_name='E Posta')
    phone = models.CharField(max_length=254 , verbose_name='Telefon')
    subject = models.CharField(max_length=254 , verbose_name='Konu', blank=True)
    message = models.TextField(verbose_name='Açıklama',blank=True)
    isRead = models.BooleanField(default=False,verbose_name='Okundu mu?')
    created= models.DateTimeField(auto_now_add= True, verbose_name="Oluşturulma Tarihi")


    def __str__(self):
        return self.name
    class Meta:
        managed = True
        verbose_name = 'İletişim Formu'
        verbose_name_plural = 'İletişim Formu'

class Faq(models.Model):
    question = models.CharField(max_length=256 , verbose_name='Soru')
    answer = models.TextField(verbose_name='Cevap')
    isActive = models.BooleanField(default=True,verbose_name='Aktif mi?')
    showIndex = models.BooleanField(default=True,verbose_name='Anasayfa da gösterilsin mi?')
    created= models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.question
    
    class Meta:
        verbose_name = 'SSS'
        verbose_name_plural = 'Sıkça Sorulan Sorular'

class Page_Seo(BaseSEOModel):
    page_url = models.CharField(max_length=100, verbose_name='Sayfa Url')

    def __str__(self):
        return self.page_url
    
    class Meta:
        verbose_name = 'SEO Ayarı'
        verbose_name_plural = 'SEO Ayarları'


class Report(models.Model):
     title = models.CharField(max_length=100)
     description = models.TextField()
     cost = models.IntegerField()
     create_at = models.DateTimeField(auto_now_add=True)
     def __str__(self):
         return self.title


class Project(models.Model):
    """Tamamlanan projeler - portfolyo için"""
    title = models.CharField(max_length=200, verbose_name='Proje Başlığı')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Açıklama')
    location = models.CharField(max_length=100, verbose_name='Konum', help_text='Örn: Kadıköy, İstanbul')
    
    # Görsel alanları
    image = OptimizedImageField(upload_to='uploads/projects', verbose_name='Ana Görsel')
    before_image = OptimizedImageField(upload_to='uploads/projects', blank=True, null=True, verbose_name='Öncesi Görseli')
    after_image = OptimizedImageField(upload_to='uploads/projects', blank=True, null=True, verbose_name='Sonrası Görseli')
    
    # Kategori ilişkisi - service app'ten import edemiyoruz circular import olur, string kullanacağız
    category = models.CharField(max_length=100, verbose_name='Kategori', help_text='Örn: Mobilya Boyama')
    
    # Durum alanları
    is_featured = models.BooleanField(default=False, verbose_name='Öne Çıkan')
    show_on_index = models.BooleanField(default=True, verbose_name='Anasayfada Göster')
    is_active = models.BooleanField(default=True, verbose_name='Aktif mi?')
    
    # Tarih alanları
    completed_date = models.DateField(verbose_name='Tamamlanma Tarihi', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Proje'
        verbose_name_plural = 'Projeler'
        ordering = ['-is_featured', '-created']
