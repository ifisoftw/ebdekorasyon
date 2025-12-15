from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        """
        Override admin index to add custom dashboard link.
        """
        extra_context = extra_context or {}
        extra_context['custom_dashboard_url'] = '/admin/webvitals/dashboard/'
        return super().index(request, extra_context)

# Use custom admin site
admin_site = CustomAdminSite()
admin_site.site_header = "İFİ Yazılım Admin"
admin_site.site_title = "İFİ Yazılım"
admin_site.index_title = "Yönetim Paneli"

# Register all models with custom admin site
from django.apps import apps
from django.contrib.admin.sites import site as default_site

# Copy all registrations from default site to custom site
for model, admin_class in default_site._registry.items():
    admin_site.register(model, admin_class.__class__)

# Replace default admin site
admin.site = admin_site
