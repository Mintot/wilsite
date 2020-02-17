from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Client(AbstractUser):
	profile_picture = models.ImageField(upload_to='media/')
	verificationCode = models.CharField(max_length=10)

	def getEmail(self):
		return self.email