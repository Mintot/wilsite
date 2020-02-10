from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Client

class IndexForm(forms.ModelForm):
	idNo = forms.CharField(label='Your ID Number', max_length=20, widget=forms.TextInput(attrs={'placeholder' : 'ID Number'}))
	class Meta:
		model = Client
		fields = ["idNo"]
	def clean_idNo(self):
		idNo = self.cleaned_data.get('idNo')
		try:
			Client.objects.get(username=idNo)
			return idNo
		except Client.DoesNotExist:
			raise forms.ValidationError('User ID does not exist.')


class RegForm(forms.ModelForm):
	firstName = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder' : 'First Name'})) 
	lastName = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder' : 'Last Name'})) 
	email = forms.CharField(label='Email Address', widget=forms.EmailInput(attrs={'placeholder' : 'Email Address'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder' : 'Enter Password'}), min_length=8)
	conf_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm Password'}), min_length=8)

	class Meta:
		model = Client
		fields = ["firstName", "lastName", "email", "password", "conf_password"]

	def clean_conf_password(self):
		password_confirm = self.cleaned_data.get('conf_password')
		password_submit = self.cleaned_data.get('password')
		if password_confirm != password_submit:
			raise forms.ValidationError('Password does not match.')
		return password_confirm			

	def clean_email(self):
		try:
			email = self.cleaned_data.get('email') # [Fixing Merge Conflicts] from cleaed_data
			validate_email(email)
			return email
		except ValidationError: # [Fixing Merge Conflicts] from validate_email.ValidationError
			raise forms.ValidationError('Use a Proper Email')

class SignInForm(forms.ModelForm):
	# idNo = forms.CharField(label='ID Number', widget=forms.TextInput(attrs={'placeholder' : 'ID Number'}))
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder' : 'Password'}))

	# def clean_password(self):
	# 	password = self.cleaned_data.get('password')
	# 	idNo = self.request.session['idNo']
	# 	user = Users.objects.get(username=idNo)
	# 	if user.password != password:
	# 		raise forms.ValidationError('Incorrect password')
	# 	return password

	class Meta:
		model = Client
		fields = ["password"] # these are the fields in the form 

class ForgetPasswordForm(forms.ModelForm):
	verificationCode = forms.CharField(label='Enter verification code', widget=forms.TextInput(attrs={'placeholder' : 'Enter verification code'}))

	class Meta:
		model = Client
		fields = ["verificationCode"]

class ChangePasswordForm(forms.ModelForm):
	password = forms.CharField(label='Enter New Password', widget=forms.PasswordInput(attrs={'placeholder' : 'Enter New Password'}))
	conf_password = forms.CharField(label='Reenter New Password', widget=forms.PasswordInput(attrs={'placeholder' : 'Reenter New Password'}))

	def clean_conf_password(self):
		password_confirm = self.cleaned_data.get('conf_password')
		password_submit = self.cleaned_data.get('password')
		if password_confirm != password_submit:
			raise forms.ValidationError('Password does not match.')
		if len(password_confirm) < 8:
			raise forms.ValidationError('Password should be at least 8 characters.')
		return password_confirm

	class Meta:
		model = Client
		fields = ["password", "conf_password"]