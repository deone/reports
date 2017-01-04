from django.conf import settings
from django.utils import timezone

from pymongo import MongoClient

import requests

import os
import datetime

from decimal import Decimal
from collections import OrderedDict

def validate_date(year=None, month=None, day=None):
    if year:
        year = int(year)
    if month:
        month = int(month)
    if day:
        day = int(day)

    now = timezone.now()
    date = OrderedDict()

    # URL contains only year
    if month is None and day is None and year:
        if year > now.year:
            return JsonResponse({'code': 500, 'message': 'Invalid year.'})
        else:
            date['year'] = year

    # URL contains year and month
    elif day is None and month and year:
        if year > now.year or month > now.month:
            return JsonResponse({'code': 500, 'message': 'Invalid year or month.'})
        else:
            date['month'] = month
            date['year'] = year

    # URL contains year, month and day
    elif year and month and day:
        date_supplied = datetime.date(year, month, day)
        if date_supplied > now.date():
            return JsonResponse({'code': 500, 'message': 'Invalid date.'})
        else:
            date['day'] = day
            date['month'] = month
            date['year'] = year

    return date

def create_file(service, date=None, _from=None, to=None):
    # Create CSV file
    now = timezone.now()
    path = os.path.join(settings.STATICFILES_DIRS[0], 'files')

    file_name = service
    if date:
        file_name += '_' + ''.join(['%s-' % value for value in date.values()])[:-1]
        file_name += '.csv'

    return os.path.join(path, file_name)

def vends_reporter(date=None, _from=None, to=None):
    url = settings.VENDOR_VENDS_URL
    response = requests.get(url, params=date).json()

    vendors = response['results']['vendors']
    voucher_values = response['results']['voucher_values']

    # Add more key/value pairs to vendor objects

    # Add total vend value
    [vendor.update({
        'total_vend_value': sum([vc['value'] * vc['count'] for vc in vendor['vend_count']])
    }) for vendor in vendors]

    # Add total vend count
    [vendor.update({
        'total_vend_count': sum([vc['count'] for vc in vendor['vend_count']])
    }) for vendor in vendors]

    file = create_file('vends', date)

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

    return file

def send_report(request, file):
    pass
    # Send email
    """ url = request.build_absolute_uri()
    requests.get(settings.MESSAGING_URL, params={
        'subject': 'Test Subject',
        'message': 'Test Message',
        'sender': 'incisiaappmailer@gmail.com',
        'recipients': ['alwaysdeone@gmail.com'],
        'file': url + file,
    }) """

REPORT_HANDLERS = {
    'vends': vends_reporter,
}

def create_and_send_report(request, service, date=None, _from=None, to=None):
    report = REPORT_HANDLERS[service]

    if date:
        file_name = report(date=date)
    # send_report(request, file_name)

def get_collection(collection_name):
    client = MongoClient()
    db = client.reports
    return db[collection_name]