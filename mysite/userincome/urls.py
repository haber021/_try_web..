
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


app_name = 'income'  # Define the app namespace


urlpatterns = [
    path('', views.index, name='index'),  
    path('add_income/', views.add_income, name='add_income'),  
    path('edit_data/<int:id>/', views.Edit_Income, name='edit_data'),  
    path('delete_data/<int:id>/', views.delete_data, name='delete_data'),  
    path('search_incomes/', csrf_exempt(views.search_incomes), name='search_incomes'),
]