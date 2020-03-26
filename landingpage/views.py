from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def landingpage(request):
	print(request.user.username + " @LandingPage")
	return render(request, 'landingpage/index.html')
