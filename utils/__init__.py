from django.conf import settings
from django.utils import timezone

from pymongo import MongoClient

import requests

import os

from decimal import Decimal
from collections import OrderedDict

def order_stringify_date(date):
    year, month, day = tuple(date.split('-'))
    dct = order_date(year, month, day)
    return ''.join(['%s-' % value for value in reversed(dct.values())])[:-1]

def order_date(year=None, month=None, day=None):
    if year:
        year = int(year)
    if month:
        month = int(month)
    if day:
        day = int(day)

    date = OrderedDict()

    # URL contains only year
    if month is None and day is None and year:
        date['year'] = year

    # URL contains year and month
    elif day is None and month and year:
        date['month'] = month
        date['year'] = year

    # URL contains year, month and day
    elif year and month and day:
        date['day'] = day
        date['month'] = month
        date['year'] = year

    return date

def create_file_name(service, date=None, _from=None, to=None):
    file_name = service
    if date:
        file_name += '_'
        file_name += ''.join(['%s-' % value for value in date.values()])[:-1]
    else:
        file_name += '_'
        file_name += ''.join(['%s-' % v for v in _from.split('-')[::-1]])[:-1]
        file_name += '_to_'
        file_name += ''.join(['%s-' % v for v in to.split('-')[::-1]])[:-1]

    file_name += '.csv'
    return file_name

def vends_reporter(date=None, _from=None, to=None):
    url = settings.VENDOR_VENDS_URL

    if date:
        response = requests.get(url, params=date).json()
        file_name = create_file_name('vends', date=date)
    else:
        response = requests.get(url, params={'from': _from, 'to': to}).json()
        file_name = create_file_name('vends', _from=_from, to=to)

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

    path = os.path.join(settings.STATICFILES_DIRS[0], 'files')
    file = os.path.join(path, file_name)

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

    return file_name

def send_report(request, file):
    # Send email
    url = request.build_absolute_uri()
    requests.get(settings.MESSAGING_URL, params={
        'subject': 'Test Subject',
        'message': 'Test Message',
        'sender': 'incisiaappmailer@gmail.com',
        'recipients': ['alwaysdeone@gmail.com'],
        'file': url + file,
    })

REPORT_HANDLERS = {
    'vends': vends_reporter,
}

def create_and_send_report(request, service, date=None, _from=None, to=None):
    report = REPORT_HANDLERS[service]

    if date:
        file_name = report(date=date)
    else:
        file_name = report(_from=_from, to=to)

    # print request.build_absolute_uri()
    print settings.STATIC_URL
    print file_name
    # send_report(request, file_name)

def get_collection(collection_name):
    client = MongoClient()
    db = client.reports
    return db[collection_name]