from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Client(AbstractUser):
	profile_picture = models.ImageField(upload_to='media/')
	verificationCode = models.CharField(max_length=10)
	balance = models.IntegerField(default=0)
	points = models.IntegerField(default=0)

	def getEmail(self):
		return self.email

	def __str__(self):
		return self.first_name + ' ' + self.last_name