from reportlab.pdfgen import canvas
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json
import re
import random
from django.core.mail import EmailMessage
from .models import Vehicle, Junction, Owner, Plates, Log, Fine, DriverLicense
import os

sc_number = r'[^\w\s]|\d'
@csrf_exempt
def register_owner(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))

            Owner_name = data.get("name")
            Owner_age = data.get("age")
            Owner_phone = data.get("phone")
            Owner_email = data.get("email")
            Owner_address = data.get("address")
            Owner_driver_license = data.get("driver_license")

            if not Owner_name or not isinstance(Owner_name, str) or re.search(r'\d|[^A-Za-z\s]', Owner_name):
                return JsonResponse({'error': "Invalid or missing Owner_name"}, status=400)

            if not Owner_age or not isinstance(Owner_age, int) or not (16 <= Owner_age <= 80):
                return JsonResponse({'error': "Owner should be between 16 and 80 to be qualified"}, status=400)

            if not Owner_phone or not isinstance(Owner_phone, str):
                return JsonResponse({'error': "Invalid or missing Owner_phone"}, status=400)

            if not Owner_email or not isinstance(Owner_email, str):
                return JsonResponse({'error': "Invalid or missing Owner_email"}, status=400)

            if not Owner_address or not isinstance(Owner_address, str):
                return JsonResponse({'error': "Invalid or missing Owner_address"}, status=400)

            if not Owner_driver_license or not isinstance(Owner_driver_license, str):
                return JsonResponse({'error': "Invalid or missing Owner_driver_license"}, status=400)

            exist_owner = Owner.objects.filter(Owner_phone=Owner_phone).first()
            if exist_owner:
                return JsonResponse({'error': "Owner with the same phone number already exists"}, status=400)

            owner = Owner.objects.create(
                Owner_name=Owner_name,
                Owner_age=Owner_age,
                Owner_phone=Owner_phone,
                Owner_email=Owner_email,
                Owner_address=Owner_address,
                Owner_driver_license=Owner_driver_license
            )

            return JsonResponse({'Owner_id': owner.id})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f"Invalid JSON format: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': "This endpoint only supports POST requests"}, status=405)


@csrf_exempt
def register_junction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            address = data.get("address")

            if not address or address == "":
                return JsonResponse({'error': "Address not specified"}, status=400)

            if not isinstance(address, str):
                return JsonResponse({'error': "Address should be a string!"}, status=400)

            try:
                junction, created = Junction.objects.get_or_create(Address=address)
                if not created:
                    return JsonResponse({'error': "Junction is already registered!"}, status=400)

                return JsonResponse({'status': "Junction registered successfully", 'junction_id': junction.id})

            except IntegrityError as e:
                return JsonResponse({'error': str(e)}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': "Invalid JSON format"}, status=400)

    return JsonResponse({'error': "Invalid request method"}, status=405)


@csrf_exempt
def register_vehicle(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            owner_id = data.get("owner_id")
            color = data.get("color")
            vtype = data.get("type")

            if not owner_id or not isinstance(owner_id, int):
                return JsonResponse({'error': "Invalid or missing owner_id"}, status=400)

            owner = Owner.objects.filter(id=owner_id).first()
            if not owner:
                return JsonResponse({'error': "Owner hasn't registered yet"}, status=400)

            if not color or not isinstance(color, str):
                return JsonResponse({'error': "Invalid or missing color"}, status=400)

            if not vtype or not isinstance(vtype, str):
                return JsonResponse({'error': "Missing type"}, status=400)

            # Check vehicle condition
            condition_score = random.randint(48, 99)
            if condition_score < 50:
                return JsonResponse({'error': "Vehicle condition unqualified"}, status=400)

            # Assign an available plate number
            available_plate = Plates.objects.filter(Status='available').first()
            if not available_plate:
                return JsonResponse({'error': "No available plates"}, status=400)

            # Update plate status to 'assigned'
            available_plate.Status = 'assigned'
            available_plate.save()

            vehicle = Vehicle.objects.create(
                Owner=owner, Color=color, VType=vtype, Speed=0,
                Condition=condition_score, PlateNumber=available_plate
            )

            return JsonResponse({'vehicle_id': vehicle.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': "Invalid request method"}, status=405)


@csrf_exempt
def logging(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            address = data.get('Junction')
            plateNumber = data.get('PlateNumber')
            speed = data.get('Speed')
            light = data.get('Light')

            plate = Plates.objects.get(Number=plateNumber)
            vehicle = Vehicle.objects.get(PlateNumber_id=plate.id)
            log = Log.objects.create(Junction=address, Vehicle_PlateNumber=plateNumber, Vehicle_Speed=speed)

            driver_license = DriverLicense.objects.get(Owner_id=vehicle.Owner_id)

            violation = []
            if driver_license.Status == 'Suspended':
                violation.append('Illegal Driving')
            if not plate:
                violation.append('Fake Plate Number')
            if light == 1:
                if speed == 0:
                    violation.append('Illegal Parking')
            if light == 0 and speed != 0:
                violation.append('Running Red Light')
            if speed > 60:
                speeding_percentage = (speed-60)*2
                if speeding_percentage < 20:
                    violation.append('Speeding')
                elif speeding_percentage < 40:
                    violation.append('Speeding20%')
                elif speeding_percentage < 60:
                    violation.append('Speeding40%')
                elif speeding_percentage < 80:
                    violation.append('Speeding60%')
                elif speeding_percentage < 100:
                    violation.append('Speeding80%')
                else:
                    violation.append('Speeding100%')

            if violation:
                issueFine(violation, plateNumber, address, log.Date, log.Time.strftime('%H:%M:%S'))
            else:
                violation = None

            logging_details = (f"{log.Date} {log.Time.strftime('%H:%M:%S')}, {address}, {plateNumber}, {vehicle.Color} "
                               f"{vehicle.VType}, {speed}km/h, Violation: {violation}")

            return JsonResponse({'Logging': logging_details})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def issueFine(violation, plateNumber, address, date, time):
    plate = Plates.objects.get(Number=plateNumber)
    vehicle = Vehicle.objects.get(PlateNumber_id=plate.id)
    owner = Owner.objects.get(id=vehicle.Owner_id)
    driver_license = DriverLicense.objects.get(Owner_id=owner.id)

# calculate fine
    fine = 0
    if 'Illegal Parking' in violation:
        fine += 50
    if 'Running Red Light' in violation:
        fine += 100
    if 'Fake Plate Number' in violation:
        fine += 1000
    if 'Illegal Driving' in violation:
        fine += 2000
    if 'Speeding' in violation:
        fine += 50
    if 'Speeding20%' in violation:
        fine += 100
    if 'Speeding40%' in violation:
        fine += 200
    if 'Speeding60%' in violation:
        fine += 300
    if 'Speeding80%' in violation:
        fine += 400
    if 'Speeding100%' in violation:
        fine += 500

# License Score Update
    currentScore = driver_license.Score-fine/100
    DriverLicense.objects.filter(Owner_id=owner.id).update(Score=currentScore)
    if currentScore <= 0:
        DriverLicense.objects.filter(Owner_id=owner.id).update(Status='Suspended')

# Generate notice
    pdf = canvas.Canvas(f"E:\\LU_Leipzig\\ProgramClinic\\Project3\\Fine_for_{owner.Owner_name}.pdf")
    pdf.setFont("Helvetica-Bold", 18)
    textobject = pdf.beginText(210, 800)
    textobject.textLines("The City of Leipzig\n\nNotice of Violation\n\n")
    pdf.drawText(textobject)

    pdf.setFont("Helvetica", 12)
    textobject = pdf.beginText(50, 700)
    if currentScore <= 0:
        messagebody = (f"Mr./Ms. {owner.Owner_name}:\n\nYour Vehicle {plateNumber}  {violation}\n\n"
                       f"at {address} in {date} at {time}\n\n"
                       f"Your Driver License has been SUSPENDED.\n\n"
                       f"You need to pay the total fine ${fine} in one week!\n\n"
                       f"Fine for delaying payment is 10% every week!\n\n"
                       f"You have the right to appeal within one month of this notice.")
    else:
        messagebody = (f"Mr./Ms. {owner.Owner_name}:\n\nYour Vehicle {plateNumber}  {violation}\n\n"
                       f"at {address} in {date} at {time}\n\n"
                       f"Your Driver License has {currentScore} left.\n\n"
                       f"You need to pay the total fine ${fine} in one week!\n\n"
                       f"Fine for delaying payment is 10% every week!\n\n"
                       f"You have the right to appeal within one month of this notice.")

    textobject.textLines(messagebody)
    pdf.drawText(textobject)

    pdf.setFont("Times-Roman", 10)
    textobject = pdf.beginText(400, 500)
    textobject.textLines(f"IBAN: DE03790412379328765326\nBIC: COBADEFFXXX\n"
                         f"Bank: Commerzbank AG\nHolder: Hongtao Li")
    pdf.drawText(textobject)
    pdf.save()

    existing_fine = Fine.objects.filter(owner_id=owner.id).first()
    if existing_fine:
        current_fine = existing_fine.fine + fine
        Fine.objects.filter(owner_id=owner.id).update(fine=current_fine, status='notified')
    else:
        Fine.objects.create(fine=fine, owner=owner, status='notified')

# Email notice
    subject = 'Violation Notice LEIPZIG TRAFFIC POLICE'
    message = messagebody
    from_email = 'leipzig_traffic@outlook.com'
    recipient_list = [owner.Owner_email]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach_file(f'E:\\LU_Leipzig\\ProgramClinic\\Project3\\Fine_for_{owner.Owner_name}.pdf')
    email.send()


@csrf_exempt
def payFine(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            driver_license = data.get('Driver_license')
            fine = data.get('Fine')

            if not isinstance(fine, int):
                return JsonResponse({'Error': 'The smallest unit is $1'})

            owner = Owner.objects.get(Owner_driver_license=driver_license)
            currentfine = Fine.objects.filter(owner_id=owner.id).first()
            balance = currentfine.fine - fine
            if balance > 0:
                Fine.objects.filter(owner_id=owner.id).update(fine=balance)
                Fine.objects.filter(owner_id=owner.id).update(status="partPaid")
                return JsonResponse({'Balance': balance, 'Status': 'partPaid'})
            elif balance <= 0:
                Fine.objects.filter(owner_id=owner.id).update(fine=balance)
                Fine.objects.filter(owner_id=owner.id).update(status="fullyPaid")
                return JsonResponse({'Balance': balance, 'Status': 'fullyPaid'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def send_congestion_notification_email(junction_name, drivers_emails):

    message = f"Dear driver, please avoid {junction_name} as it is congested."

    subject = 'Congested Area Notification'
    from_email = 'leipzig_traffic@outlook.com'

    email = EmailMessage(subject, message, from_email, drivers_emails)
    email.send()

    print("Congestion notification email sent successfully.")

junction_name = "Sample Junction"
drivers_emails = ["drivrs1, drivrs2", "drivrs3"]
send_congestion_notification_email(junction_name, drivers_emails)