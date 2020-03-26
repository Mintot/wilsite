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

class Venue(models.Model):
	name = models.CharField(max_length=50)
	cap = models.IntegerField()
	has_computers = models.BooleanField(default=False)
	computers = models.IntegerField(default=0)
	cost = models.IntegerField(default=20)

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
	computers = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(8)])
	cost = models.IntegerField(blank=True)
	venue = models.CharField(max_length=30, choices=VENUES, default='Coworking Space')