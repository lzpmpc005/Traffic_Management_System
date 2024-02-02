import random
from faker import Faker
from traffic_management.models import Owner

fake = Faker()

def create_random_owners(num_owners=100):
    print("Creating owners...")
    for _ in range(num_owners):
        Owner.objects.create(
            Owner_name=fake.name(),
            Owner_age=random.randint(16, 80),
            Owner_phone='+49 ' + fake.numerify(text='###########'),
            Owner_email=fake.email()[:20],
            Owner_address=fake.address(),
            Owner_driver_license=str(fake.random_int(min=1000000000, max=9999999999)),
        )


if __name__ == "__main__":
    try:
        create_random_owners()
        print("Owners created successfully.")
    except Exception as e:
        print(f"Error: {e}")
