from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from .forms import *
from .models import Booking, Client
from random import randint
import datetime

# Create your views here.
class BookingView(View):
	template_name = 'booking/bookingform.html'

	def get(self, request):
		user = self.request.user
		bookings = Booking.objects.all()
		startDates = [b.startDate for b in bookings]
		endDates = [b.endDate for b in bookings]
		startTimes = [b.startTime for b in bookings]
		endTimes = [b.endTime for b in bookings]
		allVenues = [b.venue for b in bookings]
		allStarts = []
		allEnds = []
		i = 0;
		while i < len(bookings):
			allStarts.append(str(startDates[i]) + ' ' + str(startTimes[i]))
			allEnds.append(str(endDates[i]) + ' ' + str(endTimes[i]))
			i = i + 1
		if user.is_authenticated:
			return render(request = request, template_name = self.template_name, context={'user' : user, 'startDates' : allStarts, 'endDates': allEnds, 'venues': allVenues, })
		return redirect('account:Index')

class BookingCalendarView(View):
	form_class = BookingCalendarForm
	template_name = 'booking/bookcal.html'
	def get(self, request):
		form = self.form_class(None)
		refNum = randint(100000, 999999)
		request.session['refNum'] = refNum
		return render(request, template_name=self.template_name, context={'form' : form})
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			venue = form.cleaned_data['venue']
			startDate = form.cleaned_data['start_date']
			endDate = form.cleaned_data['end_date']
			startTime = form.cleaned_data['start_time']
			endTime = form.cleaned_data['end_time']
			totTime = (int(endTime.strftime("%H"))-int(startTime.strftime("%H")))
			totMin = (int(endTime.strftime("%M"))-int(startTime.strftime("%M")))
			if totMin == -30:
				totTime -= 0.5
			elif totMin == 30:
				totTime += 0.5
			request.session['totTime'] = totTime
			request.session['venue'] = venue
			request.session['startDate'] = str(startDate)
			request.session['endDate'] = str(endDate)
			request.session['startTime'] = str(startTime)
			request.session['endTime'] = str(endTime)
			return redirect('booking:BookingDetails')
		return render(request=request, template_name=self.template_name, context={'form' : form})

class BookingDetailsView(View):
	form_class = BookingDetailsForm
	template_name = 'booking/bookdet.html'
	def get(self, request):
		form = self.form_class(None)
		users = list(Client.objects.all().exclude(first_name=""))
		str_users = []
		for u in users:
			str_users.append(str(u))
		return render(request, self.template_name, context={'form': form, 'users':str_users})
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			purpose = form.cleaned_data['purpose']
			request.session['purpose'] = purpose
		return redirect('booking:BookingInfo')

class BookingInfoView(View):
	form_class = BookingInfoForm
	template_name = 'booking/bookcal.html'
	def get(self, request):
		cost = request.session.get('totTime') * 20
		request.session['cost'] = cost
		form = self.form_class(
			initial={
			'refNum': request.session.get('refNum'), 
			'cost': cost,
			'startDate': request.session.get('startDate'),
			'endDate': request.session.get('endDate'),
			'startTime': request.session.get('startTime'),
			'endTime': request.session.get('endTime'),
			})
		return render(request, self.template_name, context={'form': form})
	def post(self, request):
		form = self.form_class(request.POST)
		venue = request.session.get('venue')
		startDate = request.session.get('startDate')
		endDate = request.session.get('endDate')
		startTime = request.session.get('startTime')
		endTime = request.session.get('endTime')
		cost = request.session.get('cost')
		refNum = request.session.get('refNum')
		purpose = request.session.get('purpose')
		attendee = self.request.user.username
		booking = Booking(referenceNo=refNum, cost=cost, venue=venue, startTime=startTime, endDate=endDate, startDate=startDate, endTime=endTime, purpose=purpose, attendee=attendee, )
		booking.save()
		print('SUCCESS')
		return redirect('home:Homepage')