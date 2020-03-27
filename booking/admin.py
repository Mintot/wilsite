from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class BookingAdmin(admin.ModelAdmin):
	model = Booking
	list_display = ['startDate', 'endDate', 'startTime', 'endTime', 'book_date']
class VenueAdmin(admin.ModelAdmin):
	model = Venue
	list_display = ['name', 'cap', ]
class ReviewAdmin(admin.ModelAdmin):
	model = Review
	list_display = ['submit_date', 'stars', ]

admin.site.register(Booking, BookingAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Review, ReviewAdmin)