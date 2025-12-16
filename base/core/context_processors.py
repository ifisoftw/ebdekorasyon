from django.conf import settings
from core.models import Settings

def site_settings(request):
    """
    Context processor to make site settings available in all templates.
    """
    try:
        site_settings = Settings.objects.first()
        if not site_settings:
            # Create default settings if none exist
            site_settings = Settings.objects.create(
                name="İFİ Yazılım",
                domain="localhost:8000"
            )
    except Exception:
        # Fallback to empty settings if database is not available
        site_settings = None
    
    footer_categories = []
    try:
        from service.models import ServiceCategory
        footer_categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')[:2]
    except Exception:
        pass

    return {
        'settings': site_settings,
        'site_settings': site_settings,
        'footer_categories': footer_categories,
    }
