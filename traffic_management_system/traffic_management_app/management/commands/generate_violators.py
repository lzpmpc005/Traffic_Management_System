from django.core.management.base import BaseCommand
import requests
import json
from random import randrange
import random
from traffic_management_app.models import Vehicle, Plates, Junction
import time


class Command(BaseCommand):
    help = 'Simulate traffic flow'

    def handle(self, *args, **kwargs):
        url = "http://localhost:8000/traffic_management/logging"
        light = 1

        for _ in range(10):
            vehicle_id = random.randint(120, 129)
            light = 1 - light
            self.traffic_flow(vehicle_id, light, url)
            time.sleep(5)

    def traffic_flow(self, vehicle_id, light, url):
        junction = Junction.objects.get(id=randrange(1, 13))
        vehicle = Vehicle.objects.get(id=vehicle_id)
        plate = Plates.objects.get(id=vehicle.PlateNumber_id)
        speed = randrange(0, 120)

        data = {
            "Junction": junction.Address,
            "PlateNumber": plate.Number,
            "Speed": speed,
            "Light": light
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS(response.json()))
        else:
            self.stdout.write(self.style.ERROR(response.json().get('error')))
