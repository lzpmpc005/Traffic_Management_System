from django.core.management.base import BaseCommand
import requests
import json
from faker import Faker
from faker_vehicle import VehicleProvider

fake = Faker()
fake.add_provider(VehicleProvider)

class Command(BaseCommand):
    help = 'Register a vehicle for an owner'

    def add_arguments(self, parser):
        parser.add_argument('owner_id', type=int, help='The ID of the owner')

    def handle(self, *args, **kwargs):
        owner_id = kwargs['owner_id']
        self.register_vehicle(owner_id)

    def register_vehicle(self, owner_id):
        url = "http://localhost:8000/traffic_management/register_vehicle"

        data = {
            "owner_id": owner_id,
            "color": fake.color_name(),
            "type": fake.vehicle_year_make_model()
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS(
                f"Vehicle registered successfully. Vehicle ID: {response.json().get('vehicle_id')}"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f"Error registering vehicle: {response.json().get('error')}"
            ))