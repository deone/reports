from django.http import JsonResponse
from django.http import HttpResponseServerError
from django.utils import timezone

from utils import create_report, send_report, order_date, order_stringify_date

def error_or_success_message(status_code, reason):
    if status_code != 200:
        return HttpResponseServerError(reason)
    else:
        return JsonResponse({'status': 'ok'})

def get_report(request, service, year=None, month=None, day=None):
    date = order_date(year=year, month=month, day=day)

    _file = create_report(request.get_host(), service, date)
    response = send_report(_file)

    return error_or_success_message(response.status_code, response.reason)

def get_report_by_date_range(request, service, _from, to):
    _file = create_report(request.get_host(), service, _from=order_stringify_date(_from), to=order_stringify_date(to))
    response = send_report(_file)

    return error_or_success_message(response.status_code, response.reason)