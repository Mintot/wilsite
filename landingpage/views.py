from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def landingpage(request):
	return render(request, 'landingpage/index.html')
