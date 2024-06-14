""" URL mappings for the Users API """
from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterNewUserView.as_view(), name='register'),
    path('token/', views.CreateAuthTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('changepassword/', views.ChangeUserPasswordView.as_view(), name='changepassword'),
]
