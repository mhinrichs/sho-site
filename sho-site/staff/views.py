# -*- coding: utf-8 -*-
# views.py for staff

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from shobiz.models import Customer

class StaffMenuView(TemplateView):
    template_name = 'shobiz/staff_menu.html'

class CustomerListView(ListView):
    #template_name = 'shobiz/customer_list.html'
    model = Customer
    context_object_name = 'customers'

    def post(self, request):
        if request.POST.has_key('phone'):
            context = {}
            p = request.POST['phone']
            c = Customer.objects.get(phone=p)
            context['customer'] = c
            return CustomerDetailView.as_view()

class CustomerDetailView(DetailView):
    #template_name = 'shobiz/customer_detail.html'
    model = Customer
    context_object_name = 'customer'

class CustomerCreateView(CreateView):
    #template_name = 'shobiz/customer_form.html'
    model = Customer
    context_object_name = 'customer'

class CustomerUpdateView(UpdateView):
    #template_name = 'shobiz/customer_form.html'
    model = Customer
    context_object_name = 'customer'

class BookForCustomerView(TemplateView):
    template_name = "shobiz/staff_booking.html"

