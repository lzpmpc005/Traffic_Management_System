import requests
import json
from random import randrange
import random
from traffic_management.models import Vehicle, Plates, Junction
import time


def traffic_flow(vehicle_id, light):
    url = "http://localhost:8000/traffic_management/logging"

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

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        print(response.json())
    else:
        print(response.json().get('error'))


if __name__ == "__main__":

    light = 1

    for _ in range(10):
        vehicle_id = random.randint(4, 119)

        light = 1 - light

        traffic_flow(vehicle_id, light)
        time.sleep(20)