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
    def by_store_emp_date(self, store_id, emp_id, date):
        return Workday.objects.filter(store__store_id__iexact = store_id)\
               .filter(employee__emp_id__iexact = emp_id)\
               .filter(date = date)

    @classmethod
    def by_store_emp_year_month(self, store_id, emp_id, year, month):
        return Workday.objects.filter(store__store_id__iexact = store_id)\
                     .filter(employee__emp_id__iexact = emp_id)\
                     .filter(date__year = year)\
                     .filter(date__month = month)

    def to_string(self):
        return self.date.strftime("%Y %m %d")

    def get_status(self):
        return "todo_return_real_status"

class TimeBlock(models.Model):

    ''' A block of time for a Workday '''

    name = models.ForeignKey(Workday)
    time_start = models.TimeField()
    time_finish = models.TimeField()
    is_booked = models.BooleanField(default = False)
    booked_by = models.ForeignKey(Customer, null=True, blank=True)

    def __unicode__(self):
        return str(self.time_start) + "-" + str(self.time_finish)













