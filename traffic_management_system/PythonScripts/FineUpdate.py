import time
from traffic_management.models import Fine


def update_fines():
    while True:
        try:
            all_fines = Fine.objects.all()

            for fine in all_fines:
                fine.fine = fine.fine * 1.1
                fine.save()

            time.sleep(5)
        except Exception as e:
            print(f"Error updating fines: {e}")


if __name__ == "__main__":
    update_fines()
