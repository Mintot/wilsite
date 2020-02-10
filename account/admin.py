from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Client
from .forms import RegForm
from .forms import SignInForm
# Register your models here.

class ClientAdmin(UserAdmin):
	model = Client
	# add_form = RegForm
	# form = SignInForm
	list_display = ['username', 'first_name', 'last_name', 'email', ]

admin.site.register(Client, ClientAdmin)