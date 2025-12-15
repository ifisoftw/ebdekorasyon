from django.db import models
from django.utils import timezone
from core.models import BaseSEOModel
from django.urls import reverse
from django.contrib.auth.models import User
from image_optimizer.fields import OptimizedImageField
from django_summernote.fields import SummernoteTextField
# One to Many Realations with Blog
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Kategori', db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Etiket', db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Blog(BaseSEOModel):
    title = models.CharField(max_length=100 , verbose_name='Başlık')
    slug = models.SlugField(max_length=100, unique=True, null=True, verbose_name='URL', db_index=True)
    description = SummernoteTextField(verbose_name='Açıklama')
    short_description = models.TextField(verbose_name='Kısa Açıklama')
    image = models.ImageField(upload_to='uploads/blogs', verbose_name='Resim', default='uploads/blog.jpg')
    miniimage = models.ImageField(upload_to='uploads/blogs',blank=True, verbose_name='Küçük Resim (Opsiyonel)', default='uploads/blog.jpg')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Kategori') # Kategori silinirse blog korunur
    tags = models.ManyToManyField(Tag, blank=True, help_text='Birden fazla seçim yapmak için te "CTRL" veya "COMMAND" tuşuna basılı tutun.')
    isActive = models.BooleanField(default=True,verbose_name='Aktif mi?')
    showIndex = models.BooleanField(default=True,verbose_name='Anasayfa da gösterilsin mi?')
    created= models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)

    def get_date(self):
        time = timezone.now()


        if self.created.day == time.day:
            return str(time.hour - self.created.hour) + " saat önce"
        
        else:
            return str(time.day - self.created.day) + " gün önce"
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("blog_detail", args=[str(self.slug),])
    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Bloglar'
        ordering = ['-created']

