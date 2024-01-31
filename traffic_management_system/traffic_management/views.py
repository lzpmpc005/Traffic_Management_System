from .models import Vehicle, Junction, Owner
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import random
import string

sc_number = r'[^\w\s]|\d'
@csrf_exempt
def register_owner(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            Owner_name = data.get("name")
            Owner_phone = data.get("phone")
            Owner_email = data.get("email")
            Owner_address = data.get("address")
# Imperative programming
            if not Owner_name or Owner_name == "":
                return JsonResponse({'error': "Owner_name not specified"}, status=400)
            if not isinstance(Owner_name, str):
                return JsonResponse({'error': "Owner_name should be string!"}, status=400)
            if re.search(sc_number, Owner_name):
                return JsonResponse({'error': "Owner_name contains number or special character"}, status=400)

            if not Owner_phone or Owner_phone == "":
                return JsonResponse({'error': "Owner_phone not specified"}, status=400)
            if not isinstance(Owner_name, str):
                return JsonResponse({'error': "Owner_phone should be string!"}, status=400)

            if not Owner_email or Owner_email == "":
                return JsonResponse({'error': "Owner_email not specified"}, status=400)
            if not isinstance(Owner_email, str):
                return JsonResponse({'error': "Owner_email should be string!"}, status=400)

            if not Owner_address or Owner_address == "":
                return JsonResponse({'error': "Owner_address not specified"}, status=400)
            if not isinstance(Owner_address, str):
                return JsonResponse({'error': "Owner_address should be string!"}, status=400)

            exist_owner = Owner.objects.filter(Owner_phone=Owner_phone).first()
            if exist_owner:
                return JsonResponse({'error': "Owner is already exist!"}, status=400)

            owner = Owner.objects.create(Owner_name=Owner_name, Owner_phone=Owner_phone, Owner_email=Owner_email, Owner_address=Owner_address)
            return JsonResponse({'Owner_id': owner.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

from django.http import JsonResponse

def generate_plate_number():
    random_chars=''.join(random.choice(string.ascii_uppercase+string.digits, k=5))
    plate_number = f"L-{random_chars}"
    return plate_number

@csrf_exempt
def register_vehicle(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))

            owner_id = data.get("owner_id")
            color = data.get("color")
            producer = data.get("producer")
            type = data.get("type")
            year = data.get("year")
            speed = data.get("speed")
            condition = data.get("condition")
            if not producer or producer == "":
                return JsonResponse({"error": "Producer is required!"}, status=400)
            if not color or color =="":
                return JsonResponse({"error": "color is required"}, status=400)
            if not type or type == "":
                return JsonResponse({'error': "Vehicle type not specified"}, status=400)
            if not owner_id:
                return JsonResponse({'error': "Owner ID not specified"}, status=400)
            if not year or year == "":
                return JsonResponse({'error': "Year not specified"})
            if not speed or speed == "":
                return JsonResponse({'error': "Speed"})
            if not condition or condition == "":
                return JsonResponse({'error': "Condition"})
            owner = Owner.objects.filter(id=owner_id).first()
            if not owner:
                return JsonResponse({'error': "Owner does not exist"}, status=400)

            plate_number=generate_plate_number()
            vehicle = Vehicle.objects.create(plate_number=plate_number, vehicle_type=vehicle_type, owner=owner)
            return JsonResponse({'vehicle_id': vehicle.id,"plate_number": plate_number})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    elif request.method == 'GET':
        return JsonResponse({'message': 'This endpoint only supports POST requests'}, status=405)

@csrf_exempt
def register_junction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            Address = data.get("address")

            if not Address or Address == "":
                return JsonResponse({'error': "Address not specified"}, status=400)
            if not isinstance(Address, str):
                return JsonResponse({'error': "Address should be string!"}, status=400)

            exist_junction = Junction.objects.filter(Address=Address).first()
            if exist_junction:
                return JsonResponse({'error': "Junction is already registered!"}, status=400)

            junction = Junction.objects.create(Address=Address)
            return JsonResponse({'junction_id': junction.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def recognize_vehicle(request):
    try:
        color = request.GET.get('color')
        producer = request.GET.get('producer')
        type = request.GET.get('type')

        if not color or color == "":
            return JsonResponse({'error': "color not specified"}, status=400)
        if not isinstance(color, str):
            return JsonResponse({'error': "color should be string!"}, status=400)

        if not producer or producer == "":
            return JsonResponse({'error': "producer not specified"}, status=400)
        if not isinstance(producer, str):
            return JsonResponse({'error': "producer should be string!"}, status=400)
        if re.search(sc_number, producer):
            return JsonResponse({'error': "producer contains number or special character"}, status=400)

        if not type or type == "":
            return JsonResponse({'error': "type not specified"}, status=400)
        if not isinstance(type, str):
            return JsonResponse({'error': "type should be string!"}, status=400)
        if re.search(sc_number, type):
            return JsonResponse({'error': "type contains number or special character"}, status=400)

        vehicle = Vehicle.objects.filter(Color=color, Producer=producer, Type=type).first()
        return JsonResponse({'Plate_number': vehicle.Number})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

