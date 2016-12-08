from django.conf import settings
from django.http import JsonResponse

from utils import get_collection

import requests

def index(request):
    response = requests.get(settings.VEND_VENDORS_URL).json()
    vendors = get_collection('vendors')
    vendor = {"phone_number": "0231802940", "name": "Ruben Mawuji", "company_name": "Spectra Wireless"}
    vendor_id = vendors.insert_one(vendor).inserted_id
    print vendor_id
    return JsonResponse({'status': 'ok'})