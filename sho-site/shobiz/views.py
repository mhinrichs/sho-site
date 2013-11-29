# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from django.core.urlresolvers import reverse
from shobiz.models import Store, Employee, Customer, Workday, TimeBlock
from shobiz.classes import WorkdayCalendarMaker
from calendar import Calendar
from datetime import datetime

#the calendar
workdaycal = WorkdayCalendarMaker()

#helper functions
def get_calendar(year, month): #change me
    url = 'shobiz/calendar/?year={0}&month={1}'.format(year, month)
    return HttpResponse(url)

def encode_datestr(datestring):
    ''' encodeds a datestr to a datetime object '''
    try:
        date = datetime.strptime(datestring, '%Y_%m_%d')
    except:
        raise ValueError()
    return date

#views
def index(request):
    return render(request, 'shobiz/index.html')

def schedule(request):
    context_dict = {}
    needed_keys = ('store_id','emp_id','date')
    if all(key in request.GET for key in needed_keys):
        try:
            store_id = request.GET['store_id']
            emp_id = request.GET['emp_id']
            date = encode_datestr(request.GET['date'])
            workday = Workday.by_store_emp_date(store_id, emp_id, date)
            context_dict['year'] = date.year
            context_dict['month'] = date.month
            context_dict['workday'] = workday
        except ValueError:
            return HttpResponse("schedule problem")
    else:
        #Just because I dont feel like typing the full info every time
        url = '?store_id=s0001&emp_id=e000001&date=2014_11_26'
        return HttpResponseRedirect(url)
    return render(request, 'shobiz/schedule.html', context_dict)

def calendar(request, store_id, emp_id, year, month):
    try:
        context_dict = {}
        year, month = int(year), int(month)
        context_dict['year'] = year
        context_dict['month'] = month
        context_dict['employee'] = Employee.objects.get(emp_id=emp_id)
        context_dict['days_of_week'] = workdaycal.get_weekdays()
        context_dict['calendar'] = workdaycal.get_calendar(store_id, emp_id, year, month)
    except:
        return HttpResponse("Dude, wtf bro!")
    return render(request, 'shobiz/calendar.html', context_dict)

def time(request):
    now = datetime.today()
    context = {'now': now,
               'link': 'http://localhost:8000/shobiz/schedule/?store_id=s0001&emp_id=e000001&date=2014_11_26'}
    return render(request, 'shobiz/time.html', context)

