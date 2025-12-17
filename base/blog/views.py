from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.db.models import Q, Count
from . models import Blog, Category, Tag


class BlogListView(ListView):
    model = Blog
    template_name = 'blogs.html'
    context_object_name = 'blogs'
    paginate_by = 6
    
    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['partials/_blog_content.html']
        return ['blogs.html']

    def get_queryset(self):
        queryset = super().get_queryset().filter(isActive=True).order_by('-updated')

        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(short_description__icontains=search_query)
            )

        # Category filter
        category_slug = self.request.GET.get('kategori')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Tag filter
        tag_slug = self.request.GET.get('etiket')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Base Queryset for Counts (Active + Search)
        base_qs = Blog.objects.filter(isActive=True)
        search_query = self.request.GET.get('q')
        if search_query:
            base_qs = base_qs.filter(
                Q(title__icontains=search_query) | 
                Q(short_description__icontains=search_query)
            )
        
        # Category Counts (Based on Search only, ignoring current category/tag selection to allow switching)
        # But commonly in facets, you want to see counts within current scope. 
        # Let's count categories based on Search Query.
        context['categories'] = Category.objects.filter(
            blog__in=base_qs
        ).annotate(count=Count('blog')).order_by('name').distinct()
        
        # Tag Counts (Based on Search + Current Category)
        tags_qs = base_qs
        current_category = self.request.GET.get('kategori')
        if current_category:
            tags_qs = tags_qs.filter(category__slug=current_category)
            
        context['tags'] = Tag.objects.filter(
            blog__in=tags_qs
        ).annotate(count=Count('blog')).order_by('name').distinct()
        
        context['current_category'] = self.request.GET.get('kategori', '')
        context['current_tag'] = self.request.GET.get('etiket', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['breadcrumbs'] = [
            {'name': 'Blog', 'url': '/bloglar/'}
        ]

        
        # SEO Context
        context['seo'] = {
            'seo_title': 'Blog - Dekorasyon ve Tadilat İpuçları',
            'seo_description': 'Mobilya boyama, ev tadilatı, dekorasyon önerileri ve daha fazlası için blog sayfamızı ziyaret edin.'
        }
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all()
        context['categories'] = Category.objects.all()
        
        # Related Blogs (Same Category, Exclude Current)
        context['related_blogs'] = Blog.objects.filter(
            category=self.object.category, 
            isActive=True
        ).exclude(id=self.object.id).order_by('-created')[:3]
        
        context['tags'] = Tag.objects.all()

        return context