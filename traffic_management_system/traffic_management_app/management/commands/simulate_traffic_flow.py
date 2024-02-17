from django.core.management.base import BaseCommand
import requests
import json
from traffic_management_app.models import Vehicle, Plates, Junction
import random
from datetime import datetime


class Command(BaseCommand):
    help = 'Simulate traffic flow'

    def handle(self, *args, **kwargs):
        url = "http://localhost:8000/traffic_management/logging"
        light = 1
        last_toggle_time = datetime.now().strftime("%M%S")

        while True:
            vehicle_id = random.randint(120, 129)
            now = datetime.now().strftime("%M%S")

            if (int(now) - int(last_toggle_time)) >= 10:
                light = 1 - light
                last_toggle_time = now

            self.traffic_flow(vehicle_id, light, url)

    def traffic_flow(self, vehicle_id, light, url):
        now = datetime.now()
        time_interval = now.minute

        weights = [1] * 31
        if time_interval < 10:
            weights[0] = 3
            weights[6] = 3
        elif time_interval < 20:
            weights[1] = 3
            weights[7] = 3
        elif time_interval < 30:
            weights[2] = 3
            weights[8] = 3
        elif time_interval < 40:
            weights[3] = 3
            weights[9] = 3
        elif time_interval < 50:
            weights[4] = 3
            weights[10] = 3
        else:
            weights[5] = 3
            weights[11] = 3

        junction = random.choices(Junction.objects.all(), weights=weights, k=1)[0]
        vehicle = Vehicle.objects.get(id=vehicle_id)
        plate = Plates.objects.get(id=vehicle.PlateNumber_id)
        speed = random.randint(40, 60) if light else 0

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
