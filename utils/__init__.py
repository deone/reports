from django.conf import settings
from django.utils import timezone

from pymongo import MongoClient

import requests

import os

from decimal import Decimal

def stringify_date(date_list):
    return ''.join(['%s-' % elem for elem in date_list])[:-1]

def stringify_service_and_dates(service=None, date=None, _from=None, to=None):
    if service:
        string = service
    else:
        string = ''

    if date:
        if service:
            string += '_'
        string += stringify_date(date.values())
    else:
        if service:
            string += '_'
        string += stringify_date(_from.split('-'))
        if service:
            string += '_to_'
        else:
            string += ' To '
        string += stringify_date(to.split('-'))

    return string

def vends_reporter(date=None, _from=None, to=None):
    url = settings.VENDOR_VENDS_URL

    if date:
        response = requests.get(url, params=date).json()
        file_name = '%s.%s' % (stringify_service_and_dates(service='vends', date=date), 'csv')
    else:
        response = requests.get(url, params={'from': _from, 'to': to}).json()
        file_name = '%s.%s' % (stringify_service_and_dates(service='vends', _from=_from, to=to), 'csv')

    vendors = response['vendors']
    voucher_values = response['voucher_values']

    if vendors:
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

        _file = os.path.join(settings.MEDIA_ROOT, file_name)

        with open(_file, 'w') as f:
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

def send_report(service, _file, date=None, _from=None, to=None):
    subject_and_body = settings.EMAIL_SUBJECT_AND_BODY[service]
    subject = subject_and_body['subject']
    body = subject_and_body['body']

    period = stringify_service_and_dates(service=None, date=date, _from=_from, to=to)

    # Send email
    response = requests.get(settings.MESSAGING_URL, params={
        'subject': '%s: %s' % (subject, period),
        'message': body,
        'sender': settings.DEFAULT_FROM_EMAIL,
        'recipients': settings.TO,
        'file': _file,
    })

    return response

REPORT_HANDLERS = {
    'vends': vends_reporter,
}

def create_report(host, service, date=None, _from=None, to=None):
    report = REPORT_HANDLERS[service]

    if date:
        file_name = report(date=date)
    else:
        file_name = report(_from=_from, to=to)

    if file_name:
        _file = '%s%s%s%s' % ('http://', host, settings.MEDIA_URL, file_name)
        return _file

def get_collection(collection_name):
    client = MongoClient()
    db = client.reports
    return db[collection_name]