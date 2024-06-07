""" URL mappings for the Users API """
from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateAuthTokenView.as_view(), name='token')
]
