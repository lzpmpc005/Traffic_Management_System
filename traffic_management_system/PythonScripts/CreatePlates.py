import random
import string
from traffic_management.models import Plates
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traffic_management_system.settings")

django.setup()


def generate_plate_number():
    numbers = random.choices(string.digits, k=3)
    return 'LP S' + ''.join(numbers)


def create_plates():
    for _ in range(100):
        plate_number = generate_plate_number()
        Plates.objects.create(Number=plate_number, Status='reserved')


if __name__ == "__main__":
    create_plates()

