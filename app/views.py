from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from utils import get_collection

import requests

def index(request):
    response = requests.get(settings.VENDOR_VENDORS_URL).json()
    vendors = response['results']['vendors']
    voucher_values = response['results']['voucher_values']

    # Add timestamp to vendor objects
    now = timezone.now()
    [vendor.update({'date': now}) for vendor in vendors]

    vendor_collection = get_collection('vendors')
    # result = vendor_collection.insert_many(vendors)
    
    # Create CSV file
    file_name = '%s_%s_%s_%s.%s' % ('Vend_Report', str(now.day), str(now.month), str(now.year), 'csv')
    voucher_values_line = '%s%s%s' % ('Vendor Name,Vendor Company,', ','.join([str(x) for x in voucher_values]), '\n')
    
    with open(file_name, 'a') as f:
        f.write(voucher_values_line)
        for vendor in vendors:
            vend_count = vendor['vend_count']
            vendor_report_line = '%s,%s,%s,%s,%s,%s,%s\n' % (
                vendor['name'],
                vendor['company_name'],
                vend_count[0]['1'],
                vend_count[1]['2'],
                vend_count[2]['5'],
                vend_count[3]['10'],
                vend_count[4]['20']
                )
            f.write(vendor_report_line)

    # Send email

    return JsonResponse({'status': 'ok'})