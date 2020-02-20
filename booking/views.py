from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from .forms import *
from .models import Booking

# Create your views here.
class BookingView(View):
	template_name = 'booking/bookingform.html'

	def get(self, request):
		user = self.request.user
		if user.is_authenticated:
			return render(request = request, template_name = self.template_name, context={'user' : user})
		return redirect('account:Index')

class BookingCalendarView(View):
	form_class = BookingCalendarForm
	template_name = 'booking/bookcal.html'
	def get(self, request):
		form = self.form_class(None)
		return render(request, template_name=self.template_name, context={'form' : form})
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			# request.session['startDate'] = form.cleaned_data['start_date']
			return redirect('booking:BookingDetails')
		return render(request=request, template_name=self.template_name, context={'form' : form})

class BookingDetailsView(View):
	form_class = BookingDetailsForm
	template_name = 'booking/bookcal.html'
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, context={'form': form})
	def post(self, request):
		form = self.form_class(request.POST)
		return redirect('booking:BookingInfo')

class BookingInfoView(View):
	form_class = BookingInfoForm
	template_name = 'booking/bookcal.html'
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, context={'form': form})
	def post(self, request):
		form = self.form_class(request.POST)
		return redirect('home:Homepage')