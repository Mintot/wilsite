from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User

# Create your views here.
class HomeView(View):
	template_name = 'home/index.html'

	def get(self, request):
		user = self.request.user
		print(request.user.username + " @Home")
		if user.is_authenticated:
			return render(request = request, template_name = self.template_name, context={'user' : user})
		return redirect('account:Index')
