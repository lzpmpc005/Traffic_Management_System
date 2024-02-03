from traffic_management.models import Owner, DriverLicense
def create_driver_license(owner_id):

    owner = Owner.objects.get(id=owner_id)

    DriverLicense.objects.create(
        Owner=owner,
        License_Number=owner.Owner_driver_license,
    )


if __name__ == "__main__":
    for id in range(297, 486):
        create_driver_license(id)