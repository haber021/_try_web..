
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


app_name = 'expenses'  # Define the app namespace


urlpatterns = [
    path('', views.index, name='index'),  
    path('logout/', views.logout, name='logout'),  
    path('add_expenses/', views.add_expenses, name='add_expenses'),  
    path('edit_data/<int:id>/', views.Edit_expenses, name='edit_data'),  
    path('delete_data/<int:id>/', views.delete_data, name='delete_data'),  
    path('search_expenses/', csrf_exempt(views.search_expenses), name='search_expenses'),
]