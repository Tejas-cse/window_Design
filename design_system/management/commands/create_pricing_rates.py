from django.core.management.base import BaseCommand
from design_system.models import PricingRate


class Command(BaseCommand):
    help = 'Create default pricing rates for materials'

    def handle(self, *args, **options):
        materials = {
            'aluminum': {'rate': 200, 'labor': 250, 'glass': 120, 'mesh': 60, 'profile': 180},
            'upvc': {'rate': 150, 'labor': 200, 'glass': 100, 'mesh': 50, 'profile': 150},
            'steel': {'rate': 250, 'labor': 300, 'glass': 130, 'mesh': 70, 'profile': 200},
            'wood': {'rate': 300, 'labor': 350, 'glass': 140, 'mesh': 80, 'profile': 220},
        }
        
        for material_key, rates in materials.items():
            rate, created = PricingRate.objects.get_or_create(
                material_type=material_key,
                defaults={
                    'rate_per_sqft': rates['rate'],
                    'labor_cost_per_unit': rates['labor'],
                    'glass_cost_per_sqft': rates['glass'],
                    'mesh_cost_per_sqft': rates['mesh'],
                    'profile_cost_per_meter': rates['profile'],
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created pricing rate for {material_key.upper()}')
                )
            else:
                self.stdout.write(f'Pricing rate for {material_key.upper()} already exists')
