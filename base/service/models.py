from django.db import models
from django_summernote.fields import SummernoteTextField
from django.urls import reverse
from core.models import BaseSEOModel, Faq, Feature
from image_optimizer.fields import OptimizedImageField


class ServiceCategory(models.Model):
    """Hizmet kategorileri - anasayfada tab filtreleme için"""
    name = models.CharField(max_length=100, verbose_name='Kategori Adı')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    icon = models.CharField(max_length=50, blank=True, verbose_name='İkon', 
                           help_text='FontAwesome ikon adı (örn: fas fa-paint-brush)')
    order = models.PositiveIntegerField(default=0, verbose_name='Sıralama')
    is_active = models.BooleanField(default=True, verbose_name='Aktif mi?')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hizmet Kategorisi'
        verbose_name_plural = 'Hizmet Kategorileri'
        ordering = ['order', 'name']


class ServiceBase(BaseSEOModel):
    title = models.CharField(max_length=100 , verbose_name='Başlık')
    slug = models.SlugField(max_length=50, unique=True, null=True, verbose_name='URL' )
    description = SummernoteTextField(verbose_name='Açıklama')
    short_description = models.TextField(verbose_name='Kısa Açıklama')
    image = OptimizedImageField(upload_to='uploads/services', verbose_name='Resim', default='uploads/service_default.jpg')
    features = models.ManyToManyField(Feature, verbose_name='Özellikler', blank=True, related_name='%(class)s_features')
    faqs = models.ManyToManyField(Faq, verbose_name='Sıkça Sorulan Sorular', blank=True, related_name='%(class)s_faqs')
    isActive = models.BooleanField(default=True,verbose_name='Aktif mi?')
    showIndex = models.BooleanField(default=True,verbose_name='Anasayfa')
    created= models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("service_detail", args=[str(self.slug),])
    
    class Meta:
        abstract = True


class Service(ServiceBase):
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Kategori',
        related_name='services'
    )
    icon = models.CharField(max_length=50, verbose_name='İcon', blank=True, help_text='FontAwesome ikon adı (örn: fas fa-info)')
    
    before_image = OptimizedImageField(upload_to='uploads/services/transformations', blank=True, null=True, verbose_name='Öncesi Resim (Dönüşüm)')
    after_image = OptimizedImageField(upload_to='uploads/services/transformations', blank=True, null=True, verbose_name='Sonrası Resim (Dönüşüm)')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Hizmet'
        verbose_name_plural = 'Hizmetler'
        ordering = ['-created']


class ServiceStep(models.Model):
    """Hizmet süreç adımları (Örn: 1. Keşif, 2. Uygulama)"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='steps', verbose_name='Hizmet')
    step_number = models.PositiveIntegerField(verbose_name='Adım No', default=1)
    title = models.CharField(max_length=100, verbose_name='Başlık')
    description = models.TextField(verbose_name='Açıklama')
    
    class Meta:
        verbose_name = 'Süreç Adımı'
        verbose_name_plural = 'Süreç Adımları'
        ordering = ['step_number']

    def __str__(self):
        return f"{self.service.title} - Adım {self.step_number}"


class ServiceArea(ServiceBase):
    icon = models.CharField(max_length=50, verbose_name='İcon', blank=True, help_text='FontAwesome ikon adı (örn: fas fa-info)')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Hizmet Bölgesi'
        verbose_name_plural = 'Hizmet Bölgeleri'
        ordering = ['-created']




class ServiceHeader(models.Model):
    title = models.CharField(max_length=100, verbose_name='Başlık')
    description = SummernoteTextField( verbose_name='Açıklama')
    created= models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Hizmet Alanı'
        verbose_name_plural = 'Hizmet Alanı'
