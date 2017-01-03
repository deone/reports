from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from utils import get_collection

from decimal import Decimal
import requests
import os

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
    path = os.path.join(settings.STATICFILES_DIRS[0], 'files')
    file_name = '%s_%s_%s_%s.%s' % (
        'Vend_Report', str(now.day), str(now.month), str(now.year), 'csv'
        )

    file = os.path.join(path, file_name)

    header = '%s%s%s%s%s%s%s%s\n' % (
        'Vendor Name,',
        'Vendor Company,',
        ','.join([str(value) for value in voucher_values]),
        ',Total Vend Count',
        ',Total Vend Value (GHS)',
        ',Bonus',
        ',Commission',
        ',Net Revenue'
        )
    
    with open(file, 'w') as f:
        f.write(header)
        for vendor in vendors:
            vend_count = vendor['vend_count']
            vend_count_string = ','.join([str(elem['count']) for elem in vend_count])

            sales = Decimal(vendor['total_vend_value'])
            bonus = revenue = sales / 2
            commission = (sales - bonus) / 10
            net_revenue = revenue - commission

            line = '%s,%s,%s,%s,%s,%s,%s,%s\n' % (
                vendor['name'],
                vendor['company_name'],
                vend_count_string,
                vendor['total_vend_count'],
                str(sales),
                str(bonus),
                str(commission),
                str(net_revenue)
                )

            f.write(line)

    # Insert into database
    # vendor_collection = get_collection('vendors')
    # result = vendor_collection.insert_many(vendors)

    # Send email
    """ url = request.build_absolute_uri()
    requests.get(settings.MESSAGING_URL, params={
        'subject': 'Test Subject',
        'message': 'Test Message',
        'sender': 'incisiaappmailer@gmail.com',
        'recipients': ['alwaysdeone@gmail.com'],
        'file': url + 'static/files/' + file_name,
    }) """

    return JsonResponse({'status': 'ok'})