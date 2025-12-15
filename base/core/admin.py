from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Report, Project
from .resource import ReportResource
from . models import Settings, About, Hero, FeatureArea, Feature, Comment, CommentHeader, Faq, Contact, Page_Seo, Counter

@admin.register(Settings)
class SettingsAdmin(ImportExportModelAdmin):
    list_display = ('name', 'domain', 'updated', 'created')
    list_filter = ('enable_sitemap', 'enable_robots_txt', 'created', 'updated')
    search_fields = ('name', 'domain')
    
    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('name', 'domain', 'logo', 'logowhite', 'favicon')
        }),
        ('İletişim Bilgileri', {
            'fields': ('phone', 'whatsapp', 'email', 'adress')
        }),
        ('Sosyal Medya', {
            'fields': ('facebook', 'instagram', 'twitter')
        }),
        ('Takip Kodları', {
            'fields': ('head_scripts', 'body_scripts'),
            'description': 'Google Analytics, Meta Pixel vb. takip kodlarını buraya ekleyebilirsiniz.'
        }),
        ('Schema Markup Ayarları', {
            'fields': (
                'alternate_name', 'city', 'region', 'postal_code', 'country',
                'latitude', 'longitude', 'opening_hours', 'price_range',
                'payment_accepted', 'currencies_accepted', 'founding_date',
                'founder_name', 'number_of_employees', 'service_radius',
                'average_rating', 'review_count', 'contact_type',
                'price_currency', 'country_name', 'city_name'
            ),
            'classes': ('collapse',)
        }),
        ('SEO Ayarları', {
            'fields': ('seo_title', 'seo_description', 'enable_sitemap', 'enable_robots_txt', 'enable_structured_data')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['created', 'updated']
        return readonly_fields

@admin.register(About)
class AboutAdmin(ImportExportModelAdmin):
    list_display = ('header','title','updated','created')

@admin.register(Hero)
class HeroAdmin(ImportExportModelAdmin):
    list_display = ('title', 'subtitle', 'is_active', 'updated', 'created')
    list_filter = ('is_active', 'created', 'updated')
    search_fields = ('title', 'subtitle', 'description')
    
    fieldsets = (
        ('Ana İçerik', {
            'fields': ('title', 'subtitle', 'description', 'banner')
        }),
        ('Birincil Buton', {
            'fields': ('primary_button_text', 'primary_button_link', 'primary_button_icon')
        }),
        ('İkincil Buton', {
            'fields': ('secondary_button_text', 'secondary_button_link', 'secondary_button_icon')
        }),
        ('İstatistikler', {
            'fields': ('counters',)
        }),
        ('Durum', {
            'fields': ('is_active',)
        })
    )

@admin.register(FeatureArea)
class FeatureAreaAdmin(ImportExportModelAdmin):
    list_display = ('title','updated','created')

@admin.register(Feature)
class FeatureAdmin(ImportExportModelAdmin):
    list_display = ('name','updated','created')


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    list_display = ('name','phone','email','created')

@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_display = ('name','title','created','updated')

@admin.register(CommentHeader)
class CommentHeaderAdmin(ImportExportModelAdmin):
    list_display = ('title','updated','created')


@admin.register(Faq)
class FaqAdmin(ImportExportModelAdmin):
    list_display = ('question','isActive','showIndex','updated','created')

@admin.register(Page_Seo)
class Page_SeoAdmin(ImportExportModelAdmin):
    list_display = ("page_url",)


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    list_display = ('title', 'category', 'location', 'is_featured', 'show_on_index', 'is_active', 'created')
    list_display_links = ('title',)
    list_editable = ('is_featured', 'show_on_index', 'is_active')
    list_filter = ('category', 'is_featured', 'show_on_index', 'is_active', 'created')
    search_fields = ('title', 'description', 'location', 'category')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created', 'updated')
    list_per_page = 20
    date_hierarchy = 'created'
    
    fieldsets = (
        ('📝 Temel Bilgiler', {
            'fields': ('title', 'slug', 'description', 'category', 'location', 'completed_date')
        }),
        ('🖼️ Görseller', {
            'fields': ('image', 'before_image', 'after_image'),
            'description': 'Ana görsel zorunlu, öncesi/sonrası görselleri isteğe bağlı.'
        }),
        ('⚙️ Durum', {
            'fields': ('is_featured', 'show_on_index', 'is_active', 'created', 'updated'),
            'classes': ('collapse',)
        }),
    )