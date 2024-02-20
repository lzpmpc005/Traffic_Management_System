from django.core.management.base import BaseCommand
from time import sleep
import requests
import json
from traffic_management_app.models import Vehicle, Plates, Junction, Street, StatReport
import random
from django.db.models import Q


class Command(BaseCommand):
    help = 'Simulate vehicle driving behavior'

    def add_arguments(self, parser):
        parser.add_argument('destination', type=int, help='The ID of the destination junction')

    def handle(self, *args, **kwargs):
        destination_id = kwargs['destination']
        current_junction_id = 3
        vehicle_id = random.randint(131, 133)
        next_junction_id = self.drive(1, 60, current_junction_id, vehicle_id, destination_id)

        while next_junction_id:
            street = Street.objects.filter(Q(Start_junction_id=current_junction_id, End_junction_id=next_junction_id) | Q(Start_junction_id=next_junction_id, End_junction_id=current_junction_id)).first()
            speed = 60
            time_cost = 12 * street.Distance / speed
            print(f"Driving to Junction {next_junction_id}")
            sleep(time_cost)
            current_junction_id = next_junction_id
            next_junction_id = self.drive(1, 60, current_junction_id, vehicle_id, destination_id)

        print(f"Arrived at destination: Junction {destination_id}")


    def drive(self, light, speed, junction_id, vehicle_id, destination_id):
        url = "http://localhost:8000/traffic_management/logging"

        vehicle = Vehicle.objects.get(id=vehicle_id)
        plate = Plates.objects.get(id=vehicle.PlateNumber_id)
        junction = Junction.objects.get(id=junction_id)
        data = {
            "Junction": junction.Address,
            "PlateNumber": plate.Number,
            "Speed": speed,
            "Light": light,
            "destination": destination_id
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            next_junction = response.json().get('next_junction')
            return next_junction

        else:
            print(f"Failed to get next junction. Response status code: {response.status_code}")
            return None
