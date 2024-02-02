import requests
import json
from faker import Faker
from faker_vehicle import VehicleProvider

fake = Faker()
fake.add_provider(VehicleProvider)

def register_vehicle(owner_id):
    url = "http://localhost:8000/traffic_management/register_vehicle"

    data = {
        "owner_id": owner_id,
        "color": fake.color_name(),
        "type": fake.vehicle_year_make_model()
    }

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        print(f"Vehicle registered successfully. Vehicle ID: {response.json().get('vehicle_id')}")
    else:
        print(f"Error registering vehicle: {response.json().get('error')}")

if __name__ == "__main__":
    for owner_id in range(297, 300):
        register_vehicle(owner_id)
