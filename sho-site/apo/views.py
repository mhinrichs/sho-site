# views for apo

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from django.core.urlresolvers import reverse
from apo.models import WorkDay
import datetime as dt

def index(request):
    return render(request, 'apo/index.html')

def time(request):
    now = dt.datetime.today()
    context = {'now': now,}
    return render(request, 'apo/time.html', context)

def schedule(request, store_id , emp_id, year, month, day):
    datestring = year + " " + month + " " + day
    date = dt.datetime.strptime(datestring, "%Y %m %d") #converts date from url to datetime object
    workday = WorkDay.by_year(date).by_month(date).by_day(date)
    context = {'store_id': store_id,
               'emp_id': emp_id,
               'year': year,
               'month': month,
               'day': day,
               'test': workday}

    return render(request, 'apo/schedule.html', context)

def month_schedule(request, store_id , emp_id, year, month):
    datestring = year + " " + month
    date = dt.datetime.strptime(datestring, "%Y %m") #converts date from url to datetime object
    workday = WorkDay.by_year_month(date)
    context = {'store_id': store_id,
               'emp_id': emp_id,
               'year': year,
               'month': month,
               'test': workday}

    return render(request, 'apo/schedule.html', context)







