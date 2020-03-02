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
		allUsers = [b.attendee for b in bookings]
		allStarts = []
		allEnds = []
		i = 0;
		while i < len(bookings):
			# if (startDates[i] != endDates[i]):
			# 	curr = startDates[i]
			# 	finished = False
			# 	while !finished:
			# 		allStarts.append(str(curr) + ' ' + str(startTimes[i]))
			# 		allEnds.append(str(curr) + ' ' + str(endTimes[i]))
			# 		month = int(curr.substring(0, 2))
			# 		day = int(curr.substring(3, 5))
			# 		# if (day == 28)

			# else:
			allStarts.append(str(startDates[i]) + ' ' + str(startTimes[i]))
			allEnds.append(str(endDates[i]) + ' ' + str(endTimes[i]))
			i = i + 1
		if user.is_authenticated:
			return render(request = request, template_name = self.template_name, context={'user' : user, 'id': user.username, 'startDates' : allStarts, 'endDates': allEnds, 'venues': allVenues, 'users': allUsers, })
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
			print("valid")
			venue = form.real_venue()
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
		user = self.request.user
		form = self.form_class(None)
		users = list(Client.objects.all().exclude(first_name=""))
		str_users = []
		for u in users:
			str_users.append(str(u) + ' [' + u.username + ']')
		return render(request, self.template_name, context={'form': form, 'users':str_users, 'self': str(user)+' ['+user.username+']', })
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			print(request.POST.get('names'))
			attendees = request.POST.get('names')
			attendees_id = request.POST.get('ids')
			purpose = form.cleaned_data['purpose']
			request.session['purpose'] = purpose
			request.session['attendees'] = attendees
			request.session['attendees_id'] = attendees_id
		return redirect('booking:BookingInfo')

class BookingInfoView(View):
	form_class = BookingInfoForm
	template_name = 'booking/bookcal.html'
	def get(self, request):
		attendees_id = request.session.get('attendees_id')
		cost = request.session.get('totTime') * 20 * (len(attendees_id.split(", "))-1)
		request.session['cost'] = cost
		form = self.form_class(
			initial={
			'refNum': request.session.get('refNum'), 
			'cost': cost,
			'startDate': request.session.get('startDate'),
			'endDate': request.session.get('endDate'),
			'startTime': request.session.get('startTime'),
			'endTime': request.session.get('endTime'),
			'purpose': request.session.get('purpose'),
			'attendees': request.session.get('attendees'),
			'venue': request.session.get('venue'),
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
		attendees_id = request.session.get('attendees_id')
		for at_id in attendees_id.split(", "):
			if at_id.strip() != "":
				booking = Booking(referenceNo=refNum, cost=cost, venue=venue, startTime=startTime, endDate=endDate, startDate=startDate, endTime=endTime, purpose=purpose, attendee=at_id, )
				booking.save()
		print('SUCCESS')
		return redirect('home:Homepage')