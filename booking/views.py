from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from .forms import *
from .models import Booking, Client
from random import randint
from django import forms
from django.http import JsonResponse
import datetime

# This view holds the calendar and caters to booking.
class BookingView(View):
	template_name = 'booking/bookingform.html'
	def get(self, request):
		user = self.request.user
		if user.is_authenticated == False:					# A user has to log in to access this view.
			return redirect('account:Index')
		bookings = Booking.objects.all()					# This gets all the bookings in the database to render to the classroom.
		startDates = [b.startDate for b in bookings]
		endDates = [b.endDate for b in bookings]
		startTimes = [b.startTime for b in bookings]
		endTimes = [b.endTime for b in bookings]
		allVenues = [b.venue for b in bookings]
		allUsers = [b.attendee for b in bookings]
		allStarts = []
		allEnds = []
		cowCap = Venue.objects.get(name="Coworking Space").cap  		#Initial calendar view's capacity
		i = 0;
		while i < len(bookings): 							# Stores all the date-time pairs to a separate array.
			allStarts.append(str(startDates[i]) + ' ' + str(startTimes[i]))
			allEnds.append(str(endDates[i]) + ' ' + str(endTimes[i]))
			i = i + 1
		return render(request = request, template_name = self.template_name, context={'user' : user, 'id': user.username, 'startDates' : allStarts, 'endDates': allEnds, 'venues': allVenues, 'users': allUsers, 'cowCap': cowCap, })

# This view is seen after the user has selected timeslots from the above view.
class BookingDetailsView(View):
	form_class = BookingDetailsForm
	template_name = 'booking/bookdet.html'
	def get(self, request):
		str_users = []
		user = self.request.user
		form = self.form_class(cap=request.session.get('space'), pcCap=request.session.get('comps'))
		venue = request.session.get('venue')
		print(venue)
		if Venue.objects.get(name=venue).has_computers == 0:  			# Hides the computer field
			form.fields['computers'].widget = forms.HiddenInput()
		users = list(Client.objects.all().exclude(first_name=""))
		for u in users:													# Puts all registered users in the possible list of co-bookee
			str_users.append(str(u) + ' [' + u.username + ']')
		return render(request, self.template_name, context={'form': form, 'users':str_users, 'self': str(user)+' ['+user.username+']', })
	def post(self, request):
		venue = request.session.get('venue')
		venCap = Venue.objects.get(name=venue).cap
		minCap = Venue.objects.get(name=venue).cap
		venComp = Venue.objects.get(name=venue).computers
		minComp = Venue.objects.get(name=venue).computers
		startDays = str(request.session.get('start_days')).split(', ')
		endDays = str(request.session.get('end_days')).split(', ')
		startTimes = str(request.session.get('start_times')).split(', ')
		endTimes = str(request.session.get('end_times')).split(', ')
		totTimes = 0
		i = 0
		last = (len(endTimes)-1)
		endTimes = endTimes[1:len(endTimes)-1]
		endDays = endDays[1:len(endDays)-1]
		startTimes = startTimes[1:len(startTimes)-1]
		startDays = startDays[1:len(startDays)-1]
		# The following statements are used to check avaliability of the facility and computers for every timeslot.
		while i < len(startDays):
			startDate = startDays[i][1:len(startDays[i])-1]
			endDate = endDays[i][1:len(endDays[i])-1]
			startTime = startTimes[i][1:len(startTimes[i])-1]
			endTime = endTimes[i][1:len(endTimes[i])-1]
			i = i + 1
			venBook = Booking.objects.filter(venue=venue)
			finConf = venBook.filter(startDate__exact=startDate).filter(startTime__exact=startTime)
			if len(finConf) > 0 and venue == 'Coworking Space': 
				timeslots = {}
				comps = {}
				for b in finConf:
					start = b.startDate
					end = b.endDate
					stTime = b.startTime
					enTime = b.endTime
					timesl = str(start) + " " + str(stTime)
					exist = timeslots.get(timesl)
					cpExist = comps.get(timesl)
					if exist == None:
						timeslots[timesl] = len(b.attendee.split(","))
						comps[timesl] = b.computers
					else:
						timeslots[timesl] = exist + len(b.attendee.split(","))
						comps[timesl] = cpExist + b.computers
				for timeslot in timeslots:
					if (minCap > venCap-timeslots[timeslot]):
						minCap = venCap-timeslots[timeslot]
					if (minComp > venComp-comps[timeslot]):
						minComp = venComp-comps[timeslot]
		request.session['space'] = minCap
		request.session['comps'] = minComp
		attendees = request.POST.get('names')
		attendees_id = request.POST.get('ids')
		form = self.form_class(request.POST, cap=request.session.get('space'), pcCap=request.session.get('comps'), atts=len(attendees.split(","))-1, )
		if form.is_valid():
			attendees = request.POST.get('names')
			attendees_id = request.POST.get('ids')
			purpose = form.cleaned_data['purpose']
			request.session['purpose'] = purpose
			request.session['attendees'] = attendees
			request.session['attendees_id'] = attendees_id
			computers = form.cleaned_data['computers']
			request.session['computers'] = computers
			return redirect('booking:BookingInfo')
		user = request.user
		str_users = []
		users = list(Client.objects.all().exclude(first_name=""))
		for u in users:
			str_users.append(str(u) + ' [' + u.username + ']')
		return render(request, self.template_name, context={'form': form, 'users':str_users, 'self': str(user)+' ['+user.username+']', })

# This view shows all the details for the user to see.
# This also contains a button that will finalize the booking.
class BookingInfoView(View):
	form_class = BookingInfoForm
	template_name = 'booking/bookcal.html'
	def get(self, request):
		attendees_id = request.session.get('attendees_id')
		print(request.session.get('totTime'))
		if request.session.get("venue") == "Coworking Space":
			cost = (request.session.get('totTime') * Venue.objects.get(name="Coworking Space").cost * (len(attendees_id.split(", "))-1)) + (request.session.get('totTime') * request.session.get('computers') * Venue.objects.get(name="Coworking Space").computer_fee)
		else:
			cost = request.session.get('totTime') * Venue.objects.get(name=request.session.get('venue')).cost
		request.session['cost'] = cost
		request.session['unit_cost'] = request.session.get('totTime') * Venue.objects.get(name=request.session.get('venue')).cost + (request.session.get('totTime') * request.session.get('computers') * Venue.objects.get(name="Coworking Space").computer_fee)
		form = self.form_class(
			initial={
			'refNum': request.session.get('refNum'), 
			'cost': cost,
			'startDate': str(request.session.get('start_days'))[1:len(str(request.session.get('start_days')))-1],
			'endDate': request.session.get('end_days'),
			'startTime': request.session.get('start_times'),
			'endTime': request.session.get('end_times'),
			'purpose': request.session.get('purpose'),
			'attendees': request.session.get('attendees'),
			'venue': request.session.get('venue'),
			})
		return render(request, self.template_name, context={'form': form})
	def post(self, request):
		user = self.request.user
		form = self.form_class(request.POST, balance=user.coins, cost=request.session.get('cost'), points=user.points, unit_cost=request.session.get('totTime') * Venue.objects.get(name=request.session.get('venue')).cost)
		if form.is_valid():
			payment_method = 'Points'
			unit_cost = request.session.get('unit_cost')
			credit = unit_cost - user.points
			if credit < 0:
				credit = 0
				user.points = user.points - unit_cost
			else:
				if user.points == 0:
					payment_method = 'Coins'
				else:
					payment_method = 'Coins and Points'
				user.points = 0
			user.coins = (user.coins - credit) - (request.session.get('cost') - unit_cost)
			user.save()
			venue = request.session.get('venue')
			startDate = str(request.session.get('start_days'))[1:len(str(request.session.get('start_days')))-1].split(", ")
			endDate = str(request.session.get('end_days'))[1:len(str(request.session.get('end_days')))-1].split(", ")
			startTime = str(request.session.get('start_times'))[1:len(str(request.session.get('start_times')))-1].split(", ")
			endTime = str(request.session.get('end_times'))[1:len(str(request.session.get('end_times')))-1].split(", ")
			cost = form.cleaned_data['cost']
			refNum = request.session.get('refNum')
			purpose = request.session.get('purpose')
			attendees_id = request.session.get('attendees_id')
			i = 0
			while i < len(startDate):
				start_day = startDate[i][1:len(startDate[i])-1]
				end_day = endDate[i][1:len(endDate[i])-1]
				start_time = startTime[i][1:len(startTime[i])-1]
				end_time = endTime[i][1:len(endTime[i])-1]
				i = i + 1
				for at_id in attendees_id.split(", "):
					if at_id.strip() != "":
						booking = Booking(referenceNo=refNum, cost=cost, venue=venue, startTime=start_time, endDate=end_day, startDate=start_day, endTime=end_time, purpose=purpose, attendee=at_id, booker=attendees_id.split(", ")[0], payment_method=payment_method, )
						booking.save()
			print('SUCCESS')
			return redirect('home:Homepage')
		attendees_id = request.session.get('attendees_id')
		cost = request.session.get('cost')
		form.initial={
			'refNum': request.session.get('refNum'), 
			'cost': cost,
			'startDate': request.session.get('start_days'),
			'endDate': request.session.get('end_days'),
			'startTime': request.session.get('start_times'),
			'endTime': request.session.get('end_times'),
			'purpose': request.session.get('purpose'),
			'attendees': request.session.get('attendees'),
			'venue': request.session.get('venue'),
			}
		return render(request, self.template_name, context={'form': form})

def review_book(request):
	venue = request.GET.get('venue', None)
	fr_day = request.GET.get('from', None)
	fr_to = request.GET.get('to', None)
	print(fr_day + " daysss")
	fr_day = str(fr_day).split(',')
	fr_to = str(fr_to).split(',')
	fr_time = "08:00"
	to_time = "08:00"
	i = 0
	all_day_f = []
	all_day_t = []
	all_time_f = []
	all_time_t = []
	print("Venue is  " + venue)
	while i < len(fr_day):
		print(i)
		fr_d = fr_day[i]
		fr_t = fr_to[i]
		print(fr_d + " day")
		print(fr_t + " to")
		fr_time = fr_d.split(" ")[1]
		fr_d = fr_d.split(" ")[0]
		to_time = fr_t.split(" ")[1]
		fr_t = fr_t.split(" ")[0]
		all_day_f.append(fr_d)
		all_day_t.append(fr_t)
		all_time_f.append(fr_time)
		all_time_t.append(to_time)
		i = i + 1

	request.session['start_days'] = all_day_f
	request.session['end_days'] = all_day_t
	request.session['start_times'] = all_time_f
	request.session['end_times'] = all_time_t
	request.session['venue'] = venue
	request.session['totTime'] = len(fr_day)/2

	refNum = randint(100000, 999999)
	allBookRef = [b.referenceNo for b in Booking.objects.all()]
	while refNum in allBookRef:
		refNum = randint(100000, 999999)
	request.session['refNum'] = refNum
	data = {
		'okay': True,
	}
	return JsonResponse(data)