from django.core.management.base import BaseCommand
from django.utils.text import slugify
from service.models import ServiceArea
import random

class Command(BaseCommand):
    help = 'Populates the ServiceArea model with Istanbul Anatolian Side districts'

    def handle(self, *args, **kwargs):
        districts = [
            'Kadıköy',
            'Üsküdar',
            'Ataşehir',
            'Ümraniye',
            'Maltepe',
            'Kartal',
            'Pendik',
            'Beykoz',
            'Çekmeköy',
            'Tuzla',
            'Sancaktepe',
            'Sultanbeyli',
            'Şile',
            'Adalar'
        ]

        # Generic icons to rotate through if specific ones aren't set
        icons = [
            'fas fa-map-marker-alt',
            'fas fa-city',
            'fas fa-building',
            'fas fa-home'
        ]

        # Cleanup old entries first
        deleted_count, _ = ServiceArea.objects.filter(title__contains='Boya & Tadilat').delete()
        self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} old "Boya & Tadilat" entries.'))

        created_count = 0
        for district in districts:
            title = f"{district} Dekorasyon & Restorasyon"
            # Basic Turkish slugify replacement
            slug_base = district.lower().replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
            slug = f"{slug_base}-dekorasyon-restorasyon"
            
            description = (
                f"<p>İstanbul <strong>{district}</strong> bölgesinde profesyonel dekorasyon, "
                f"restorasyon, iç mimarlık ve anahtar teslim yenileme hizmetleri sunuyoruz.</p>"
                f"<p>EB Dekorasyon olarak {district} ve çevresinde tarihi ve modern yapıların dokusuna uygun "
                f"restorasyon ve dekorasyon çözümleri üretiyoruz. Ücretsiz keşif için bize ulaşın.</p>"
            )
            
            short_description = f"{district} bölgesinde profesyonel dekorasyon, restorasyon ve iç mimarlık hizmetleri. Anahtar teslim projeler."

            if not ServiceArea.objects.filter(slug=slug).exists():
                ServiceArea.objects.create(
                    title=title,
                    slug=slug,
                    description=description,
                    short_description=short_description,
                    isActive=True,
                    showIndex=True,
                    icon=random.choice(icons)
                )
                self.stdout.write(self.style.SUCCESS(f'Created service area: {title}'))
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'Service area already exists: {title}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {created_count} service areas.'))
