from django.urls import path
from . import views

app_name = 'profilepage'
urlpatterns = [ 
	path('', views.ProfilepageView.as_view(), name="Profilepage"),
]