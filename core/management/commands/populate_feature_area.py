from django.core.management.base import BaseCommand
from core.models import FeatureArea, Feature

class Command(BaseCommand):
    help = 'Populates the FeatureArea with specific content for Service Areas'

    def handle(self, *args, **kwargs):
        # 1. Create Features
        features_data = [
            {
                "name": "Zamanında Teslimat",
                "description": "Ulaşım süresini bahane etmeden, söz verdiğimiz tarihte işbaşı yapıyor ve teslim ediyoruz.",
                "icon": "fas fa-clock"
            },
            {
                "name": "Garantili Hizmet",
                "description": "Hangi ilçede olursanız olun, yaptığımız işin arkasındayız. 2 yıl işçilik garantisi veriyoruz.",
                "icon": "fas fa-shield-alt"
            },
            {
                "name": "Ücretsiz Keşif",
                "description": "Mesafe fark etmeksizin tüm İstanbul içi projeleriniz için ücretsiz yerinde keşif hizmetimiz vardır.",
                "icon": "fas fa-tools"
            },
            {
                "name": "Uzman Kadro",
                "description": "Sertifikalı ve deneyimli ustalarımızla, projenizin her aşamasında en yüksek kaliteyi sunuyoruz.",
                "icon": "fas fa-users-cog"
            }
        ]

        created_features = []
        for f_data in features_data:
            feature, created = Feature.objects.get_or_create(
                name=f_data["name"],
                defaults={
                    "description": f_data["description"],
                    "icon": f_data["icon"]
                }
            )
            created_features.append(feature)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created feature: {feature.name}'))
            else:
                self.stdout.write(f'Feature already exists: {feature.name}')

        # 2. Update or Create FeatureArea
        # Assuming we want to update the first one or create a specific one.
        # Since views.py uses .first(), we should target that.
        
        feature_area = FeatureArea.objects.first()
        if not feature_area:
            feature_area = FeatureArea()
            self.stdout.write('Creating new FeatureArea')
        else:
            self.stdout.write('Updating existing FeatureArea')

        feature_area.header = "Neden Bizi Seçmelisiniz?"
        feature_area.title = 'Lokasyon Fark Etmeksizin'
        feature_area.highlighted_title = 'Aynı Kalite Standartları'
        feature_area.short_description = "Hizmet kalitemiz standarttır." # Placeholder as it wasn't in the static HTML explicitly shown in the main text block, but model requires it.
        
        # Info Card Fields
        feature_area.info_card_title = "Mobil Ekiplerimiz"
        feature_area.info_card_description = "İstanbul'un her noktasına ulaşabilen geniş araç filomuz ve uzman ekiplerimizle, tadilat süreçlerinizi aksatmadan yönetiyoruz."
        feature_area.info_card_icon = "fas fa-truck"
        
        feature_area.save()

        # 3. Link Features
        feature_area.features.set(created_features)
        feature_area.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated FeatureArea content'))
