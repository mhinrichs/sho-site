# -*- coding: utf-8 -*-
# views.py for shobiz_staff

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, \
     DetailView, CreateView, UpdateView
from shobiz.models import Customer
from .forms import CustomerForm

def errorView(request, msg):
    template_name = 'staff/staff_menu_error.html'
    context = {'msg': msg}
    return render(request, template_name, context)

class StaffMenuView(TemplateView):
    template_name = 'staff/staff_menu.html'

class CustomerListView(ListView):
    template_name = 'staff/customer_list.html'
    model = Customer
    context_object_name = 'customers'

class CustomerDetailView(DetailView):
    template_name = 'staff/customer_detail.html'
    model = Customer
    context_object_name = 'customer'

class CustomerCreateView(CreateView):
    template_name = 'staff/customer_form.html'
    form_class = CustomerForm
    context_object_name = 'customer'

class CustomerUpdateView(UpdateView):
    template_name = 'staff/customer_form.html'
    model = Customer
    context_object_name = 'customer'

class CustomerDetailByPhone(TemplateView):
    template_name = 'staff/customer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailByPhone, self).get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(phone = kwargs['phone'])
        return context

    def post(self, request):
        try:
            if request.POST.has_key('phone'):
                pn = request.POST['phone']
                context = self.get_context_data(phone = pn)
        except (Customer.DoesNotExist, KeyError) as e:
            msg = 'The phone number you entered was not valid'
            return errorView(request, msg)
        return self.render_to_response(context)

class AppointmentForCustomerView(TemplateView):
    template_name = "staff/staff_booking.html"

    def get(self, request, **kwargs):
        pass
