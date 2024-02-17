from django.core.management.base import BaseCommand
from traffic_management_app.models import Owner, DriverLicense

class Command(BaseCommand):
    help = 'Create driver licenses for owners'

    def add_arguments(self, parser):
        parser.add_argument('owner_id', type=int, help='The ID of the owner')

    def handle(self, *args, **kwargs):
        owner_id = kwargs['owner_id']
        try:
            owner = Owner.objects.get(id=owner_id)
            self.create_driver_license(owner)
            self.stdout.write(self.style.SUCCESS(f"Driver license created for owner with ID {owner_id}"))
        except Owner.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Owner with ID {owner_id} does not exist"))

    def create_driver_license(self, owner):
        DriverLicense.objects.create(
            Owner=owner,
            License_Number=owner.Owner_driver_license,
        )