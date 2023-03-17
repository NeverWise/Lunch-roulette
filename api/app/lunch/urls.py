"""
URL mappings for the lunch app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from lunch import views


router = DefaultRouter()
router.register('places', views.PlaceViewSet)

app_name = 'lunch'

urlpatterns = [
    path('', include(router.urls)),
]
