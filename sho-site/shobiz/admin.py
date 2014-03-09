from django.contrib import admin
from shobiz.models import Store, Employee, Customer, TimeBlock, Workday, SurveyItem, Reservation
from django.utils import timezone
import datetime

class StoreAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Store Information', {'fields':['name', 'romaji', 'store_id', 'post_code', 'address1', 'address2', 'phone', 'email' ]}),
        ('Data Entry', {'fields': ['created', 'modified', 'valid_profile'], 'classes': ['collapse']}),
        ]
    readonly_fields = ('created', 'modified')

admin.site.register(Store, StoreAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Profile', {'fields':['name', 'lastname', 'romaji', 'birthday', 'user', 'emp_id']}),
        ('Contact Information', {'fields': ['post_code', 'address1', 'address2', 'phone', 'email' ]}),
        ('Data Entry', {'fields': ['created', 'modified', 'valid_profile'], 'classes': ['collapse']}),
        ]
    readonly_fields = ('created', 'modified')

admin.site.register(Employee, EmployeeAdmin)

class CustomerAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Profile', {'fields':['name', 'lastname', 'romaji', 'birthday', 'user']}),
        ('Contact Information', {'fields': ['post_code', 'address1', 'address2', 'phone', 'email' ]}),
        ('Data Entry', {'fields': ['created', 'modified', 'valid_profile'], 'classes': ['collapse']}),
        ]
    readonly_fields = ('created', 'modified')

admin.site.register(Customer, CustomerAdmin)

class BlockInline(admin.TabularInline):
    model = TimeBlock
    extra = 1
    fields = ['time_start', 'time_finish', 'is_booked']

class WorkdayAdmin(admin.ModelAdmin):

    inlines = [BlockInline]

    def within_two_weeks(self):
        now = timezone.now()
        two_weeks = datetime.timedelta(days=14)
        return (self.date <= now + twoweeks) and (self.date >= now)

    def is_today(self):
        return self.date.day == datetime.datetime.today().day

    list_filter = ['date']

admin.site.register(Workday, WorkdayAdmin)
admin.site.register(Reservation)
admin.site.register(SurveyItem)






