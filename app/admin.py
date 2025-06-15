from django.contrib import admin
from .models import Timetable, TimetableEntry, BookingRequest

admin.site.register(Timetable)
admin.site.register(TimetableEntry)
admin.site.register(BookingRequest)
