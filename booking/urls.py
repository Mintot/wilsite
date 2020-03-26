from django.urls import path
from . import views

app_name = 'booking'
urlpatterns = [ 
	path('', views.BookingView.as_view(), name="Booking"),
	path('bookdetails', views.BookingDetailsView.as_view(), name="BookingDetails"),
	path('bookinfo', views.BookingInfoView.as_view(), name="BookingInfo"),
	path('ajax/book', views.review_book, name="review_book")
]