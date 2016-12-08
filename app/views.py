from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from utils import get_collection

import requests

def index(request):
    response = requests.get(settings.VEND_VENDORS_URL).json()
    vendors = response['results']

    # Add timestamp to vendor objects
    [vendor.update({'date': timezone.now()}) for vendor in vendors]

    vendor_collection = get_collection('vendors')
    result = vendor_collection.insert_many(vendors)
    print result.inserted_ids
    return JsonResponse({'status': 'ok'})