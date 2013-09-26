from django.db import models

class BaseProfile(models.Model):
    name = models.CharField(max_length=30)
    romaji = models.CharField(max_length=100)
    post_code = models.CharField(max_length=8)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=35)
    entry_date = models.DateTimeField()
    last_edited = models.DateTimeField(blank=True)
    valid_profile = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Store(BaseProfile):

    ''' A store location and information '''
    store_id = models.CharField(max_length=5)

class Person(BaseProfile):

    lastname = models.CharField(max_length=30, blank = False)

    class Meta:
        abstract = True

class Employee(Person):

    ''' An employee '''

    emp_id = models.CharField(max_length=5)
    birthday = models.DateField(blank=False)

class Customer(Person):

    ''' A customer '''

    birthday = models.DateField(blank=True)

class Schedule(models.Model):

    ''' Schedule template for working hours
        Blocks of time are linked to the schedule.
        Customers can in turn be connected to blocks
        whe they make an appointment. '''

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Block(models.Model):

    ''' A block of time for schedule. '''

    name = models.ForeignKey(Schedule)
    time_start = models.TimeField()
    time_finish = models.TimeField()
    is_booked = models.BooleanField(default = False)
    booked_by = models.ForeignKey(Customer, null=True, blank=True)

    def __str__(self):
        return str(time_start) + "-" + str(time_finish)

class WorkDay(models.Model):

    store = models.ForeignKey(Store)
    employee = models.ForeignKey(Employee)
    date = models.DateField()
    schedule = models.ForeignKey(Schedule)

    @classmethod
    def by_emp_id(self, emp_id):
        return WorkDay.objects.filter(employee__emp_id__iexact = emp_id)

    @classmethod
    def by_year_month(self, dateobject):
        return WorkDay.objects.filter(date__year = dateobject.year)\
               .filter(date__month = dateobject.month)

    @classmethod
    def by_year_month_day(self, dateobject):
        return WorkDay.objects.filter(date__year = dateobject.year)\
               .filter(date__month = dateobject.month)\
               .filter(date__day = dateobject.day)

    @classmethod
    def within_next_month(self):
        pass

    def to_string(self):
        return self.date.strftime("%Y %m %d")









