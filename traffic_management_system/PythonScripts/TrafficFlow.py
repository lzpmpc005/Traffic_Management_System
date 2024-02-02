import requests
import json
from random import randrange
from traffic_management.models import Vehicle, Plates, Junction
from datetime import datetime


def traffic_flow(vehicle_id, light):
    url = "http://localhost:8000/traffic_management/logging"

    junction = Junction.objects.get(id=randrange(1, 13))
    vehicle = Vehicle.objects.get(id=vehicle_id)
    plate = Plates.objects.get(id=vehicle.PlateNumber_id)


    speed = randrange(40, 60) if light else 0

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
    last_toggle_time = datetime.now().strftime("%M%S")

    for vehicle_id in range(4, 119):
        now = datetime.now().strftime("%M%S")

        if (int(now) - int(last_toggle_time)) >= 10:
            light = 1 - light
            last_toggle_time = now

        traffic_flow(vehicle_id, light)