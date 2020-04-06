from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class ClientAdmin(UserAdmin):
	model = Client
	# add_form = RegForm
	# form = SignInForm
	list_display = ['username', 'first_name', 'last_name', 'email', 'points', 'coins', ]

class TechTeamAdmin(admin.ModelAdmin):
	model = TechnoTeam
	list_display = ['project_name', 'group_name', 'contact_number', 'email', 'start_date', ]

admin.site.register(Client, ClientAdmin)
admin.site.register(TechnoTeam, TechTeamAdmin)