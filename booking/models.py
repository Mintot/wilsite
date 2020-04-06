from django.db import models
from account.models import Client
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
PURPOSES = (
	('Studying', 'Studying'),
	('Project Making', 'Project Making'),
	('Group Collaboration', 'Group Collaboration'),
)
VENUES = (
	('Conference Room A', 'Conference Room A'),
	('Conference Room B', 'Conference Room B'),
	('Joined Conference Room', 'Joined Conference Room'),
	('Coworking Space', 'Coworking Space'),
)
STATUS = (
	('Booked', 'Booked'),
	('Cancelled', 'Cancelled'),
	('Completed', 'Completed'),
	('No Show', 'No Show'),
	('Late', 'Late'),
	('Overstayed', 'Overstayed'),
	('Cancelled by Admin', 'Cancelled by Admin'),
)
PAYMENT_METHOD = (
	('Coins', 'Coins'),
	('Points', 'Points'),
	('Coins and Points', 'Coins and Points'),
	('None', 'None'),
)

class Venue(models.Model):
	name = models.CharField(max_length=50)
	cap = models.IntegerField()
	has_computers = models.BooleanField(default=False)
	computers = models.IntegerField(default=0)
	cost = models.IntegerField(default=20)
	computer_fee = models.IntegerField(default=10)

class Booking(models.Model):
	title = models.CharField(max_length=100, blank=True)
	book_date = models.DateTimeField(default=datetime.today()) 
	startDate = models.DateField()
	endDate = models.DateField()
	startTime = models.TimeField()
	endTime = models.TimeField()
	purpose = models.CharField(max_length=30, choices=PURPOSES, default='Studying')
	attendee = models.CharField(max_length=30, default='none')
	referenceNo = models.IntegerField()
	computers = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	cost = models.IntegerField(blank=True)
	venue = models.CharField(max_length=30, choices=VENUES, default='Coworking Space')
	status = models.CharField(max_length=30, choices=STATUS, default='Booked')
	time_stay = models.IntegerField(default=0)
	booker = models.CharField(max_length=30, default='none')
	payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='Coins')

class Review(models.Model):
	submit_date = models.DateTimeField(default=datetime.today())
	stars = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
	comment = models.TextField()

class MaxDaysOfBooking(models.Model):
	max_days = models.IntegerField(default=3)