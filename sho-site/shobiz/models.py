from django.db import models
import shobiz.validators as validate

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

    # object filters
    @classmethod
    def by_store_id_emp_id(self, store_id, emp_id):
        return Employee.objects.filter(emp_id = emp_id)

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
        return self.date.strftime("%Y_%m_%d")

    def get_status(self):
        blocks = self.timeblock_set.all()
        total = len(blocks)
        count = float(0)
        for block in blocks:
            if block.is_booked:
                count += 1
        if count == 0 or count/total >= .5:
            return "green"
        elif count/total >= .2:
            return "yellow"
        elif count/total > 0:
            return "orange"
        else:
            return "red"

class TimeBlock(models.Model):

    ''' A block of time for a Workday '''

    name = models.ForeignKey(Workday)
    time_start = models.TimeField()
    time_finish = models.TimeField()
    is_booked = models.BooleanField(default = False)
    booked_by = models.ForeignKey(Customer, null=True, blank=True)

    def __unicode__(self):
        return str(self.time_start) + "-" + str(self.time_finish)



