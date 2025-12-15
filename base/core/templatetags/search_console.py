from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def gsc_verification_meta():
    """
    Generates the Google Search Console HTML meta tag for site verification.
    """
    # Fallback to settings.py if no database settings
    try:
        from core.models import Settings
        settings_obj = Settings.objects.first()
        
        if settings_obj and settings_obj.gsc_verification_code:
            return mark_safe(f'<meta name="google-site-verification" content="{settings_obj.gsc_verification_code}" />')
    except:
        pass
    
    # Fallback to settings.py
    gsc_settings = getattr(settings, 'GOOGLE_SEARCH_CONSOLE', {})
    verification_code = gsc_settings.get('SITE_VERIFICATION_CODE')
    
    if verification_code:
        return mark_safe(f'<meta name="google-site-verification" content="{verification_code}" />')
    return ""

@register.inclusion_tag('partials/_search_console.html')
def search_console():
    """
    Google Search Console verification and optimization template tag.
    Usage: {% search_console %}
    """
    # Fallback to settings.py if no database settings
    try:
        from core.models import Settings
        settings_obj = Settings.objects.first()
        
        if settings_obj:
            return {
                'verification_code': settings_obj.gsc_verification_code,
                'enable_sitemap': settings_obj.enable_sitemap,
                'enable_robots_txt': settings_obj.enable_robots_txt,
                'enable_structured_data': settings_obj.enable_structured_data,
                'enable_core_web_vitals': settings_obj.enable_core_web_vitals,
                'sitemap_urls': ['/sitemap.xml', '/sitemap-services.xml', '/sitemap-blogs.xml'],
            }
    except:
        pass
    
    # Fallback to settings.py
    gsc_settings = getattr(settings, 'GOOGLE_SEARCH_CONSOLE', {})
    return {
        'verification_code': gsc_settings.get('SITE_VERIFICATION_CODE', ''),
        'enable_sitemap': gsc_settings.get('ENABLE_SITEMAP', False),
        'enable_robots_txt': gsc_settings.get('ENABLE_ROBOTS_TXT', False),
        'enable_structured_data': gsc_settings.get('ENABLE_STRUCTURED_DATA', False),
        'enable_core_web_vitals': gsc_settings.get('ENABLE_CORE_WEB_VITALS', False),
        'sitemap_urls': gsc_settings.get('SITEMAP_URLS', []),
    }

@register.simple_tag
def sitemap_url(sitemap_name='main'):
    """
    Generate sitemap URL for Search Console.
    Usage: {% sitemap_url "services" %}
    """
    sitemap_mapping = {
        'main': '/sitemap.xml',
        'services': '/sitemap-services.xml',
        'blogs': '/sitemap-blogs.xml',
    }
    return sitemap_mapping.get(sitemap_name, '/sitemap.xml')

@register.simple_tag
def robots_txt_content():
    """
    Generate robots.txt content for Search Console optimization.
    Usage: {% robots_txt_content %}
    """
    if not settings.GOOGLE_SEARCH_CONSOLE['ENABLE_ROBOTS_TXT']:
        return ''
    
    content = "User-agent: *\n"
    content += "Allow: /\n"
    content += "Disallow: /admin/\n"
    content += "Disallow: /media/\n"
    content += "Disallow: /static/\n"
    content += "\n"
    
    # Add sitemap URLs
    for sitemap_url in settings.GOOGLE_SEARCH_CONSOLE['SITEMAP_URLS']:
        content += f"Sitemap: {settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost:8000'}{sitemap_url}\n"
    
    return content
