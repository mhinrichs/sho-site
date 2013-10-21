import calendar
from shobiz.models import WorkDay

class Scheduler(calendar.Calendar):

    def __init__(self):
        # initialized with calendar set to appropriate starting weekday
        calendar.Calendar.__init__(self, 6)

    def prepare_calendar_for_template(self, year, month):



