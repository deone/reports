from django.http import JsonResponse
from django.http import HttpResponseServerError
from django.utils import timezone

from utils import create_report, send_report, order_date, order_stringify_date

from datetime import timedelta
from collections import OrderedDict

def error_or_success_message(status_code, reason):
    if status_code != 200:
        return HttpResponseServerError(reason)
    else:
        return JsonResponse({'status': 'ok'})

def get_report(request, service, year=None, month=None, day=None):
    date = OrderedDict()
    if year is not None:
        date['year'] = int(year)
    elif month is not None:
        parts = month.split('-')
        date['month'] = parts[0]
        date['year'] = parts[1]
    elif day is not None:
        parts = day.split('-')
        date['day'] = parts[0]
        date['month'] = parts[1]
        date['year'] = parts[2]

    print date

    _file = create_report(request.get_host(), service, date)
    response = send_report(service, _file)

    return error_or_success_message(response.status_code, response.reason)

""" def get_report_by_date_range(request, service, _from=None, to=None, days=None):
    print _from
    if days is not None:
        now = timezone.now()
        start = now - timedelta(days=int(days))
        _from = '%s-%s-%s' % (start.year, start.month, start.day)
        to = '%s-%s-%s' % (now.year, now.month, now.day)
    else:
        _from = order_stringify_date(_from)
        to = order_stringify_date(to)

    print _from
    _file = create_report(request.get_host(), service, _from=_from, to=to)
    response = send_report(service, _file)

    return error_or_success_message(response.status_code, response.reason) """