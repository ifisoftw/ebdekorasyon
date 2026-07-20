from django import template
from django.conf import settings
import os

register = template.Library()

@register.filter
def webp_url(image_field):
    """
    Convert image URL to WebP format if supported
    """
    if not image_field:
        return ''
    
    # Get the original URL
    original_url = image_field.url
    
    # Check if WebP is supported (you can add browser detection here)
    # For now, we'll return the original URL
    # In production, you might want to check request headers for WebP support
    
    return original_url

@register.filter
def responsive_image(image_field, sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"):
    """
    Generate responsive image attributes
    """
    if not image_field:
        return ''
    
    return {
        'src': image_field.url,
        'sizes': sizes,
        'alt': getattr(image_field, 'alt', ''),
        'loading': 'lazy'
    }

@register.simple_tag
def picture_element(image_field, alt_text="", class_name="", sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"):
    """
    Generate a complete picture element with WebP and fallback
    """
    if not image_field:
        return ''
    
    original_url = image_field.url
    webp_url = original_url.replace('.jpg', '.webp').replace('.jpeg', '.webp').replace('.png', '.webp')
    
    return f'''
    <picture>
        <source srcset="{webp_url}" type="image/webp">
        <img src="{original_url}" 
             alt="{alt_text}" 
             class="{class_name}"
             sizes="{sizes}"
             loading="lazy"
             width="auto"
             height="auto">
    </picture>
    '''
