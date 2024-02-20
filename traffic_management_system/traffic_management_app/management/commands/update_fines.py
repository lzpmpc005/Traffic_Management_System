from django.core.management.base import BaseCommand
from traffic_management_app.models import Fine
import time

class Command(BaseCommand):
    help = 'Update fines every 5 seconds'

    def handle(self, *args, **kwargs):
        while True:
            try:
                all_fines = Fine.objects.all()

                for fine in all_fines:
                    fine.fine *= 1.1
                    fine.save()

                time.sleep(5)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error updating fines: {e}"))