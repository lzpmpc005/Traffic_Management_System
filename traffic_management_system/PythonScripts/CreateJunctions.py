import requests
import json
from faker import Faker

fake = Faker()

def register_junction(address):
    url = "http://localhost:8000/traffic_management/register_junction"

    data = {
        "address": address,
    }

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        print(f"Junction registered successfully. Junction ID: {response.json().get('junction_id')}")
    else:
        print(f"Error registering junction: {response.json().get('error')}")

if __name__ == "__main__":
    for i in range(1, 11):
        junction_address = fake.street_address()
        register_junction(junction_address)
