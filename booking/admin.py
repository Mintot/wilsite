from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class BookingAdmin(admin.ModelAdmin):
	model = Booking
	list_display = ['startDate', 'endDate', 'startTime', 'endTime', ]
class VenueAdmin(admin.ModelAdmin):
	model = Venue
	list_display = ['name', 'cap', 'isSimultaneous', ]

admin.site.register(Booking, BookingAdmin)
admin.site.register(Venue, VenueAdmin)