from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Blog
from service.models import Service
from core.models import About

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['index', 'about', 'contact', 'services', 'blogs', 'faqs']

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Blog.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated

class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated
