# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from django.http import HttpResponse
from shobiz.models import Store, Employee, Customer, Workday, TimeBlock, Reservation
from shobiz.utils import WorkdayCalendar, AppointmentManager
from shobiz.forms import ReservationForm
from shobiz.validators import valid_session_for_view
from shobiz.defaults import DEFAULT_STORE, DEFAULT_EMPLOYEE
from calendar import Calendar
from datetime import datetime
import json

# Settings
WorkdayCalendar = WorkdayCalendar()
USE_DEFAULT_STORE = True
USE_DEFAULT_EMPLOYEE = True

# Views

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

    if request.method == 'POST':
        # do something
        pass
    else:
        if USE_DEFAULT_EMPLOYEE:
            request.session['apt_manager'].employee = DEFAULT_EMPLOYEE
            request.session.modified = True
            return redirect(calendar)
        else: #write a view for selecting employee
            return render(request, 'shobiz/employee.html', context)

def calendar(request):
    # verify session info
    if not valid_session_for_view(request, 'calendar'):
        return redirect(index)

    if request.method == 'POST':
        result = {}
        if request.POST.has_key('date'):
            date = WorkdayCalendar.encode_datestr(request.POST['date'])
            request.session['apt_manager'].target_date = date
            request.session.modified = True
            result['result'] = 'success'
        else:
            result['result'] = 'failure'
        return HttpResponse(json.dumps(result), content_type='application/json')
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
    if not valid_session_for_view(request, 'calendar'):
        return redirect(index)

    if request.method == 'POST':
        result = {}
        time = TimeBlock.objects.get(pk = request.POST['time'])
        #if the selected time block is not booked set as target_time
        if time.is_booked == False:
            request.session['apt_manager'].target_time = time
            request.session.modified = True
            result['result'] = 'success'
        else:
            result['result'] = 'failure'
        return HttpResponse(json.dumps(result), content_type='application/json')

    context = WorkdayCalendar.get_schedule_context(request)
    return render(request, 'shobiz/schedule.html', context)

def appointment(request):
    if not valid_session_for_view(request, 'appointment'):
        return redirect(calendar)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form = request.session['apt_manager'].process_form(request, form)
            request.session.modified = True
            if request.session['apt_manager'].complete_reservation:
                return redirect(success)
            else:
                return redirect(failure)
        else:
            print(form.errors)

    form = ReservationForm()
    context = {'form': form}
    return render(request, 'shobiz/appointment.html', context)

def success(request):
    appointment = request.session['apt_manager'].complete_reservation
    request.session['apt_manager'].send_confirmation_email(appointment)
    return HttpResponse("Check your E-mail!")

def failure(request):
    return HttpResponse("Something went wrong!")
