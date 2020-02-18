from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User

# Create your views here.
class BookingView(View):
	template_name = 'booking/bookingform.html'

	def get(self, request):
		user = self.request.user
		if user.is_authenticated:
			return render(request = request, template_name = self.template_name, context={'user' : user})
		return redirect('account:Index')
