from django.contrib import sitemaps
from django.urls import reverse
from service.models import Service, ServiceArea
from blog.models import Blog

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return ["index","about","services","blogs","faqs","contact"]

    def location(self, item):
        return reverse(item)
    
    def lastmod(self, obj):
        last_service = Service.objects.last()
        return last_service.updated if last_service else None

class ServiceViewSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Service.objects.all()
    def lastmod(self, obj):
        return obj.updated


class ServiceAreaSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ServiceArea.objects.all()
    def lastmod(self, obj):
        return obj.updated


class BlogViewSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Blog.objects.all()
    def lastmod(self, obj):
        return obj.updated