from .models import Vehicle, Junction, Owner
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re

def validate_string(string):
    if not string or string == "":
        return JsonResponse({'error': f"{string} not specified"}, status=400)

    if not isinstance(string, str):
        return JsonResponse({'error': f"{string} should be string!"}, status=400)

    sc_number = r'[^\w\s]|\d'
    if re.search(sc_number, string):
        return JsonResponse({'error': f"{string} contains number or special character"}, status=400)


@csrf_exempt
def register_owner(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            Owner_name = data.get("name")
            Owner_phone = data.get("phone")
            Owner_address = data.get("address")

            validate_string(Owner_name)

            exist_owner = Owner.objects.filter(Owner_phone=Owner_phone).first()
            if exist_owner:
                return JsonResponse({'error': "Owner is already exist!"}, status=400)

            owner = Owner.objects.create(Owner_name=Owner_name, Owner_phone=Owner_phone, Owner_address=Owner_address)
            return JsonResponse({'Owner_id': owner.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def register_junction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            Address = data.get("address")

            if not Address or Address == "":
                return JsonResponse({'error': "Address not specified"}, status=400)

            exist_junction = Junction.objects.filter(Address=Address).first()
            if exist_junction:
                return JsonResponse({'error': "Junction is already registered!"}, status=400)

            junction = Junction.objects.create(Address=Address)
            return JsonResponse({'junction_id': junction.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# @csrf_exempt
# def register_vehicle(request):