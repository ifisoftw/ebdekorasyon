from django.http import HttpResponse
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from core.models import Settings, About, Hero, Feature, FeatureArea, Counter, Faq, Comment, CommentHeader, Project
from core.forms import ContactForm
from blog.models import Blog
from service.models import Service, ServiceCategory, ServiceArea

def robots_txt(request):
    """
    Generate robots.txt file for Search Console optimization.
    """
    settings = Settings.objects.first()
    if not settings or not settings.enable_robots_txt:
        return HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")
    
    context = {
        'domain': request.get_host(),
    }
    
    robots_content = render_to_string('robots.txt', context)
    return HttpResponse(robots_content, content_type="text/plain")

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        from core.models import Project  # Import here to avoid circular import
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all()
        context['services'] = Service.objects.filter(showIndex=True, isActive=True).order_by('created')
        context['categories'] = ServiceCategory.objects.filter(is_active=True).order_by('order')
        context['projects'] = Project.objects.filter(show_on_index=True, is_active=True)
        context['comparison_project'] = Project.objects.filter(before_image__isnull=False, after_image__isnull=False, show_on_index=True, is_active=True).first()
        context['settings'] = Settings.objects.first()
        context['hero'] = Hero.objects.first()
        context['features'] = Feature.objects.all()[:6]
        context['feature_area'] = FeatureArea.objects.first()
        context['service_areas'] = ServiceArea.objects.filter(isActive=True, showIndex=True)
        context['counters'] = Counter.objects.all()
        context['comments'] = Comment.objects.all()[:3]
        context['comment_header'] = CommentHeader.objects.first()
        context['faqs'] = Faq.objects.filter(isActive=True, showIndex=True)
        return context

class AboutView(TemplateView):
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.objects.first()
        context['about'] = About.objects.first()
        context['counters'] = Counter.objects.all()
        context['breadcrumbs'] = [
            {'name': 'Hakkımızda', 'url': '/hakkimizda/'}
        ]
        return context

class ContactView(TemplateView):
    template_name = 'contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.objects.first()
        context['form'] = ContactForm()
        context['breadcrumbs'] = [
            {'name': 'İletişim', 'url': '/iletisim/'}
        ]
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapacağız.')
            return redirect('contact')
        else:
            messages.error(request, 'Formda hatalar bulundu. Lütfen kontrol edip tekrar deneyin.')
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)

class FaqView(TemplateView):
    template_name = 'faqs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.objects.first()
        context['faqs'] = Faq.objects.filter(isActive=True)
        return context

class PrivacyPolicyView(TemplateView):
    template_name = 'staticpages/privacy-policy.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.objects.first()
        return context

class TermsOfServiceView(TemplateView):
    template_name = 'staticpages/terms-of-service.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.objects.first()
        return context

class KvkkView(TemplateView):
    template_name = 'staticpages/kvkk.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.objects.first()
        return context

class ProjectsListView(ListView):
    model = Project
    template_name = 'projects.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        qs = Project.objects.filter(is_active=True).order_by('-order' if hasattr(Project, 'order') else '-created')
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.objects.first()
        # Get distinct categories from active projects
        context['categories'] = Project.objects.filter(is_active=True).values_list('category', flat=True).distinct().order_by('category')
        context['current_category'] = self.request.GET.get('category', '')
        context['breadcrumbs'] = [
            {'name': 'Projeler', 'url': '/projeler/'}
        ]
        return context

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['partials/_project_content.html']
        return super().get_template_names()

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.objects.first()
        context['breadcrumbs'] = [
            {'name': 'Projeler', 'url': '/projeler/'},
            {'name': self.object.title, 'url': self.object.slug}
        ]
        return context

class GalleryView(ListView):
    model = Project
    template_name = 'gallery.html'
    context_object_name = 'projects'
    paginate_by = 6

    def get_queryset(self):
        return Project.objects.filter(is_active=True).exclude(before_image='').exclude(after_image='').order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.objects.first()
        context['breadcrumbs'] = [
            {'name': 'Galeri', 'url': '/galeri/'}
        ]
        return context


class KvkkView(TemplateView):
    template_name = 'staticpages/kvkk.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = Settings.objects.first()
        return context