from django.core.management.base import BaseCommand
from service.models import Service, ServiceStep

class Command(BaseCommand):
    help = 'Populates services with default steps if missing'

    def handle(self, *args, **options):
        services = Service.objects.all()
        
        default_steps = [
            {
                'step_number': 1,
                'title': 'Ücretsiz Keşif & Planlama',
                'description': 'Uzman ekibimiz yerinde inceleme yapar, ihtiyaçlarınızı dinler ve en uygun çözüm planını hazırlar.'
            },
            {
                'step_number': 2,
                'title': 'Fiyatlandırma & Onay',
                'description': 'Şeffaf ve detaylı bir fiyat teklifi sunarız. Onayınızla birlikte iş takvimini belirleriz.'
            },
            {
                'step_number': 3,
                'title': 'Uygulama & Teslimat',
                'description': 'Belirlenen sürede, temiz ve titiz bir işçilikle projenizi tamamlayıp size teslim ederiz.'
            }
        ]

        for service in services:
            if not service.steps.exists():
                self.stdout.write(f"Adding steps to {service.title}...")
                for step_data in default_steps:
                    ServiceStep.objects.create(
                        service=service,
                        step_number=step_data['step_number'],
                        title=step_data['title'],
                        description=step_data['description']
                    )
            else:
                self.stdout.write(f"{service.title} already has steps.")
                
        self.stdout.write(self.style.SUCCESS('Successfully populated service steps'))
