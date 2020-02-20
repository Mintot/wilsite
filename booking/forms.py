from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.utils import timezone
from .models import Booking


PURPOSES = (
	('studying', 'Studying'),
	('project making', 'Project Making'),
	('group collaboration', 'Group Collaboration'),
)

class BookingCalendarForm(forms.Form):
	today = str(timezone.now())[0:10]
	year = int(today[0:4])
	maxDay = str(year+1)+today[4:10]

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
		required=True,
		widget=DatePicker(
			options={
				'minDate': today,
				'maxDate': maxDay,
				'daysOfWeekDisabled': [0],
			},
			attrs={
				'append': 'fa fa-calendar',
				'icon_toggle': True,
			},
		),
		initial=today,
	)
	"""
	In this example, the date portion of `defaultDate` is irrelevant;
	only the time portion is used. The reason for this is that it has
	to be passed in a valid MomentJS format. This will default the time
	to be 14:56:00 (or 2:56pm).
	"""
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
			}
		),
		initial='12:00:00'
	)

class BookingDetailsForm(forms.ModelForm):
	# purpose = forms.CharField(max_length=30, choices = PURPOSES)
	class Meta:
		model = Booking
		fields = ['purpose']

class BookingInfoForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ['referenceNo']