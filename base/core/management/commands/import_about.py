import json
from django.core.management.base import BaseCommand
from core.models import About, Feature, Counter


class Command(BaseCommand):
    help = 'Import About page content from about.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='about.json',
            help='Path to the about.json file'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f'Invalid JSON: {e}'))
            return

        fields = data.get('fields', {})
        related_data = data.get('related_data', {})

        # Create or update Features
        features = []
        for feature_data in related_data.get('features_to_create', []):
            feature, created = Feature.objects.update_or_create(
                name=feature_data['title'],
                defaults={
                    'icon': feature_data.get('icon', ''),
                    'description': feature_data.get('description', ''),
                }
            )
            features.append(feature)
            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{status} Feature: {feature.name}'))

        # Create or update Counters
        counters = []
        for counter_data in related_data.get('counters_to_create', []):
            counter, created = Counter.objects.update_or_create(
                name=counter_data['title'],
                defaults={
                    'count': counter_data.get('value', '0'),
                }
            )
            counters.append(counter)
            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{status} Counter: {counter.name}'))

        # Create or update About
        about, created = About.objects.update_or_create(
            pk=data.get('pk', 1),
            defaults={
                'header': fields.get('header', ''),
                'title': fields.get('title', ''),
                'short_description': fields.get('short_description', ''),
                'description': fields.get('description', ''),
                'mission': fields.get('mission', ''),
                'vision': fields.get('vision', ''),
                'seo_title': fields.get('seo_title', '')[:60],  # max 60 chars
                'seo_description': fields.get('seo_description', '')[:160],  # max 160 chars
            }
        )

        # Add features and counters
        if features:
            about.features.set(features)
        if counters:
            about.counters.set(counters)

        status = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'\n✅ {status} About: {about.title}'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(features)} features attached'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(counters)} counters attached'))
