from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('partials/_ga4_analytics.html')
def ga4_analytics():
    """
    Google Analytics 4 tracking code template tag.
    Usage: {% ga4_analytics %}
    """
    # Fallback to settings.py if no database settings
    try:
        from core.models import Settings
        settings_obj = Settings.objects.first()
        
        if settings_obj and settings_obj.enable_analytics and settings_obj.ga4_measurement_id:
            return {
                'ga4_measurement_id': settings_obj.ga4_measurement_id,
                'enable_analytics': settings_obj.enable_analytics,
                'enable_debug': settings_obj.enable_analytics_debug,
                'enable_events': settings_obj.enable_analytics_events,
                'enable_conversions': settings_obj.enable_analytics_conversions,
                'enable_core_web_vitals': settings_obj.enable_core_web_vitals,
            }
    except:
        pass
    
    # Fallback to settings.py
    ga4_settings = getattr(settings, 'GOOGLE_ANALYTICS', {})
    return {
        'ga4_measurement_id': ga4_settings.get('GA4_MEASUREMENT_ID', ''),
        'enable_analytics': ga4_settings.get('ENABLE_ANALYTICS', False),
        'enable_debug': ga4_settings.get('ENABLE_DEBUG_MODE', False),
        'enable_events': ga4_settings.get('ENABLE_EVENTS', False),
        'enable_conversions': ga4_settings.get('ENABLE_CONVERSIONS', False),
        'enable_core_web_vitals': ga4_settings.get('ENABLE_CORE_WEB_VITALS', False),
    }

@register.simple_tag
def ga4_event(event_name, event_category=None, event_label=None, value=None):
    """
    Generate GA4 event tracking code.
    Usage: {% ga4_event "button_click" "engagement" "header_cta" %}
    """
    if not settings.GOOGLE_ANALYTICS['ENABLE_EVENTS']:
        return ''
    
    event_data = {
        'event_name': event_name,
        'event_category': event_category or 'general',
        'event_label': event_label or '',
        'value': value or 0
    }
    
    return f"gtag('event', '{event_name}', {{ 'event_category': '{event_data['event_category']}', 'event_label': '{event_data['event_label']}', 'value': {event_data['value']} }});"

@register.simple_tag
def ga4_conversion(conversion_name, value=None, currency='TRY'):
    """
    Generate GA4 conversion tracking code.
    Usage: {% ga4_conversion "contact_form_submit" 100 %}
    """
    if not settings.GOOGLE_ANALYTICS['ENABLE_CONVERSIONS']:
        return ''
    
    return f"gtag('event', 'conversion', {{ 'send_to': '{conversion_name}', 'value': {value or 0}, 'currency': '{currency}' }});"
