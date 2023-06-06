from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from calendar import month_name, monthcalendar, setfirstweekday, SUNDAY
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from json import dumps, loads

from .models import Event

def view_calendar(request):
    setfirstweekday(SUNDAY)
    calendar_data = {}

    if request.method == 'POST':
        response = dumps(request.POST)
        data = loads(response)

        curr_month = datetime.strptime(data['month'], '%B %Y')
        calendar_data['curr_month_name'] = month_name[curr_month.month]
        calendar_data['curr_month_year'] = curr_month.year
        calendar_data['curr_month_calendar'] = monthcalendar(curr_month.year, curr_month.month)

        prev_month = curr_month.replace(day=1) - timedelta(days=1)
        calendar_data['prev_month_name'] = month_name[prev_month.month]
        calendar_data['prev_month_year'] = prev_month.year

        next_month = curr_month.replace(day=max(monthcalendar(curr_month.year, curr_month.month)[-1])) + timedelta(days=1)
        calendar_data['next_month_name'] = month_name[next_month.month]
        calendar_data['next_month_year'] = next_month.year

        this_month = date.today().replace(day=1)
        viewing_month = curr_month.date()
        if viewing_month <= this_month + relativedelta(months=-1):
            prev_limit = True
            next_limit = False
        elif viewing_month >= this_month + relativedelta(months=+1):
            prev_limit = False
            next_limit = True
        else:
            prev_limit = False
            next_limit = False
        calendar_data['prev_limit'] = prev_limit
        calendar_data['next_limit'] = next_limit

        calendar_data['day_of_week'] = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        events = Event.objects.filter(date__range=(curr_month.replace(day=1), curr_month.replace(day=max(monthcalendar(curr_month.year, curr_month.month)[-1]))))
        calendar_data.update({'events': loads(serializers.serialize('json', events))})

        return HttpResponse(dumps(calendar_data), content_type='application/json')
    else:
        curr_month = date.today()
        calendar_data['curr_month_name'] = month_name[curr_month.month]
        calendar_data['curr_month_year'] = curr_month.year
        calendar_data['curr_month_calendar'] = monthcalendar(curr_month.year, curr_month.month)
        prev_month = curr_month.replace(day=1) - timedelta(days=1)
        calendar_data['prev_month_name'] = month_name[prev_month.month]
        calendar_data['prev_month_year'] = prev_month.year
        next_month = curr_month.replace(day=max(monthcalendar(curr_month.year, curr_month.month)[-1])) + timedelta(days=1)
        calendar_data['next_month_name'] = month_name[next_month.month]
        calendar_data['next_month_year'] = next_month.year

        events = Event.objects.filter(date__range=(curr_month.replace(day=1), curr_month.replace(day=max(monthcalendar(curr_month.year, curr_month.month)[-1]))))
        calendar_data.update({'events': list(events.values())})

        return render(request, 'calendar_app/calendar.html', calendar_data)

def view_event(request, event_id):
    events = Event.objects.filter(id=event_id)
    return render(request, 'calendar_app/event.html', {'events': events})