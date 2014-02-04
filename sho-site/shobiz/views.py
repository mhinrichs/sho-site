# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from shobiz.models import Store, Employee, Customer, Workday, TimeBlock
from shobiz.utils import WorkdayCalendar, AppointmentManager
from shobiz.forms import ReservationForm
from shobiz.validators import valid_session_for_view
from calendar import Calendar
from datetime import datetime

# WorkdayCalendar
WorkdayCalendar = WorkdayCalendar()

# Change after adding default Store and Employee to Database
USE_DEFAULT_STORE = True
USE_DEFAULT_EMPLOYEE = True
DEFAULT_STORE = Store.objects.get(store_id = 's0001')
DEFAULT_EMPLOYEE = Employee.objects.get(emp_id = 'e000001')

def index(request):
    # perform initial setup
    context = {}
    request.session.flush()
    request.session['apt_manager'] = AppointmentManager()

    if request.method == 'POST':
        # do something
        pass
    else:
        if USE_DEFAULT_STORE:
            request.session['apt_manager'].store = DEFAULT_STORE
            request.session.modified = True
            return redirect(employee)
        else: #write a view for selecting store
            return render(request, 'shobiz/index.html', context)

def employee(request):
    # verify session info
    if not valid_session_for_view(request, 'employee'):
        return redirect(index)

    if request.method = 'POST':
        # do something
        pass
    else:
        if USE_DEFAULT_EMPLOYEE:
            request.session['apt_manager'].employee = DEFAULT_EMPLOYEE
            request.session.modified = True
            return redirect(calendar)
        else:
            return render(request, 'shobiz/employee.html', context)

def calendar(request):
    # verify session info
    if not valid_session_for_view(request, 'calendar'):
        return redirect(index)

    if request.method = 'POST':
        # do something
        pass
    else:
        d = datetime.now()
        request.session['apt_manager'].cal_year = d.year
        request.session['apt_manager'].cal_month = d.month
        request.session.modified = True
        context = WorkdayCalendar.get_calendar_context(request)
        return render(request, 'shobiz/calendar.html', context)

def calendar_ajax(request):
    try:
        WorkdayCalendar.navigate(request)
        request.session.modified = True
    except ValueError: #This only happens if someone trys to navigate past valid calandar values
        return redirect(index)
    context = WorkdayCalendar.get_calendar_context(request)
    return render(request, 'shobiz/calendar_template.html', context)

def schedule(request):
    if not valid_session_for_view(request, 'schedule'):
        return redirect(index)

    elif request.GET.has_key('date'):
        date = WorkdayCalendar.encode_datestr(request.GET['date'])
        request.session['apt_manager'].target_date = date
        request.session.modified = True
    else:
        pass
    context = WorkdayCalendar.get_schedule_context(request)
    return render(request, 'shobiz/schedule.html', context)


def make_appointment(request):
    if not valid_session_for_view(request, 'make_appointment'):
        return redirect(index)

    else:
        if request.method == 'POST':
            form = ReservationForm(request.POST)
            if form.is_valid():
                form.save(commit=True)
                return success(request)
            else:
                print(form.errors)
        else:
            form = ReservationForm()
    context = {'form': form}
    return render(request, 'shobiz/appointment.html', context)

def success(request):
    '''When customer confirms appointment sends confirmation mail to manager.'''
    pass
