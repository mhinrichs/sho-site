from django.db import models

class Billable(models.Model):
    name = models.CharField(max_length = 30)
    item_id = models.CharField(max_length = 11, null=True, blank=True)
    price = models.IntegerField() # value in yen (whole numbers only)
    note = models.CharField(max_length = 100)
    class Meta:
        abstract = True

class Service(Billable):
    pass
class Product(Billable):
    pass

class ServiceTransaction(models.Model):
    item = models.ForeignKey(Service)
    quantity = models.IntegerField()
class ProductTransaction(models.Model):
    item = models.ForeignKey(Product)
    quantity = models.IntegerField()

class CheckoutRecord(models.Model):
    """ When booking an appointment an unregistered customer can pass
    desired services in the form of a survey which will be
    referenced by the TimeBlock when an Employee checks their
    email """
    customer = models.ForeignKey(Customer, null = True)
    employee = models.ForeignKey(Employee)
    datetime = models.DateTimeField(auto_now=True)
