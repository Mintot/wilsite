from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [ 
	path('', views.IndexView.as_view(), name="Index"),
	path('register', views.RegistrationView.as_view(), name="Register"),
	path('signin', views.SigninView.as_view(), name="Signin"),
	path('logout', views.LogoutView.as_view(), name="Logout"),
	path('forgotpw', views.ForgetPasswordView.as_view(), name="ForgetPassword"),
	path('changepw', views.ChangePasswordView.as_view(), name="ChangePassword"),
]