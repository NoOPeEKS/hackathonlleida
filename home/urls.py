from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api-vision', views.api_vision, name='api-vision'),
    path('api-description', views.api_description, name='api-description'),
    path('api-property', views.api_property, name='api-property'),
    path('api-intelligence', views.api_intelligence, name='api-intelligence')
]
