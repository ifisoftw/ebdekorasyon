import os
from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import io

def optimize_image(image_field, quality=85, max_width=None, max_height=None):
    """
    Optimize image for web delivery
    """
    if not image_field:
        return None
    
    try:
        # Open the image
        image = Image.open(image_field)
        
        # Convert to RGB if necessary (for JPEG)
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Resize if dimensions are provided
        if max_width or max_height:
            image.thumbnail((max_width or image.width, max_height or image.height), Image.Resampling.LANCZOS)
        
        # Save optimized image
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True, progressive=True)
        output.seek(0)
        
        return ContentFile(output.getvalue())
    
    except Exception as e:
        print(f"Image optimization error: {e}")
        return None

def create_webp_version(image_field, quality=85):
    """
    Create WebP version of an image
    """
    if not image_field:
        return None
    
    try:
        # Open the image
        image = Image.open(image_field)
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Save as WebP
        output = io.BytesIO()
        image.save(output, format='WebP', quality=quality, optimize=True)
        output.seek(0)
        
        return ContentFile(output.getvalue())
    
    except Exception as e:
        print(f"WebP conversion error: {e}")
        return None

def get_image_dimensions(image_field):
    """
    Get image dimensions
    """
    if not image_field:
        return None, None
    
    try:
        image = Image.open(image_field)
        return image.width, image.height
    except Exception as e:
        print(f"Image dimension error: {e}")
        return None, None

def generate_responsive_images(image_field, sizes=[(400, 300), (800, 600), (1200, 900)]):
    """
    Generate multiple sizes of an image for responsive design
    """
    if not image_field:
        return []
    
    responsive_images = []
    
    for width, height in sizes:
        try:
            image = Image.open(image_field)
            
            # Calculate aspect ratio
            original_ratio = image.width / image.height
            target_ratio = width / height
            
            if original_ratio > target_ratio:
                # Image is wider, crop width
                new_width = int(height * original_ratio)
                image = image.resize((new_width, height), Image.Resampling.LANCZOS)
                left = (new_width - width) // 2
                image = image.crop((left, 0, left + width, height))
            else:
                # Image is taller, crop height
                new_height = int(width / original_ratio)
                image = image.resize((width, new_height), Image.Resampling.LANCZOS)
                top = (new_height - height) // 2
                image = image.crop((0, top, width, top + height))
            
            # Save optimized image
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True, progressive=True)
            output.seek(0)
            
            responsive_images.append({
                'width': width,
                'height': height,
                'content': ContentFile(output.getvalue())
            })
            
        except Exception as e:
            print(f"Responsive image generation error: {e}")
            continue
    
    return responsive_images
