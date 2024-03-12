from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreferences
from django.contrib import messages

def index(request):
    # Check if UserPreferences exists for the current user
    exists = UserPreferences.objects.filter(user=request.user).exists()
    
    # Get the UserPreferences object if it exists
    if exists:
        user_preferences = UserPreferences.objects.get(user=request.user)
    else:
        user_preferences = None

    if request.method == 'GET':
        currency_data = []

        # Load currency data from the JSON file
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                currency_data.append({'name': k, 'value': v})
        
        # Get the selected currency if it exists
        selected_currency = user_preferences.currency if user_preferences else None

        # Render the index.html template with currency data, user preferences, and selected currency
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences, 'selected_currency': selected_currency})
    else:
        # Get the selected currency from the POST data
        currency = request.POST['currency']
        
        # If UserPreferences exists, update the currency field and save
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            # If UserPreferences does not exist, create a new one with the selected currency
            user_preferences = UserPreferences.objects.create(user=request.user, currency=currency)
        
        # Display a success message
        messages.success(request, 'Changes saved')
        
        # Reload the index.html template with the updated user preferences and selected currency
        return render(request, 'preferences/index.html', {'user_preferences': user_preferences, 'selected_currency': currency})
