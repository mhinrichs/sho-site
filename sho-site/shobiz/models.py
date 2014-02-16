# -*- coding: utf-8 -*-

from django.db import models
import shobiz.validators as validate

class BaseProfile(models.Model):
    name = models.CharField(max_length=30)
    romaji = models.CharField(max_length=100)
    post_code = models.CharField(max_length=8, blank = True)
    address1 = models.CharField(max_length=100, blank = True)
    address2 = models.CharField(max_length=100, blank = True)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=35)
    entry_date = models.DateTimeField()
    last_edited = models.DateTimeField(blank=True)
    valid_profile = models.BooleanField(default=True)
    note = models.CharField(max_length = 150, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self): #all inherited objects display their name
        return self.name

class Person(BaseProfile):

    lastname = models.CharField(max_length=30, blank = False)

    class Meta:
        abstract = True

class Store(BaseProfile):

    ''' A store location and information '''

    store_id = models.CharField(max_length=5, unique=True, validators=[validate.valid_store_id])

class Employee(Person):

    ''' Employee represents an employee record.
        An employee may be contracted to work at many
        different stores but his calendar lookups will
        return only his workdays / timeblocks for the
        store that the customer specifies.'''

    # fields
    emp_id = models.CharField(max_length=7, unique=True, validators=[validate.valid_emp_id])
    birthday = models.DateField(blank=False)

class Customer(Person):

    ''' A customer '''

    birthday = models.DateField(blank=True)

class Workday(models.Model):

    employee = models.ForeignKey(Employee)
    store = models.ForeignKey(Store)
    date = models.DateField()

    def __unicode__(self):
        return self.to_string()

    @classmethod
    def by_store_emp_date(self, store, employee, date):
        ''' Returns the first object in the queryset
            that matches all params or None. '''
        try:
            workday = Workday.objects.filter(store = store)\
                                     .filter(employee = employee)\
                                     .filter(date = date)[0]
        except IndexError:
            return None
        return workday

    @classmethod
    def by_store_emp_year_month(self, store, employee, year, month):
        ''' Returns a queryset that contains all workdays
            for a given month.  Used by Calendar class to build
            a Workday Calendar.  Prefetches timeblock data for use
            in building a schedule. '''
        return Workday.objects.filter(store = store)\
                              .filter(employee = employee)\
                              .filter(date__year = year)\
                              .filter(date__month = month)

    def to_string(self):
        return self.date.strftime("%Y_%m_%d")

    def get_status(self): #consider moving this
        ''' Returns busy status of a workday '''
        blocks = self.timeblock_set.all()
        total = len(blocks)
        count = float(0)
        for block in blocks:
            if block.is_booked:
                count += 1
        if count == 0 or count/total >= .5:
            return "green clickable"
        elif count/total >= .2:
            return "yellow clickable"
        elif count/total > 0:
            return "orange clickable"
        else:
            return "red"

class TimeBlock(models.Model):

    ''' A block of time for a Workday
        A customer can book a reservation
        within a block of time. '''

    workdate = models.ForeignKey(Workday)
    time_start = models.TimeField()
    time_finish = models.TimeField()
    is_booked = models.BooleanField(default = False)

    def __unicode__(self):
        return "{0}: {1}-{2}".format(self.workdate.to_string(),
                                     str(self.time_start),
                                     str(self.time_finish))

class SurveyItem(models.Model):

    ''' A service provided, used for booking an
        exit survey upon completion of a customer
        reservation

        Each instance should be worded as something
        the customer is iterested in doing during their
        appointment '''

    item = models.CharField(max_length = 50)

    def __unicode__(self):
        return str(self.item)

class Reservation(models.Model):

    ''' A reservation booked on a TimeBlock
        If the customer books from a logged in state
        the view will assign values to name and phone
        from their customer model. '''

    timeblock = models.OneToOneField(TimeBlock)
    customer = models.ForeignKey(Customer, null=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    services = models.ManyToManyField(SurveyItem, null=True)
    customer_comment = models.CharField(max_length=255)

    def __unicode__(self):
        return "{0} reservation @ {1}".format(self.name, self.timeblock.__unicode__())

