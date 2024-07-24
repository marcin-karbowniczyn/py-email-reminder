""" URL mappings for the reminder app """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reminders import views

# Name for reverse() function to know where to seek for specific urls
app_name = 'reminders'

router = DefaultRouter()
router.register('', views.ReminderViewSet, basename='reminders')

urlpatterns = [
    path('', include(router.urls))
]
