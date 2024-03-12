from django.urls import path
from . import views

app_name = 'userpreferences'

urlpatterns = [
    path('', views.index, name='index'),  # Define the URL pattern for the index view
]