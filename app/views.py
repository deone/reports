from django.http import JsonResponse

from utils import create_and_send_report

def get_report(request, service, year=None, month=None, day=None):
    if year:
        year = int(year)
    if month:
        month = int(month)
    if day:
        day = int(day)

    # URL contains only year
    if month is None and day is None and year:
        if year > now.year:
            return JsonResponse({'code': 500, 'message': 'Invalid year.'})
        else:
            date = {'year': year}

    # URL contains year and month
    elif day is None and month and year:
        if year > now.year or month > now.month:
            return JsonResponse({'code': 500, 'message': 'Invalid year or month.'})
        else:
            date = {'year': year, 'month': month}

    # URL contains year, month and day
    elif year and month and day:
        date_supplied = datetime.date(year, month, day)
        if date_supplied > now.date():
            return JsonResponse({'code': 500, 'message': 'Invalid date.'})
        else:
            date = {'year': year, 'month': month, 'day': day}

    create_and_send_report(request, service, date)
    
    return JsonResponse({'status': 'ok'})

def get_report_by_date_range(request, service, _from, to):
    pass