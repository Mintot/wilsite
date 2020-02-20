from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Booking

# Register your models here.
class BookingAdmin(admin.ModelAdmin):
	model = Booking
	list_display = ['startDate', 'endDate', 'startTime', 'endTime', ]

admin.site.register(Booking, BookingAdmin)