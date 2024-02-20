from reportlab.pdfgen import canvas
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json
import re
import random
from django.core.mail import EmailMessage
from .models import Vehicle, Junction, Owner, Plates, Log, Fine, DriverLicense, StatReport, Street
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from datetime import datetime
import webbrowser
from django.db.models import Q
import heapq


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
            Jtype = data.get("type")

            if not address or address == "":
                return JsonResponse({'error': "Address not specified"}, status=400)

            if not isinstance(address, str):
                return JsonResponse({'error': "Address should be a string!"}, status=400)

            try:
                junction, created = Junction.objects.get_or_create(Address=address, JType=Jtype)
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
            available_plate = Plates.objects.filter(Status='reserved').first()
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
            destination = data.get('destination')

            junction = Junction.objects.get(Address=address)
            plate = Plates.objects.get(Number=plateNumber)
            vehicle = Vehicle.objects.get(PlateNumber_id=plate.id)
            log = Log.objects.create(Junction=junction, Vehicle_PlateNumber=plateNumber, Vehicle_Speed=speed)

            # detect emergency vehicle and point the fastest route to the destination
            if 'S' in plateNumber:
                if destination:
                    if destination == junction.id:
                        return JsonResponse({'next_junction': 0})
                    shortest_path = calculate_shortest_path(junction.id, destination)
                    next_junction = shortest_path[1]

                    street1 = Street.objects.filter(
                        Q(Start_junction_id=junction.id, End_junction_id=next_junction) |
                        Q(Start_junction_id=next_junction, End_junction_id=junction.id)).first()
                    if len(shortest_path) > 2:
                        street2 = Street.objects.filter(
                            Q(Start_junction_id=shortest_path[1], End_junction_id=shortest_path[2]) |
                            Q(Start_junction_id=shortest_path[2], End_junction_id=shortest_path[1])).first()
                    else:
                        street2 = None

                    # send email to drivers who passed the first 2 junctions within 1 minute to avoid the route
                    current_time = datetime.now()
                    date = current_time.date()
                    start_time = current_time.replace(minute=current_time.minute-1, second=0, microsecond=0).time()
                    end_time = current_time.strftime('%H:%M:%S')

                    logs = Log.objects.filter(
                        Date=date, Time__range=(start_time, end_time),
                        Junction_id__in=[shortest_path[0], shortest_path[1]]
                    ).exclude(Vehicle_PlateNumber=plateNumber)

                    if logs.exists():
                        for log in logs:
                            plate = Plates.objects.get(Number=log.Vehicle_PlateNumber)
                            vehicle = Vehicle.objects.get(PlateNumber_id=plate.id)
                            print(destination, vehicle.Owner_id)
                            street1_name = street1.Name
                            if street2:
                                street2_name = street2.Name
                            else:
                                street2_name = None
                            send_avoid_email(address, street1_name, street2_name, destination, vehicle.Owner_id)

                    return JsonResponse({'next_junction': next_junction})

            # detecting congestion and suggest alternative routes to drivers
            report = StatReport.objects.filter(Junction_id=log.Junction_id).order_by('-id').first()
            if report.Vehicle_Quantity == 30:
                send_congestion_notification_email(address, vehicle.Owner_id)

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

            # logging_details = (f"{log.Date} {log.Time.strftime('%H:%M:%S')}, {address}, id:{junction.id}, {plateNumber}, {vehicle.Color} "
            #                    f"{vehicle.VType}, {speed}km/h, Violation: {violation}")

            logging_details = f"Junction_id: {junction.id}, Vehicle: {plateNumber}"

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


def send_congestion_notification_email(junction_name, drivers_id):
    owner = Owner.objects.get(id=drivers_id)
    junction = Junction.objects.get(Address=junction_name)
    alter_junction = Junction.objects.get(id=junction.id + 1)

    message = (f"Dear Mr/Mrs. {owner.Owner_name}:\n\nThere is a congestion at {junction_name}."
               f"\nPlease drive to {alter_junction.Address} instead."
               f"\n\nRegard,\nLeipzig Traffic Police")

    subject = 'Congested Area Notification'
    from_email = 'leipzig_traffic@outlook.com'
    recipient_list = [owner.Owner_email]
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.send()


def generate_report(data, chart, columnX, columnY, time_period, junction_id, report_path):
    x_data = [item[1] for item in data]
    y_data = [item[0] for item in data]

    if chart == 'line':
        sorted_data = sorted(zip(x_data, y_data))
        x_data_sorted, y_data_sorted = zip(*sorted_data)

        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.15, top=0.9)

        ax.plot(x_data_sorted, y_data_sorted, marker='o', linestyle='-')

        ax.set_xticklabels(x_data_sorted)

    elif chart == 'bar':
        fig, ax = plt.subplots()
        ax.bar(x_data, y_data)
        ax.set_xticks(x_data)
        ax.set_xticklabels(x_data, rotation=45)

    ax.set_xlabel(columnX)
    ax.set_ylabel(columnY)
    if junction_id != 0:
        ax.set_title(f'Traffic Flow and Congestion Report\n{time_period}  Junction {junction_id}')
    else:
        ax.set_title(f'Traffic Flow and Congestion Report\n{time_period}')

    buffer = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.draw()
    fig.savefig(buffer, format='pdf')
    with open(report_path, 'wb') as f:
        f.write(buffer.getvalue())
    plt.close(fig)


@csrf_exempt
def retrieveReport(request):
    try:
        date = request.GET.get('Date')  # yyyy-mm-dd (2024-02-09)
        start_time = request.GET.get('Time_From')  # hh:mm:ss (18:10:00)
        end_time = request.GET.get('Time_To')
        junction_id = request.GET.get('Junction_id')  # 1-12

        current_time = datetime.now()

        if not date or date == '':
            date = current_time.date()
        if not start_time or start_time == '':
            start_time = current_time.replace(minute=(current_time.minute // 10) * 10, second=0, microsecond=0).time()
        if not end_time or end_time == '':
            end_time = current_time.strftime('%H:%M:%S')

        time_period = f'{date}   {start_time}-{end_time}'
        report_path = 'E:\\LU_Leipzig\\ProgramClinic\\Project3\\traffic_report.pdf'

        if not junction_id or junction_id == '':
            data = (StatReport.objects.filter(Date=date, Time__range=(start_time, end_time))
                    .values_list('Vehicle_Quantity', 'Junction_id'))
            columnX = 'Junction_id'
            columnY = 'Vehicle_Quantity'
            generate_report(data, "bar", columnX, columnY, time_period, 0, report_path)

        else:
            data = (StatReport.objects.filter(Date=date, Time__range=(start_time, end_time),
                                              Junction_id=junction_id).values_list('Vehicle_Quantity', 'Time'))

            data = [(quantity, time.hour * 100 + time.minute) for quantity, time in data]
            columnX = 'Time_Period'
            columnY = 'Vehicle_Quantity'
            generate_report(data, "line", columnX, columnY, time_period, junction_id, report_path)

        webbrowser.open(report_path)

        return JsonResponse({'Traffic Report Period:': time_period,
                             'Traffic Report Location': report_path})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def register_route(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            start_junction_id = data.get("start")
            end_junction_id = data.get("end")
            distance = data.get("distance")
            name = data.get("name")

            start_junction = Junction.objects.get(id=start_junction_id)
            end_junction = Junction.objects.get(id=end_junction_id)

            try:
                street = Street.objects.create(Start_junction=start_junction, End_junction=end_junction,
                                             Distance=distance, Name=name)
                return JsonResponse({'status': "Route registered successfully", 'route_id': street.id})

            except IntegrityError as e:
                return JsonResponse({'error': str(e)}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': "Invalid JSON format"}, status=400)
    return JsonResponse({'error': "Invalid request method"}, status=405)


def calculate_shortest_path(start_id, destination_id):
    # Dijkstra's algorithm to find the shortest path
    junctions = Junction.objects.all()
    distances = {junction.id: float('inf') for junction in junctions}
    distances[start_id] = 0
    previous = {junction.id: None for junction in junctions}
    visited = set()

    priority_queue = [(0, start_id)]

    while priority_queue:
        current_distance, current_id = heapq.heappop(priority_queue)
        if current_id in visited:
            continue
        visited.add(current_id)

        for street in Street.objects.filter(Q(Start_junction_id=current_id) | Q(End_junction_id=current_id)):
            neighbor_id = street.Start_junction_id if street.End_junction_id == current_id else street.End_junction_id
            if neighbor_id in visited:
                continue
            if is_congested(neighbor_id):
                continue
            new_distance = current_distance + street.Distance
            if new_distance < distances[neighbor_id]:
                distances[neighbor_id] = new_distance
                previous[neighbor_id] = current_id
                heapq.heappush(priority_queue, (new_distance, neighbor_id))

    shortest_path = []
    current_id = destination_id
    while current_id is not None:
        shortest_path.insert(0, current_id)
        current_id = previous[current_id]

    return shortest_path


def is_congested(junction_id):
    current_time = datetime.now()
    date = current_time.date()
    start_time = current_time.replace(minute=(current_time.minute // 10) * 10, second=0, microsecond=0).time()
    end_time = current_time.strftime('%H:%M:%S')

    latest_report = (StatReport.objects.filter(Date=date, Time__range=(start_time, end_time),
                                               Junction_id=junction_id)).first()
    if latest_report is not None and latest_report.Vehicle_Quantity >= 20:
        return True
    else:
        return False


def send_avoid_email(junction_name, street1, street2, destination, drivers_id):
    owner = Owner.objects.get(id=drivers_id)
    destination_junction = Junction.objects.get(id=destination)

    if street2 is None:
        message = (f"Dear Mr/Mrs. {owner.Owner_name}:\n\nThere is an emergency vehicle at {junction_name} \n"
                   f"heading to {destination_junction.Address}. \n"
                   f"Please avoid {street1} to make way.\n"
                   f"\nRegard,\nLeipzig Traffic Police")
    elif street1 == street2:
        message = (f"Dear Mr/Mrs. {owner.Owner_name}:\n\nThere is an emergency vehicle at {junction_name}\n "
                   f"heading to {destination_junction.Address}. \n"
                   f"Please avoid {street1} to make way.\n"
                   f"\nRegard,\nLeipzig Traffic Police")
    else:
        message = (f"Dear Mr/Mrs. {owner.Owner_name}:\n\nThere is an emergency vehicle at {junction_name}\n "
                   f"heading to {destination_junction.Address}. \n"
                   f"Please avoid {street1} and {street2} to make way.\n"
                   f"\nRegard,\nLeipzig Traffic Police")

    subject = 'Emergency Vehicle Notification'
    from_email = 'leipzig_traffic@outlook.com'
    recipient_list = [owner.Owner_email]
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.send()