from django.contrib import sitemaps
from django.urls import reverse
from service.models import Service, ServiceArea
from blog.models import Blog
from core.models import Project

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return [
            "index", "about", "services", "blogs", "faqs", "contact",
            "projects", "gallery", "service_areas",
            "privacy_policy", "terms_of_service", "kvkk"
        ]

    def location(self, item):
        return reverse(item)
    
    def lastmod(self, obj):
        last_service = Service.objects.last()
        return last_service.updated if last_service else None


class ServiceViewSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Service.objects.filter(isActive=True)

    def lastmod(self, obj):
        return obj.updated

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page, site, protocol)
        for item, url in zip(self.paginator.page(page).object_list, urls):
            images = []
            if item.image:
                images.append(item.image.url)
            if item.before_image:
                images.append(item.before_image.url)
            if item.after_image:
                images.append(item.after_image.url)
            if images:
                url['images'] = images
        return urls


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
        return Blog.objects.filter(isActive=True)

    def lastmod(self, obj):
        return obj.updated

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page, site, protocol)
        for item, url in zip(self.paginator.page(page).object_list, urls):
            if item.image:
                url['images'] = [item.image.url]
        return urls


class ProjectViewSitemap(sitemaps.Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page, site, protocol)
        for item, url in zip(self.paginator.page(page).object_list, urls):
            images = []
            if item.image:
                images.append(item.image.url)
            if item.before_image:
                images.append(item.before_image.url)
            if item.after_image:
                images.append(item.after_image.url)
            if images:
                url['images'] = images
        return urls