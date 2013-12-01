# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from shobiz.models import Store, Employee, Customer, Workday, TimeBlock
from shobiz.utils import WorkdayCalendarMaker
from calendar import Calendar
from datetime import datetime

#Default data for sessions that involve skipping sections:
DEFAULT_STORE = Store.objects.get(store_id = 's0001')
DEFAULT_EMPLOYEE = Employee.objects.get(emp_id = 'e000001')

#the calendar
WorkdayCalendar = WorkdayCalendarMaker()

#helper functions

def encode_datestr(datestring):
    ''' encodeds a datestr to a datetime object '''
    try:
        date = datetime.strptime(datestring, '%Y_%m_%d')
    except:
        raise ValueError("Must follow the format YYYY_M_D")
    return date

#views
def test(request): #displays current session variables for testing
    context = {}
    if request.session.has_key('store'):
        context['store'] = request.session['store']
    if request.session.has_key('employee'):
        context['employee'] = request.session['employee']
    if request.session.has_key('date'):
        context['date'] = request.session['date']
    request.session.flush()

    return render(request, 'shobiz/test.html', context)

def index(request): #DEFAULT_STORE is a constant so that it wont have to hit the database each time
    '''The index page will start at store selection.
       This section can be skipped by adding the relevant
       default session data and moving on to a later step.'''
    request.session.flush() #clear old session data
    skip_store = True
    skip_employee = True
    if skip_store and skip_employee: # if only 1 store and 1 employee
        request.session['store'] = DEFAULT_STORE
        request.session['employee'] = DEFAULT_EMPLOYEE
        return redirect(calendar)
    elif skip_store: #if only one store but multiple employees
        request.session['store'] = DEFAULT_STORE
        pass
    else: #todo select a store index view
        #each store in the list will be a post method that returns to the view to set the data
        return render(request, 'shobiz/index.html', {})

def employee(request):
    pass # wont need this till later

def calendar(request):
    d = datetime.now()
    request.session['year'] = d.year
    request.session['month'] = d.month
    try: #Create context, if it fails flush the session and try again.
        context = WorkdayCalendar.get_context_with_calendar(request)
    except ValueError:
        request.session.flush()
        return redirect(index)

    return render(request, 'shobiz/calendar.html', context)

def calendar_ajax(request):
    if request.GET['action']:
        print("hello from ajax action: {}".format(request.GET['action']))
    print(request.session['month'])
    request.session['month'] = request.session['month'] - 1
    context = WorkdayCalendar.get_context_with_calendar(request)
    return render(request, 'shobiz/calendar_template.html', context)

def schedule(request):
    context = {}
    needed_keys = ('store','employee','date')
    if all(request.session.has_key(key) for key in needed_keys):
        try: #change to fetch actual employee objects from the database
            store_id = request.session['store'].store_id
            emp_id = request.session['employee'].emp_id
            date = encode_datestr(request.session['date'])
            workday = Workday.by_store_emp_date(store_id, emp_id, date)
            context_dict['year'] = date.year
            context_dict['month'] = date.month
            context_dict['workday'] = workday
        except ValueError:
            # On error send them back index
            request.session.flush()
            return redirect(index)
    else:
        # On incomplete request send them back to the calendar
        return redirect(index)
    return render(request, 'shobiz/schedule.html', context_dict)

def time(request):
    now = datetime.today()
    context = {'now': now,
               'link': 'http://localhost:8000/shobiz/schedule/?store_id=s0001&emp_id=e000001&date=2014_11_26'}
    return render(request, 'shobiz/time.html', context)



