# ddr/management/commands/populate_dummy_data.py

from django.core.management.base import BaseCommand
from ddr.models import ClusterIncharge, Variety, CropType, Source, Farmer

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        ClusterIncharge.objects.all().delete()
        Variety.objects.all().delete()
        CropType.objects.all().delete()
        Source.objects.all().delete()
        Farmer.objects.all().delete()

        # Create some dummy data
        ClusterIncharge.objects.create(name="Incharge 1")
        ClusterIncharge.objects.create(name="Incharge 2")

        Variety.objects.create(name="Variety 1")
        Variety.objects.create(name="Variety 2")

        CropType.objects.create(name="Crop Type 1")
        CropType.objects.create(name="Crop Type 2")

        Source.objects.create(name="Source 1")
        Source.objects.create(name="Source 2")

        Farmer.objects.create(code="F001", eligible_qty=100.00)
        Farmer.objects.create(code="F002", eligible_qty=200.00)
        Farmer.objects.create(code="F003", eligible_qty=150.00)

        self.stdout.write(self.style.SUCCESS('Successfully populated dummy data'))
