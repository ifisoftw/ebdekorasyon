from django import template
from django.conf import settings
import os

register = template.Library()

@register.simple_tag
def cdn_url(path, cdn_domain=None):
    """
    Generate CDN URL for static files
    """
    if not cdn_domain:
        cdn_domain = getattr(settings, 'CDN_DOMAIN', None)
    
    if cdn_domain:
        return f"https://{cdn_domain}{path}"
    
    return path

@register.simple_tag
def optimized_static(path, cdn_domain=None):
    """
    Generate optimized static file URL with CDN support
    """
    if not cdn_domain:
        cdn_domain = getattr(settings, 'CDN_DOMAIN', None)
    
    # Check if minified version exists
    if path.endswith('.css') and not path.endswith('.min.css'):
        minified_path = path.replace('.css', '.min.css')
        if os.path.exists(os.path.join(settings.STATIC_ROOT, minified_path.lstrip('/'))):
            path = minified_path
    
    if path.endswith('.js') and not path.endswith('.min.js'):
        minified_path = path.replace('.js', '.min.js')
        if os.path.exists(os.path.join(settings.STATIC_ROOT, minified_path.lstrip('/'))):
            path = minified_path
    
    if cdn_domain:
        return f"https://{cdn_domain}{path}"
    
    return path

@register.simple_tag
def preload_resource(path, resource_type='style', cdn_domain=None):
    """
    Generate preload link for critical resources
    """
    if not cdn_domain:
        cdn_domain = getattr(settings, 'CDN_DOMAIN', None)
    
    url = path
    if cdn_domain:
        url = f"https://{cdn_domain}{path}"
    
    return f'<link rel="preload" href="{url}" as="{resource_type}">'

@register.simple_tag
def critical_css():
    """
    Generate critical CSS inline
    """
    critical_css_path = os.path.join(settings.STATIC_ROOT, 'css', 'critical.css')
    
    if os.path.exists(critical_css_path):
        with open(critical_css_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    return ''

@register.simple_tag
def resource_hints():
    """
    Generate resource hints for performance
    """
    hints = []
    
    # DNS prefetch for external domains
    external_domains = [
        'fonts.googleapis.com',
        'fonts.gstatic.com',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        'unpkg.com'
    ]
    
    for domain in external_domains:
        hints.append(f'<link rel="dns-prefetch" href="//{domain}">')
    
    # Preconnect to critical domains
    critical_domains = [
        'fonts.googleapis.com',
        'fonts.gstatic.com'
    ]
    
    for domain in critical_domains:
        hints.append(f'<link rel="preconnect" href="https://{domain}" crossorigin>')
    
    return '\n'.join(hints)
