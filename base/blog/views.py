from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from . models import Blog, Category, Tag
from core.models import Page_Seo
class BlogListView(ListView):
    model = Blog
    template_name = 'blogs.html'
    context_object_name = 'blogs'
    paginate_by = 4
    

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-updated')  # En yeni bloglar önce gelsin

        category_slug = self.request.GET.get('kategori')
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            queryset = queryset.filter(category=category)

        tag_slugs = self.request.GET.getlist('etiket')
        if tag_slugs:
            tags = Tag.objects.filter(slug__in=tag_slugs)
            queryset = queryset.filter(tags__in=tags).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        seo = Page_Seo.objects.filter(page_url='bloglar').first()
        context['seo'] = seo
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all()
        context['categories'] = Category.objects.all()
        
        context['tags'] = Tag.objects.all()

        return context