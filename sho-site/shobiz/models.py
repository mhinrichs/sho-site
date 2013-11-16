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
    note = models.CharField(max_length = 150, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
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

class Workday(models.Model):

    store = models.ForeignKey(Store)
    employee = models.ForeignKey(Employee)
    date = models.DateField()

    def __unicode__(self):
        return self.to_string()

    @classmethod
    def by_emp_id(self, employee_id):
        return Workday.objects.filter(employee__emp_id__iexact = employee_id)

    @classmethod
    def by_year_month(self, dateobject):
        return Workday.objects.filter(date__year = dateobject.year)\
               .filter(date__month = dateobject.month)

    @classmethod
    def by_year_month_day(self, dateobject):
        return Workday.objects.filter(date__year = dateobject.year)\
               .filter(date__month = dateobject.month)\
               .filter(date__day = dateobject.day)

    @classmethod
    def within_next_month(self):
        pass

    def to_string(self):
        return self.date.strftime("%Y %m %d")


class TimeBlock(models.Model):

    ''' A block of time for a Workday '''

    name = models.ForeignKey(Workday)
    time_start = models.TimeField()
    time_finish = models.TimeField()
    is_booked = models.BooleanField(default = False)
    booked_by = models.ForeignKey(Customer, null=True, blank=True)

    def __unicode__(self):
        return str(self.time_start) + "-" + str(self.time_finish)





