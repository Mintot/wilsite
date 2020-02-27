from django.db import models
from account.models import Client
PURPOSES = (
	('studying', 'Studying'),
	('project making', 'Project Making'),
	('group collaboration', 'Group Collaboration'),
)
VENUES = (
	('conf', 'Conference Room'),
	('conf2', 'Joined Conference Room'),
	('coworking', 'Coworking Space'),
)

class Venue(models.Model):
	name = models.CharField(max_length=50)
	cap = models.IntegerField()
	isSimultaneous = models.BooleanField(default=False)

class Booking(models.Model):
	title = models.CharField(max_length=100)
	startDate = models.DateField()
	endDate = models.DateField()
	startTime = models.TimeField()
	endTime = models.TimeField()
	purpose = models.CharField(max_length=30, choices=PURPOSES, default='studying')
	attendee = models.CharField(max_length=30, default='none')
	referenceNo = models.IntegerField()
	cost = models.IntegerField()
	venue = models.CharField(max_length=30, choices=VENUES, default='coworking')