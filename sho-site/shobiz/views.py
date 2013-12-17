# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from shobiz.models import Store, Employee, Customer, Workday, TimeBlock
from shobiz.utils import WorkdayCalendar, AppointmentManager
from calendar import Calendar
from datetime import datetime

# Change after adding default Store and Employee to Database
USE_DEFAULT_STORE = False
USE_DEFAULT_EMPLOYEE = False
DEFAULT_STORE = '''Your Store.objects.get here.'''
DEFAULT_EMPLOYEE = '''Your Employee.objects.get here.'''

# WorkdayCalendar
WorkdayCalendar = WorkdayCalendar()

# Helper functions
def encode_datestr(datestring):
    ''' encodeds a datestr to a datetime object '''
    try:
        date = datetime.strptime(datestring, '%Y_%m_%d')
    except:
        raise ValueError("Must follow the format YYYY_M_D")
    return date

#views
def index(request):
    ''' The index page will start at store selection.
        This section can be skipped by adding the relevant
        default session data and moving on to a later step.'''
    context = {}
    request.session.flush()
    request.session['apt_manager'] = AppointmentManager()
    if USE_DEFAULT_STORE:
        pass
    elif request.method == 'GET':
        return render(request, 'shobiz/index.html', context)
    else:
        pass

def employee(request):
    ''' Select an employee from a list of employees based
        off of the store that was selected '''
    context = {}
    if USE_DEFAULT_EMPLOYEE:
        pass
    elif request.method == 'GET':
        return render(request, 'shobiz/employee.html', context)
    else: # request.method == 'POST':
        pass

def calendar(request):
    d = datetime.now()
    request.session['year'] = d.year
    request.session['month'] = d.month
    try: #Create context, if it fails flush the session and try again.
        context = WorkdayCalendar.get_calendar_context(request)
    except ValueError:
        request.session.flush()
        return redirect(index)
    return render(request, 'shobiz/calendar.html', context)

def calendar_ajax(request):
    try:
        WorkdayCalendar.navigate(request)
    except ValueError:
        request.session.flush()
        return redirect(index)
    context = WorkdayCalendar.get_calendar_context(request)
    return render(request, 'shobiz/calendar_template.html', context)

def schedule(request):
    try:
        if request.GET.has_key('date'):
            date = encode_datestr(request.GET['date'])
            request.session['date'] = date
        context = WorkdayCalendar.get_schedule_context(request)
    except ValueError:
        request.session.flush()
        return redirect(index)
    return render(request, 'shobiz/schedule.html', context)

