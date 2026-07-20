from core.models import Settings
from core.models import About
from service.models import Service
from blog.models import Blog
from django.contrib.sites.models import Site

def main(request):
    domain = Site.objects.get_current()
    settings = Settings.objects.first()
    about = About.objects.first()
    services = Service.objects.filter(isActive=True).all()

    # Settings kontrolü
    if not settings:
        settings = Settings()

    # About kontrolü
    if not about:
        about = About()

    return {
        'name': getattr(settings, 'name', ''),
        'title': getattr(settings, 'seo_title', ''),
        'keywords': getattr(settings, 'seo_keywords', ''),
        'description': getattr(settings, 'seo_description', ''),
        'domain': domain,
        'logo': getattr(settings, 'logo', None),
        'logowhite': getattr(settings, 'logowhite', None),
        'favicon': getattr(settings, 'favicon', None),
        'phone': getattr(settings, 'phone', ''),
        'whatsapp': getattr(settings, 'whatsapp', ''),
        'email': getattr(settings, 'email', ''),
        'adress': getattr(settings, 'adress', ''),
        'facebook': getattr(settings, 'facebook', ''),
        'instagram': getattr(settings, 'instagram', ''),
        'twitter': getattr(settings, 'twitter', ''),
        # Schema markup için dinamik alanlar
        'alternate_name': getattr(settings, 'alternate_name', ''),
        'city': getattr(settings, 'city', ''),
        'region': getattr(settings, 'region', ''),
        'postal_code': getattr(settings, 'postal_code', ''),
        'country': getattr(settings, 'country', ''),
        'latitude': getattr(settings, 'latitude', ''),
        'longitude': getattr(settings, 'longitude', ''),
        'opening_hours': getattr(settings, 'opening_hours', []),
        'price_range': getattr(settings, 'price_range', ''),
        'payment_accepted': getattr(settings, 'payment_accepted', ''),
        'currencies_accepted': getattr(settings, 'currencies_accepted', ''),
        'founding_date': getattr(settings, 'founding_date', ''),
        'founder_name': getattr(settings, 'founder_name', ''),
        'number_of_employees': getattr(settings, 'number_of_employees', ''),
        'service_radius': getattr(settings, 'service_radius', ''),
        'average_rating': getattr(settings, 'average_rating', ''),
        'review_count': getattr(settings, 'review_count', ''),
        'contact_type': getattr(settings, 'contact_type', ''),
        'price_currency': getattr(settings, 'price_currency', ''),
        'country_name': getattr(settings, 'country_name', ''),
        'city_name': getattr(settings, 'city_name', ''),
        'about_title': getattr(about, 'title', ''),
        'about_header': getattr(about, 'header', ''),
        'about_description': getattr(about, 'description', ''),
        'about_short_description': getattr(about, 'short_description', ''),
        'services': services,
        "canonical_url": request.build_absolute_uri().split('?')[0]
    }