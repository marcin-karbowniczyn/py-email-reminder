""" URL mappings for the remainder app """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from remainders import views

app_name = 'remainders'

router = DefaultRouter()
router.register('', views.RemainderViewSet, basename='remainders')

urlpatterns = [
    path('', include(router.urls))
]
