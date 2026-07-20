from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from core.models import Report
from core.resource import ReportResource
from . models import Service, ServiceHeader, ServiceArea, ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order', 'is_active', 'service_count')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('is_active',)
    ordering = ['order', 'name']
    
    def service_count(self, obj):
        count = obj.services.count()
        return f'📦 {count}'
    service_count.short_description = 'Hizmet Sayısı'


@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin):
    list_display = ('title', 'category', 'seo_title','seo_description','icon', 'isActive', 'showIndex', 'updated')
    list_display_links = ('title',)
    list_editable = ('category', 'seo_title','seo_description','icon','isActive', 'showIndex')
    prepopulated_fields = {'slug': ('seo_title',)}
    search_fields = ('title', 'description', 'short_description', 'icon')
    list_filter = ('category', 'isActive', 'showIndex', 'created', 'updated')
    readonly_fields = ('created', 'updated', 'feature_count', 'faq_count')
    filter_horizontal = ('features', 'faqs')
    list_per_page = 20
    date_hierarchy = 'created'
    
    fieldsets = (
        ('🔍 SEO Ayarları', {
            'fields': ('seo_title', 'slug', 'seo_description'),
        }),
        ('📝 Temel Bilgiler', {
            'fields': ('title', 'category', 'icon', 'image', 'before_image', 'after_image', 'short_description', 'description')
        }),
        ('🔗 İlişkiler', {
            'fields': ('features', 'faqs'),
            'classes': ('collapse',)
        }),
        ('⚙️ Durum', {
            'fields': ('isActive', 'showIndex','created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    

    
    def feature_count(self, obj):
        count = obj.features.count()
        return f'🔧 {count}' if count > 0 else '❌'
    feature_count.short_description = 'Özellikler'
    
    def faq_count(self, obj):
        count = obj.faqs.count()
        return f'❓ {count}' if count > 0 else '❌'
    faq_count.short_description = 'SSS'


@admin.register(ServiceArea)
class ServiceAreaAdmin(ImportExportModelAdmin):
    list_display = ('title', 'seo_title', 'slug', 'updated')
    list_display_links = ('title',)
    list_editable = ('seo_title', 'slug')
    prepopulated_fields = {'slug': ('seo_title',)}
    search_fields = ('title', 'description', 'short_description')
    list_filter = ('created', 'updated')
    readonly_fields = ('created', 'updated', 'feature_count', 'faq_count')
    filter_horizontal = ('features', 'faqs')
    list_per_page = 20
    date_hierarchy = 'created'

    fieldsets = (
        ('🔍 SEO Ayarları', {
            'fields': ('seo_title', 'slug', 'seo_description'),
        }),
        ('📝 Temel Bilgiler', {
            'fields': ('title', 'icon', 'image', 'short_description', 'description')
        }),
        ('🔗 İlişkiler', {
            'fields': ('features', 'faqs'),
            'classes': ('collapse',)
        }),
        ('⚙️ Durum', {
            'fields': ('isActive', 'showIndex', 'created', 'updated'),
            'classes': ('collapse',)
        }),
    )

    def feature_count(self, obj):
        count = obj.features.count()
        return f'🔧 {count}' if count > 0 else '❌'
    feature_count.short_description = 'Özellikler'

    def faq_count(self, obj):
        count = obj.faqs.count()
        return f'❓ {count}' if count > 0 else '❌'
    faq_count.short_description = 'SSS'



@admin.register(ServiceHeader)
class ServiceHeaderAdmin(ImportExportModelAdmin):
    list_display = ('title', 'updated', 'created')
    search_fields = ('title', 'description')
    readonly_fields = ('created', 'updated')
    list_per_page = 20
    
    fieldsets = (
        ('📝 İçerik', {
            'fields': ('title', 'description')
        }),
        ('🕒 Sistem Bilgileri', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    