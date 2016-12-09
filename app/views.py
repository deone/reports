from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from utils import get_collection

import requests

def index(request):
    response = requests.get(settings.VENDOR_VENDORS_URL).json()
    vendors = response['results']['vendors']
    voucher_values = response['results']['voucher_values']

    # Add more key/value pairs to vendor objects

    # Add date
    now = timezone.now()
    [vendor.update({'date': now}) for vendor in vendors]

    # Add total vend value
    [vendor.update({
        'total_vend_value': sum([vc['value'] * vc['count'] for vc in vendor['vend_count']])
    }) for vendor in vendors]

    # Add total vend count
    [vendor.update({
        'total_vend_count': sum([vc['count'] for vc in vendor['vend_count']])
    }) for vendor in vendors]
    
    # Create CSV file
    file_name = '%s_%s_%s_%s.%s' % (
        'Vend_Report', str(now.day), str(now.month), str(now.year), 'csv'
        )

    header = '%s%s%s%s%s\n' % (
        'Vendor Name,',
        'Vendor Company,',
        ','.join([str(value) for value in voucher_values]),
        ',Total Vend Value',
        ',Total Vend Count'
        )
    
    with open(file_name, 'a') as f:
        f.write(header)
        for vendor in vendors:
            vend_count = vendor['vend_count']
            vend_count_string = ','.join([str(elem['count']) for elem in vend_count])
            line = '%s,%s,%s,%s,%s\n' % (
                vendor['name'],
                vendor['company_name'],
                vend_count_string,
                vendor['total_vend_value'],
                vendor['total_vend_count']
                )

            f.write(line)

    # Insert into database
    # vendor_collection = get_collection('vendors')
    # result = vendor_collection.insert_many(vendors)

    # Send email

    return JsonResponse({'status': 'ok'})