from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Client(AbstractUser):
	profile_picture = models.ImageField(upload_to='media/')
	verificationCode = models.CharField(max_length=10)
	coins = models.IntegerField(default=0)
	points = models.IntegerField(default=0)
	internet = models.IntegerField(default=0)
	facility_logs = models.TextField()
	in_facility = models.BooleanField(default=False)

	def getEmail(self):
		return self.email

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class TechnoTeam(models.Model):
	team_image = models.ImageField(upload_to='media/')
	project_name = models.CharField(max_length=20)
	group_name = models.CharField(max_length=40)
	contact_number = models.CharField(max_length=11)
	email = models.CharField(max_length=35)
	start_date = models.DateField()
	end_date = models.DateField()
	type_of_business = models.CharField(max_length=50)
	industry = models.CharField(max_length=30)
	business_system = models.CharField(max_length=50)
	instructor = models.CharField(max_length=30)
	mentors = models.CharField(max_length=50)
	mission = models.TextField()
	vision = models.TextField()
	tagline = models.TextField()
	members = models.TextField()
	internet = models.IntegerField(default=0)
	coins = models.IntegerField(default=0)
	points = models.IntegerField(default=0)

class StartUpTeam(models.Model):
	team_image = models.ImageField(upload_to='media/')
	startup_name = models.CharField(max_length=30)
	company_name = models.CharField(max_length=40)
	founders = models.TextField()
	main_address = models.CharField(max_length=500)
	parent_company = models.CharField(max_length=100)
	partner_company = models.CharField(max_length=350)
	contact_number = models.CharField(max_length=11)
	email = models.CharField(max_length=35)
	type_of_business = models.CharField(max_length=50)
	industry = models.CharField(max_length=30)
	business_system = models.CharField(max_length=50)
	operating_start = models.TimeField()
	operating_end = models.TimeField()
	accelerators = models.TextField()
	mission = models.TextField()
	vision = models.TextField()
	tagline = models.TextField()
	employee_list = models.TextField()
	internet = models.IntegerField(default=0)
	coins = models.IntegerField(default=0)
	points = models.IntegerField(default=0)

class Activity(models.Model):
	team = models.CharField(max_length=30)
	incubatee = models.CharField(max_length=20)
	title = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	facilitator = models.CharField(max_length=100)
	schedule = models.DateTimeField()
	venue = models.CharField(max_length=100)
	description = models.TextField()
	attendees = models.CharField(max_length=250)
	cost = models.IntegerField(default=0)
	payment_mode = models.CharField(max_length=30)

class Transaction(models.Model):
	team = models.CharField(max_length=30)
	date = models.DateField()
	debcre = models.CharField(max_length=6)
	category = models.CharField(max_length=100)
	bookact = models.CharField(max_length=100)
	description = models.TextField()
	payment_mode = models.CharField(max_length=30)

class Investment(models.Model):
	team = models.CharField(max_length=30)
	source = models.CharField(max_length=75)
	inv_type = models.CharField(max_length=30)
	amount = models.IntegerField()
	date_received = models.DateField()
	remark = models.TextField()

class Revenue(models.Model):
	team = models.CharField(max_length=30)
	amount = models.IntegerField()
	date_received = models.DateField()
	remark = models.TextField()

class Expense(models.Model):
	team = models.CharField(max_length=30)
	amount = models.IntegerField()
	date_transact = models.DateField()
	remark = models.TextField()