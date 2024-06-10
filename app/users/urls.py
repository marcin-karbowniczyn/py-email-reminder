""" URL mappings for the Users API """
from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateAuthTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
