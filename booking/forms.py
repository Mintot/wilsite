from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.utils import timezone
from .models import *

class BookingCalendarForm(forms.ModelForm):
	today = str(timezone.now())[0:10]
	year = int(today[0:4])
	maxDay = str(year+1)+today[4:10]

	# widget=forms.PasswordInput(attrs={'class' : 'details', 'placeholder' : 'Password'}))

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
				'class' : 'sDate',
			},
		),
		initial=today,
	)
	end_date = forms.DateField(
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
				'class' : 'sDate',
			},
		),
		initial=today,
	)
	
	start_time = forms.TimeField(
		widget=TimePicker(
			options={
				'enabledHours': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
				'defaultDate': today,
				'stepping': 30,
			},
			attrs={
				'input_toggle': True,
				'input_group': True,
				'append': 'fa fa-calendar',
				'icon_toggle': True,
				'class' : 'sDate',
			},
		),
	)
	end_time = forms.TimeField(
		widget=TimePicker(
			options={
				'enabledHours': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
				'defaultDate': today,
				'stepping': 30,
			},
			attrs={
				'input_toggle': True,
				'input_group': True,
				'append': 'fa fa-calendar',
				'icon_toggle': True,
				'class' : 'sDate',
			}
		),
		initial='12:00:00'
	)
	def clean_end_date(self):
		startDate = self.cleaned_data.get('start_date')
		endDate = self.cleaned_data.get('end_date')
		if startDate > endDate:
			raise forms.ValidationError('Start date should be before end date')
		return endDate
	def clean_end_time(self):
		startTime = self.cleaned_data.get('start_time')
		endTime = self.cleaned_data.get('end_time')
		if startTime >= endTime:
			raise forms.ValidationError('Start time should be before end time')
		return endTime
	class Meta:
		model = Booking
		fields = ['venue', ]

class BookingDetailsForm(forms.ModelForm):
	# purpose = forms.CharField(max_length=30, choices = PURPOSES)
	class Meta:
		model = Booking
		fields = ['purpose']

class BookingInfoForm(forms.ModelForm):
	refNum = forms.CharField(disabled=True, label="Reference Number")
	startDate = forms.CharField(disabled=True, label="Start Date")
	endDate = forms.CharField(disabled=True, label="End Date")
	startTime = forms.CharField(disabled=True, label="Start Time")
	endTime = forms.CharField(disabled=True, label="End Time")
	cost = forms.IntegerField(disabled=True, label="Cost")
	class Meta:
		model = Booking
		fields = []