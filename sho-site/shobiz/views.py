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

#views
def index(request):
    return render(request, 'shobiz/index.html')

# Just for testing real view is belows
def calendar(request):
    now = datetime.now()
    year, month = now.year, now.month
    context_dict = {}
    context_dict['year'] = year
    context_dict['month'] = month
    context_dict['days_of_week'] = workdaycal.get_weekdays()

    if all(key in request.GET for key in ('store_id','emp_id','year','month')):
        store_id = request.GET['store_id']
        emp_id = request.GET['emp_id']
        year = int(request.GET['year'])
        month = int(request.GET['month'])
        context_dict['year'] = year
        context_dict['month'] = month
        context_dict['calendar'] = workdaycal.get_calendar(store_id, emp_id, year, month)
    else:
        store_id = "s01" #default store and employee
        emp_id = "e01" #will be replaced later if employee > 1
        context_dict['calendar'] = workdaycal.get_calendar(store_id, emp_id, year, month)
    return render(request, 'shobiz/calendar_template.html', context_dict)

def schedule(request, store_id, emp_id, year, month):
    context_dict = {}
    year, month = int(year), int(month)
    context_dict['year'] = year
    context_dict['month'] = month
    #context_dict['employee'] = Employee.get_employee_method_here()
    context_dict['days_of_week'] = workdaycal.get_weekdays()
    context_dict['calendar'] = workdaycal.get_calendar(store_id, emp_id, year, month)
    return render(request, 'shobiz/schedule.html', context_dict)

def time(request):
    now = dt.datetime.today()
    context = {'now': now,}
    return render(request, 'shobiz/time.html', context)



