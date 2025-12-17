from django.shortcuts import render, redirect
from core.models import Settings, FeatureArea
from . models import Service, ServiceHeader, ServiceArea, ServiceCategory
from core.forms import ContactForm
from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class ServicesView(SuccessMessageMixin,FormView):
    template_name = "services.html"
    form_class = ContactForm
    success_message = "Formunuz Başarıyla Gönderildi"
    success_url = '/hizmetler'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_header'] = ServiceHeader.objects.first()
        context['services'] = Service.objects.filter(isActive=True).order_by('created')
        context['categories'] = ServiceCategory.objects.filter(is_active=True).order_by('order')
        context['feature_area'] = FeatureArea.objects.first()     
        context['breadcrumbs'] = [
            {'name': 'Hizmetlerimiz', 'url': '/hizmetler/'}
        ]
        
        # SEO Context for Templates
        if context['service_header']:
            from django.utils.html import strip_tags
            context['seo'] = {
                'seo_title': context['service_header'].title,
                'seo_description': strip_tags(context['service_header'].description)[:160]
            }
        return context

    def form_valid(self, form) :
        form.save()
        return super().form_valid(form)

class ServiceAreaListView(ListView):
    model = ServiceArea
    template_name = 'service_areas.html'
    context_object_name = 'service_areas'
    
    def get_queryset(self):
        return ServiceArea.objects.filter(isActive=True).order_by('created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_header'] = ServiceHeader.objects.first()
        context['feature_area'] = FeatureArea.objects.first()
        
        # SEO Context
        if context['service_header']:
            from django.utils.html import strip_tags
            context['seo'] = {
                'seo_title': f"Hizmet Bölgelerimiz | {context['service_header'].title}",
                'seo_description': strip_tags(context['service_header'].description)[:160]
            }
        return context

def service_detail(request, slug):
    service = None
    try:
        # Try to find in Service model first
        service = Service.objects.get(slug=slug, isActive=True)
    except Service.DoesNotExist:
        try:
            # If not found, try ServiceArea model
            service = ServiceArea.objects.get(slug=slug, isActive=True)
            template_name = 'service_area_detail.html'
        except ServiceArea.DoesNotExist:
            raise Http404("Hizmet bulunamadı")
    else:
        template_name = 'service-detail.html'
    
    # Get other active services (excluding current one if it's a Service)
    # Note: We can't easily exclude if it's a ServiceArea by slug without more logic, 
    # but for sidebar consistency we usually list main services.
    services_other = Service.objects.filter(isActive=True).exclude(slug=slug)[:3]
    
    # Get all services for sidebar
    services = Service.objects.filter(isActive=True)
    categories = ServiceCategory.objects.filter(is_active=True).order_by('order')
    
    context = {
        'service': service,
        'services_other': services_other,
        'services': services,
        'categories': categories,
    }
    
    return render(request, template_name, context)

