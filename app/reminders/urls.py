""" URL mappings for the reminder app """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reminders import views

# Name for reverse() function to know where to seek for specific urls
app_name = 'reminders'

router = DefaultRouter()
router.register('reminders', views.ReminderViewSet, basename='reminders')
router.register('tags', views.TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls))
]
