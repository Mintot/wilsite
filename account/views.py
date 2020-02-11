from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from random import seed, randint
from django.core.mail import send_mail
import sendgrid
import os
# Create your views here.
from .forms import *
from .models import Client

class IndexView(View):
	form_class = IndexForm
	template_name = 'account/reg.html'
	def get(self, request):
		client = self.request.user
		if client.is_authenticated:
			return redirect('home:Homepage')
		form = self.form_class(None)
		return render(request=request, template_name=self.template_name, context={'form' : form})
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			idNo = form.cleaned_data['idNo']
			firstName = Client.objects.get(username=idNo).first_name
			request.session['idNo'] = idNo
			if firstName == "":
				return redirect('account:Register')
			return redirect('account:Signin')
		return render(request=request, template_name=self.template_name, context={'form' : form})

class RegView(View):
	form_class = RegForm
	template_name = 'account/reg_fin.html'

	def get(self, request):
		idNo = self.request.session.get('idNo')
		client = self.request.user
		if client.is_authenticated:
			return redirect('home:Homepage')
		if idNo == None:
			return redirect('account:Index')
		form = self.form_class(None)
		return render(request=request, template_name=self.template_name, context={'form': form, 'idNo' : idNo})
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			idNo = self.request.session['idNo']
			password = form.cleaned_data['password']
			conf_password = form.cleaned_data['conf_password']
			firstName = form.cleaned_data['firstName']
			lastName = form.cleaned_data['lastName']
			email = form.cleaned_data['email']
			# user.set_username(idNo)
			user = Client.objects.get(username=idNo)
			user.first_name = firstName
			user.last_name = lastName
			user.email = email
			user.set_password(conf_password)
			# user.set_first_name(firstName)
			# user.set_last_name(lastName)
			user.save()
			user = authenticate(username=idNo, password=conf_password)
			if user is not None:
				login(request, user)
				return redirect('home:Homepage')
		return render(request, self.template_name, {'form' : form})


class SigninView(View):
	form_class = SignInForm
	template_name = 'account/reg_fin.html'
	def get(self, request):
		idNo = request.session.get('idNo')
		if idNo == None:
			return redirect('account:Index')
		form = self.form_class(None)
		return render(request=request, template_name=self.template_name, context={'form': form, 'idNo' : idNo})
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			idNo = request.session['idNo']
			password = request.POST['password']
			user = authenticate(username=idNo, password=password)
			if user is not None:
				login(request, user)
				return redirect('home:Homepage')
		return render(request=request, template_name=self.template_name, context={'form' : form, 'idNo' : idNo,  'error_message' : 'Incorrect password.'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('account:Index')

class ForgetPasswordView(View):
	form_class = ForgetPasswordForm
	template_name = 'account/forget_pw.html'
	def get(self, request):
		idNo = request.session.get('idNo')
		if idNo == None:
			return redirect('account:Index')
		user = Client.objects.get(username=idNo)
		if user.first_name == "":
			return redirect('account:Register')
		user.verificationCode = randint(10000, 99999)
		user.save()
		res = send_mail('Reset Password', 'Here is your verification code: ' + str(user.verificationCode), 'wildcatslabs@yahoo.com', [user.email], fail_silently=False)
		print(res)
		#sg = sendgrid.SendGridAPIClient('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')
#		data = {
#		  "personalizations": [
#		    {
#		      "to": [
#		        {
#		          "email": user.email
#		        }
#		      ],
#		      "subject": 'Here is your verification code: ' + str(user.verificationCode)
#		    }
#		  ],
#		  "from": {
#		    "email": "wildcatslab@yahoo.com"
#		  },
#		  "content": [
#		    {
#		      "type": "text/plain",
#		      "value": "Reset Password"
#		    }
#		  ]
#		}
#		response = sg.client.mail.send.post(request_body=data)
		
#		print(response.status_code)
#		print(response.body)
#		print(response.headers)
		form = self.form_class(None)
		return render(request=request, template_name=self.template_name, context={'form' : form, 'idNo' : idNo})
		# return render(request=request, template_name=self.template_name, context={'form' : form, 'idNo' : idNo, 'error_message' : 'Sending email failed.'})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			idNo = request.session['idNo']
			verifCode = form.cleaned_data['verificationCode']
			request.session['verifCode'] = verifCode
			user = Client.objects.get(username=idNo)
			if user.verificationCode == verifCode:
				return redirect('account:ChangePassword')
		return render(request=request, template_name=self.template_name, context={'form' : form, 'idNo' : idNo,  'error_message' : 'Code does not match'})


class ChangePasswordView(View):
	form_class = ChangePasswordForm
	template_name = 'account/reg_fin.html'
	def get(self, request):
		idNo = request.session.get('idNo')
		if idNo == None:
			return redirect('account:Index')
		user = Client.objects.get(username=idNo)
		verifCode = request.session.get('verifCode')
		form = self.form_class(None)
		if user.verificationCode == verifCode:
			return render(request=request, template_name=self.template_name, context={'form' : form, 'idNo' : idNo})
		return redirect('account:ForgetPassword')

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			idNo = request.session.get('idNo')
			password = form.cleaned_data['password']
			conf_password = form.cleaned_data['conf_password']
			user = Client.objects.get(username=idNo)
			user.set_password(password)
			user.verificationCode = ""
			user.save()
			if user is not None:
				login(request, user)
				return redirect('home:Homepage')
		return render(request, self.template_name, {'form' : form})
