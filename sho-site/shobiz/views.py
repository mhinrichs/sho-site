# views for apo
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from django.core.urlresolvers import reverse
from shobiz.models import Workday
from calendar import Calendar
from datetime import datetime


#Setup the Locale Calendar


def get_calendar(year, month):
    cal = Calendar(6)
    return cal.monthdatescalendar(year, month)

def index(request):
    return render(request, 'shobiz/index.html')

def calendar(request):
    context_dict = {}
    context_dict['days_of_week'] = [r"日", r"月", r"火", r"水", r"木", r"金", r"土"]
    if request.method == 'GET':
        if request.GET.has_key('month'):
            d = datetime.now()
            month = int(request.GET['month'])
            context_dict['calendar'] = get_calendar(d.year, month)
            context_dict['month'] = month
            context_dict['year'] = d.year
    else:
        d = datetime.now()
        context_dict['calendar'] = get_calendar(d.year, d.month)
        context_dict['month'] = d.month
        context_dict['year'] = d.year
    return render(request, 'shobiz/calendar_template.html', context_dict)


    context_dict['calendar'] = get_calendar
    return render(request, 'shobiz/calendar.html')

def time(request):
    now = dt.datetime.today()
    context = {'now': now,}
    return render(request, 'shobiz/time.html', context)

'''
def schedule(request, store_id , emp_id, year, month, day):
    datestring = year + " " + month + " " + day
    date = dt.datetime.strptime(datestring, "%Y %m %d") #converts date from url to datetime object
    workdays = Workday.by_year(date).by_month(date).by_day(date)
    context = {'store_id': store_id,
               'emp_id': emp_id,
               'year': year,
               'month': month,
               'day': day,
               'test': workdays}

    return render(request, 'apo/schedule.html', context)

'''

'''
def month_schedule(request, store_id , emp_id, year, month):
    datestring = year + " " + month
    date = dt.datetime.strptime(datestring, "%Y %m") #converts date from url to datetime object
    workdays = Workday.by_year_month(date)
    context = {'store_id': store_id,
               'emp_id': emp_id,
               'year': year,
               'month': month,
               'test': workdays}

    return render(request, 'apo/schedule.html', context)

'''

def month_schedule(request, store_id, emp_id, year, month):
    theyear = int(year)
    themonth = int(month)
    context = {'store_id': store_id,
               'emp_id': emp_id,
               'calendar': cal.formatmonth(theyear, themonth)}

    return render(request, 'shobiz/schedule.html', context)







