from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker
from django.utils import timezone
from datetime import datetime, timedelta, time
from .models import *

class BookingCalendarForm(forms.ModelForm):
	today = str(timezone.now())[0:10]
	year = int(today[0:4])
	maxDay = str(year+1)+today[4:8]+'28'
	start_date = forms.DateField(
		widget=DatePicker(
			options={
				'minDate': today,
				'maxDate': maxDay,
				'daysOfWeekDisabled': [0],
			},
			attrs={
				'input_toggle': True,
				'append': 'fa fa-calendar',
				'icon_toggle': True,
			},
		),
		initial=today,
	)
	end_date = forms.DateField(
		required = True,
		widget=DatePicker(
			options={
				'minDate': today,
				'maxDate': maxDay,
				'daysOfWeekDisabled': [0],
			},
			attrs={
				'input_toggle': True,
				'append': 'fa fa-calendar',
				'icon_toggle': True,
			},
		),
		initial=today,
	)
	
	start_time = forms.TimeField(
		required=True,
		widget=TimePicker(
			options={
				'enabledHours': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
				'defaultDate': today,
				'stepping': 30,
			},
			attrs={
				'input_toggle': True,
				'append': 'fa fa-calendar',
				'icon_toggle': True,
			},
		)
	)
	end_time = forms.TimeField(
		required=True,
		widget=TimePicker(
			options={
				'enabledHours': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
				'defaultDate': today,
				'stepping': 30,
			},
			attrs={
				'input_toggle': True,
				'append': 'fa fa-calendar',
				'icon_toggle': True,
			},
		)
	)
	def clean_end_date(self):
		startDate = self.cleaned_data.get('start_date')
		endDate = self.cleaned_data.get('end_date')
		if startDate > endDate:
			raise forms.ValidationError('Start date should be before end date')
		delta = endDate - startDate
		print(delta)
		if delta.days > 6:
			raise forms.ValidationError('You cannot book for a week or more.')
		return endDate
	def clean_end_time(self):
		venue = self.cleaned_data.get('venue')
		startDate = self.cleaned_data.get('start_date')
		endDate = self.cleaned_data.get('end_date')
		if endDate == None:
			raise forms.ValidationError('')
		startTime = self.cleaned_data.get('start_time')
		endTime = self.cleaned_data.get('end_time')
		print(endDate)
		for b in Booking.objects.all():
			ven = b.venue
			print(ven)
		venBook = Booking.objects.filter(venue=venue)
		if venue == "Conference Room A" or venue == "Conference Room B":
			venBook = venBook | Booking.objects.filter(venue="Joined Conference Room")
		elif venue == "Joined Conference Room":
			venBook = venBook | Booking.objects.filter(venue="Conference Room A") | Booking.objects.filter(venue="Conference Room B")
		print("All of " + str(venBook))
		bookingLeft = venBook.filter(startDate__lte=startDate)
		if len(bookingLeft) > 0:
			bookingLeft = bookingLeft.filter(endDate__gte=startDate)
		bookingRight= venBook.filter(endDate__gte=endDate)
		if len(bookingRight) > 0:
			bookingRight = bookingRight.filter(startDate__lte=endDate)
		bookingMid = venBook.filter(startDate__gte=startDate)
		if len(bookingMid) > 0:
			bookingMid = bookingMid.filter(endDate__lte=endDate)
		
		print(str(bookingLeft) + " and " + str(bookingRight) + " and " + str(bookingMid))
		conf = bookingRight | bookingLeft | bookingMid
		print(conf)
		confLeft = conf.filter(startTime__lte=startTime).filter(endTime__gte=startTime)
		confRight= conf.filter(endTime__gte=endTime).filter(startTime__lte=endTime)
		confMid= conf.filter(startTime__gte=startTime).filter(endTime__lte=endTime)
		finConf = confRight | confLeft | confMid
		print("CONFLICT FOUND ON: " + str(finConf))
		if len(finConf) > 0:
			if venue == 'Coworking Space':
				timeslots = {}
				for b in finConf:
					start = b.startDate
					end = b.endDate
					stop = False
					while stop == False:
						stTime = b.startTime
						enTime = b.endTime
						timesl = str(start) + " " + str(stTime)
						while stTime != enTime:
							exist = timeslots.get(timesl)
							if exist == None:
								timeslots[timesl] = len(b.attendee.split(", "))-1
							else:
								timeslots[timesl] = exist + len(b.attendee.split(", "))-1
							stTime = (datetime.combine(start, time(int(stTime.strftime('%H')), int(stTime.strftime('%M')))) + timedelta(minutes=30)).time()
						if str(start) == str(end):
							stop = True
						start = start + timedelta(days=1)
				for timeslot in timeslots:
					if timeslots[timeslot] >= 20:
						raise forms.ValidationError('The coworking space in ' + timeslot + ' is already full')
			else:
				confStartDate = finConf[0].startDate
				confEndDate = finConf[0].endDate
				confStartTime = finConf[0].startTime
				confEndTime = finConf[0].endTime
				raise forms.ValidationError('At least one conflict scheduled at '+str(confStartDate)+" to " + str(confEndDate) + " on " + str(confStartTime)+"-"+str(confEndTime))
		if startTime >= endTime:
			raise forms.ValidationError('Start time should be before end time')

		return endTime
	class Meta:
		model = Booking
		fields = ['venue', ]

class BookingDetailsForm(forms.ModelForm):
	# numpc = forms.IntegerField(label="Computers", initial=0)
	cap = -1
	pcCap = -1
	tot = -2
	def __init__(self, *args, **kwargs):
		if self.cap == -1:
			self.cap = kwargs.pop('cap', -1)
		if self.pcCap == -1:
			self.pcCap = kwargs.pop('pcCap', -1)
		self.tot = kwargs.pop('atts', -2)
		super().__init__(*args, **kwargs)
	def clean_computers(self):
		print('Cap ' + str(self.cap))
		print('Total ' + str(self.tot))
		print('PcCap ' + str(self.pcCap))
		computers = self.cleaned_data.get('computers')
		if computers > self.pcCap:
			raise forms.ValidationError(str(computers - self.pcCap) + ' computers are not available in certain times.')
		if self.tot > self.cap:
			raise forms.ValidationError('Only ' + str(self.cap) + ' can be catered during specific times')
		if self.tot < computers:
			raise forms.ValidationError('You cannot book more computers than the number of attendees.')
		if computers < 0 or computers > 8:
			raise forms.ValidationError("Computers should be between 0 and 8, inclusive.") 
		return computers
	class Meta:
		model = Booking
		fields = ['purpose', 'computers', ]

class BookingInfoForm(forms.ModelForm):
	balance = 0
	cost = 0
	def __init__(self, *args, **kwargs):
		self.balance = kwargs.pop('balance', 0)
		self.cost = kwargs.pop('cost', 1)
		super().__init__(*args, **kwargs)
	refNum = forms.CharField(disabled=True, label="Reference Number", required=False)
	venue = forms.CharField(disabled=True, label="Venue", required=False)
	startDate = forms.CharField(disabled=True, label="Start Date", required=False)
	endDate = forms.CharField(disabled=True, label="End Date", required=False)
	startTime = forms.CharField(disabled=True, label="Start Time", required=False)
	endTime = forms.CharField(disabled=True, label="End Time", required=False)
	purpose = forms.CharField(disabled=True, label="Purpose", required=False)
	attendees = forms.CharField(disabled=True, label="Attendees", required=False)
	cost = forms.IntegerField(disabled=True, label="Cost", required=False)
	def clean_cost(self):
		print(self.cost)
		# if self.balance < self.cost:
		# 	raise forms.ValidationError('You do not have enough balance. Your current balance is ' + str(self.balance) + '.')
		return self.cost
	class Meta:
		model = Booking
		fields = []