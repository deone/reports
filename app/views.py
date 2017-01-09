from django.http import JsonResponse
from django.http import HttpResponseServerError
from django.utils import timezone

from utils import create_report, send_report

from datetime import timedelta
from collections import OrderedDict

def error_or_success_message(status_code, reason):
    if status_code != 200:
        return HttpResponseServerError(reason)
    else:
        return JsonResponse({'status': 'ok'})

def get_report(request, service, year=None, month=None, day=None, when=None):
    date = OrderedDict()

    if when:
        now = timezone.now()
        if when == 'today':
            date['day'] = now.day
            date['month'] = now.month
            date['year'] = now.year
        elif when == 'yesterday':
            report_date = now - timedelta(days=1)
            date['day'] = report_date.day
            date['month'] = report_date.month
            date['year'] = report_date.year

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

    _file = create_report(request.get_host(), service, date)
    if _file is not None:
        response = send_report(service, _file)
        return error_or_success_message(response.status_code, response.reason)
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid date'})

def get_report_by_date_range(request, service, _from=None, to=None, days=None):
    if days is not None:
        now = timezone.now()
        start = now - timedelta(days=int(days))
        _from = '%s-%s-%s' % (start.day, start.month, start.year)
        to = '%s-%s-%s' % (now.day, now.month, now.year)

    _file = create_report(request.get_host(), service, _from=_from, to=to)
    if _file is not None:
        response = send_report(service, _file)
        return error_or_success_message(response.status_code, response.reason)
    else:
        return JsonResponse({'status': 'error', 'message': 'invalid date'})