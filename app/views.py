from django.http import JsonResponse
from django.utils import timezone

from utils import create_and_send_report, order_date, order_stringify_date

def get_report(request, service, year=None, month=None, day=None):
    date = order_date(year=year, month=month, day=day)
    create_and_send_report(request, service, date)
    return JsonResponse({'status': 'ok'})

def get_report_by_date_range(request, service, _from, to):
    create_and_send_report(request, service, _from=order_stringify_date(_from), to=order_stringify_date(to))
    return JsonResponse({'status': 'ok'})