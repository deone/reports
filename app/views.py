from django.conf import settings
from django.http import JsonResponse

from utils import get_collection

import requests

def index(request):
    response = requests.get(settings.VEND_VENDORS_URL).json()
    vendors = response['results']

    vendor_collection = get_collection('vendors')
    result = vendor_collection.insert_many(vendors)
    print result.inserted_ids
    return JsonResponse({'status': 'ok'})