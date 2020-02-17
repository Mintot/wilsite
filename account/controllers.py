from .forms import *
from .models import Client
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login

class IndexController():
	def verifyId(idNo):
		try:
			Client.objects.get(username=idNo)
			return True
		except Client.DoesNotExist:
			return False

	def verifyIdNewUser(idNo):
		firstName = Client.objects.get(username=idNo).first_name
		if firstName == "":
			return True
		return False

class RegistrationController():
	def verifyEmail(email):
		try:
			validate_email(email)
			return True
		except ValidationError:
			return False

	def saveUserAndLogin(request, idNo, password, firstName, lastName, email):
		user = Client.objects.get(username=idNo)
		user.first_name = firstName
		user.last_name = lastName
		user.email = email
		user.set_password(password)
		user.save()
		user = authenticate(username=idNo, password=password)
		if user is not None:
			login(request, user)
			return True
		return False