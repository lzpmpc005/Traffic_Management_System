from django.core.management.base import BaseCommand
from time import sleep
import requests
import json
from traffic_management_app.models import Vehicle, Plates, Junction, Street
import random
from datetime import datetime
from django.db.models import Q


class Command(BaseCommand):
    help = 'Simulate vehicle driving behavior'

    def handle(self, *args, **kwargs):
        light = 1
        last_toggle_time = datetime.now().strftime("%M%S")
        end = random.randint(1, 30)
        street = Street.objects.filter(Start_junction_id=end).first()
        vehicle_id = random.randint(120, 129)

        while True:
            now = datetime.now().strftime("%M%S")

            if (int(now) - int(last_toggle_time)) >= 10:
                light = 1 - light
                last_toggle_time = now

            speed = random.randint(30, 60) if light else 0
            if speed == 0:
                time_cost = 12 * street.Distance / 30
            else:
                time_cost = 12 * street.Distance / speed
            sleep(time_cost)

            end = street.End_junction_id if street.Start_junction_id == end else street.Start_junction_id

            self.drive(light, speed, end, vehicle_id)

            street = random.choice(
                Street.objects.filter(
                    Q(Start_junction_id=end) | Q(End_junction_id=end)
                )
            )

    def drive(self, light, speed, junction_id, vehicle_id):
        url = "http://localhost:8000/traffic_management/logging"

        vehicle = Vehicle.objects.get(id=vehicle_id)
        plate = Plates.objects.get(id=vehicle.PlateNumber_id)
        junction = Junction.objects.get(id=junction_id)

        data = {
            "Junction": junction.Address,
            "PlateNumber": plate.Number,
            "Speed": speed,
            "Light": light
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS(str(response.json())))
        else:
            self.stdout.write(self.style.ERROR(str(response.json().get('error'))))
