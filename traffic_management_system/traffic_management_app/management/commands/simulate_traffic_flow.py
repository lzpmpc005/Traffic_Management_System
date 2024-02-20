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
            vehicle_id = random.randint(4, 119)
            now = datetime.now().strftime("%M%S")

            if (int(now) - int(last_toggle_time)) >= 10:
                light = 1 - light
                last_toggle_time = now

            self.traffic_flow(vehicle_id, light, url)

    def traffic_flow(self, vehicle_id, light, url):
        now = datetime.now()
        time_interval = now.minute
        weights = self.cal_weights(time_interval)

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
            self.stdout.write(self.style.SUCCESS(str(response.json())))
        else:
            self.stdout.write(self.style.ERROR(str(response.json().get('error'))))

    def cal_weights(self, time_interval):
        i = time_interval//10
        indices = [i, i+6, i+12, i+18, i+24]
        weights = [1] * 31
        for i in indices:
            weights[i] = random.randint(2, 10)
        return weights