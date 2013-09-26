from django.contrib import admin
from apo.models import Store, Employee, Customer, Schedule, Block, WorkDay
import datetime
from django.utils import timezone

class StoreAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Store Information', {'fields':['name', 'romaji', 'post_code', 'address1', 'address2', 'phone', 'email' ]}),
        ('Data Entry', {'fields': ['entry_date', 'last_edited', 'valid_profile'], 'classes': ['collapse']}),
        ]

admin.site.register(Store, StoreAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Profile', {'fields':['name', 'romaji', 'birthday', 'emp_id']}),
        ('Contact Information', {'fields': ['post_code', 'address1', 'address2', 'phone', 'email' ]}),
        ('Data Entry', {'fields': ['entry_date', 'last_edited', 'valid_profile'], 'classes': ['collapse']}),
        ]

admin.site.register(Employee, EmployeeAdmin)

class CustomerAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Profile', {'fields':['name', 'romaji', 'birthday']}),
        ('Contact Information', {'fields': ['post_code', 'address1', 'address2', 'phone', 'email' ]}),
        ('Data Entry', {'fields': ['entry_date', 'last_edited', 'valid_profile'], 'classes': ['collapse']}),
        ]

admin.site.register(Customer, CustomerAdmin)

class BlockInline(admin.TabularInline):
    model = Block
    extra = 1
    fields = ['time_start', 'time_finish']

class WorkScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Description', {'fields':['name']}),
        ]
    inlines = [BlockInline]

admin.site.register(Schedule, WorkScheduleAdmin)

class WorkDayAdmin(admin.ModelAdmin):

    def within_two_weeks(self):
        now = timezone.now()
        two_weeks = datetime.timedelta(days=14)
        return (self.date <= now + twoweeks) and (self.date >= now)

    def is_today(self):
        return self.date.day == datetime.datetime.today().day

    list_filter = ['date']

admin.site.register(WorkDay, WorkDayAdmin)
