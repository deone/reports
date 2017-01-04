from django.http import JsonResponse
from django.utils import timezone

from utils import create_and_send_report, validate_date

def get_report(request, service, year=None, month=None, day=None):
    date = validate_date(year=year, month=month, day=day)
    create_and_send_report(request, service, date)
    return JsonResponse({'status': 'ok'})

def get_report_by_date_range(request, service, _from, to):
    # _from = validate_date(_from)
    # to = validate_date(to)

    create_and_send_report(request, service, _from=_from, to=to)
    return JsonResponse({'status': 'ok'})