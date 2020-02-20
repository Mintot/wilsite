from django.db import models
from account.models import Client
PURPOSES = (
	('studying', 'Studying'),
	('project making', 'Project Making'),
	('group collaboration', 'Group Collaboration'),
)

class Booking(models.Model):
	title = models.CharField(max_length=100)
	startDate = models.DateField()
	endDate = models.DateField()
	startTime = models.TimeField()
	endTime = models.TimeField()
	purpose = models.CharField(max_length=30, choices=PURPOSES, default='studying')
	attendee = Client
	referenceNo = models.IntegerField()
