from django import template
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
import re
try:
    import bleach
except Exception:
    bleach = None


register = template.Library()

# İzin verilen HTML etiketleri
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'a', 'img', 'blockquote', 'div', 'span'
]

# İzin verilen HTML attribute'ları
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'width', 'height'],
    'div': ['class'],
    'span': ['class'],
    'p': ['class'],
}

@register.filter
def safe_html(value):
    """
    HTML içeriğini güvenli hale getirir.
    Sadece belirli etiketlere ve attribute'lara izin verir.
    """
    if not value:
        return ''
    
    # HTML'i temizle
    if bleach is not None:
        clean_html = bleach.clean(
            value,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
        )
    else:
        # Basit fallback: izin verilmeyen script ve event handler'ları çıkar, kalanını güvenli işaretle
        value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.DOTALL | re.IGNORECASE)
        value = re.sub(r'on\w+="[^"]*"', '', value, flags=re.IGNORECASE)
        value = re.sub(r"on\w+='[^']*'", '', value, flags=re.IGNORECASE)
        clean_html = value
    
    return mark_safe(clean_html)

@register.filter
def safe_content(value):
    """
    CKEditor'dan gelen içeriği güvenli hale getirir.
    """
    if not value:
        return ''
    
    # Tehlikeli script etiketlerini kaldır
    value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.DOTALL | re.IGNORECASE)
    
    # Inline JavaScript'i kaldır
    value = re.sub(r'on\w+="[^"]*"', '', value, flags=re.IGNORECASE)
    value = re.sub(r"on\w+='[^']*'", '', value, flags=re.IGNORECASE)
    
    # Güvenli HTML filtresi uygula
    return safe_html(value)

@register.filter
def truncate_safe(value, length=100):
    """
    HTML etiketlerini koruyarak metni kısaltır.
    """
    if not value:
        return ''
    
    # HTML etiketlerini kaldırarak uzunluğu kontrol et
    plain_text = strip_tags(value)
    if len(plain_text) <= length:
        return safe_content(value)
    
    # Metni kısalt
    truncated = plain_text[:length] + '...'
    return truncated

@register.filter
def replace(value, arg):
    """
    Replaces all occurrences of a substring with another substring.
    Usage: {{ value|replace:"old,new" }}
    """
    if isinstance(value, str) and isinstance(arg, str):
        try:
            old, new = arg.split(',')
            return value.replace(old, new)
        except ValueError:
            return value  # Return original value if arg is not in 'old,new' format
    return value

