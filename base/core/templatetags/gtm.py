from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('partials/_gtm_head.html')
def gtm_head():
    """
    Google Tag Manager head code template tag.
    Usage: {% gtm_head %}
    """
    # Fallback to settings.py if no database settings
    try:
        from core.models import Settings
        settings_obj = Settings.objects.first()
        
        if settings_obj and settings_obj.enable_gtm and settings_obj.gtm_container_id:
            return {
                'gtm_container_id': settings_obj.gtm_container_id,
                'enable_gtm': settings_obj.enable_gtm,
                'enable_debug': settings_obj.enable_gtm_debug,
                'enable_data_layer': settings_obj.enable_gtm_data_layer,
                'enable_custom_events': settings_obj.enable_gtm_custom_events,
                'enable_e_commerce': settings_obj.enable_gtm_ecommerce,
            }
    except:
        pass
    
    # Fallback to settings.py
    gtm_settings = getattr(settings, 'GOOGLE_TAG_MANAGER', {})
    return {
        'gtm_container_id': gtm_settings.get('GTM_CONTAINER_ID', 'GTM-XXXXXXX'),
        'enable_gtm': gtm_settings.get('ENABLE_GTM', False),
        'enable_debug': gtm_settings.get('ENABLE_DEBUG_MODE', False),
        'enable_data_layer': gtm_settings.get('ENABLE_DATA_LAYER', False),
        'enable_custom_events': gtm_settings.get('ENABLE_CUSTOM_EVENTS', False),
        'enable_e_commerce': gtm_settings.get('ENABLE_E_COMMERCE', False),
    }

@register.inclusion_tag('partials/_gtm_body.html')
def gtm_body():
    """
    Google Tag Manager body code template tag.
    Usage: {% gtm_body %}
    """
    # Fallback to settings.py if no database settings
    try:
        from core.models import Settings
        settings_obj = Settings.objects.first()
        
        if settings_obj and settings_obj.enable_gtm and settings_obj.gtm_container_id:
            return {
                'gtm_container_id': settings_obj.gtm_container_id,
                'enable_gtm': settings_obj.enable_gtm,
            }
    except:
        pass
    
    # Fallback to settings.py
    gtm_settings = getattr(settings, 'GOOGLE_TAG_MANAGER', {})
    return {
        'gtm_container_id': gtm_settings.get('GTM_CONTAINER_ID', 'GTM-XXXXXXX'),
        'enable_gtm': gtm_settings.get('ENABLE_GTM', False),
    }

@register.simple_tag
def gtm_event(event_name, event_category=None, event_label=None, value=None, custom_parameters=None):
    """
    Generate GTM dataLayer event push.
    Usage: {% gtm_event "button_click" "engagement" "header_cta" %}
    """
    if not settings.GOOGLE_TAG_MANAGER['ENABLE_CUSTOM_EVENTS']:
        return ''
    
    event_data = {
        'event': event_name,
        'event_category': event_category or 'general',
        'event_label': event_label or '',
        'value': value or 0
    }
    
    if custom_parameters:
        event_data.update(custom_parameters)
    
    # Convert to JavaScript object
    js_object = ', '.join([f"'{k}': {repr(v)}" for k, v in event_data.items()])
    
    return f"dataLayer.push({{{js_object}}});"

@register.simple_tag
def gtm_ecommerce(action, transaction_id=None, value=None, currency='TRY', items=None):
    """
    Generate GTM e-commerce event.
    Usage: {% gtm_ecommerce "purchase" "TXN123" 100.00 "TRY" items %}
    """
    if not settings.GOOGLE_TAG_MANAGER['ENABLE_E_COMMERCE']:
        return ''
    
    ecommerce_data = {
        'event': 'purchase',
        'ecommerce': {
            'transaction_id': transaction_id or '',
            'value': value or 0,
            'currency': currency,
            'items': items or []
        }
    }
    
    return f"dataLayer.push({ecommerce_data});"

@register.simple_tag
def gtm_custom_dimension(dimension_number, value):
    """
    Generate GTM custom dimension.
    Usage: {% gtm_custom_dimension 1 "premium_user" %}
    """
    return f"dataLayer.push({{'custom_dimension_{dimension_number}': '{value}'}});"
