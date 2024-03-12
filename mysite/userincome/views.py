from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse



from django.db.models import Q


def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        incomes = UserIncome.objects.filter(
            Q(amount__istartswith=search_str) |
            Q(date__icontains=search_str) |
            Q(description__icontains=search_str) |
            Q(source__name__icontains=search_str),
            owner=request.user
        )
        data = [
            {
                'amount': income.amount,
                'source': income.source.name if income.source else "Uncategorized",
                'description': income.description,
                'date': income.date.strftime('%Y-%m-%d')  # Format date as needed
            }
            for income in incomes
        ]
        return JsonResponse(data, safe=False)




@login_required(login_url='/authentication/login')
def index(request):
    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreferences.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login/')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST,
        }

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('income_date')
        source = request.POST.get('source')  # Get the source name from the form

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', context)

        if not source:
            messages.error(request, 'source is required')
            return render(request, 'income/add_income.html', context)

        try:
            # Get the source instance based on the name provided in the form
            source = Source.objects.get(name=source)
        except Source.DoesNotExist:
            messages.error(request, 'Invalid source')
            return render(request, 'income/add_income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, date=date, 
                               source=source, description=description)
        
        messages.success(request, 'record saved successfully')

        return redirect('income:index')  # Redirect to the index view of income app

    return render(request, 'income/add_income.html', context)

#edit
def Edit_Income(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources':sources

    }

    if request.method == 'GET':
        return render(request, 'income/edit_data.html', context)
    
    elif request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('income_date')
        source = request.POST.get('source')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_data.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_data.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/edit_data.html', context)

        if not source:
            messages.error(request, 'source is required')
            return render(request, 'income/edit_data.html', context)

        try:
            source = Source.objects.get(name=source)
        except source.DoesNotExist:
            messages.error(request, 'Invalid source')
            return render(request, 'income/edit_data.html', context)

        # Update the income object with the new values
        income.owner = request.user
        income.amount = amount
        income.description = description
        income.date = date
        income.source = source
        income.save()

        messages.success(request, 'income updated successfully')

        return redirect('income:index')

#delete
def delete_data(request, id):
    try:
        income = UserIncome.objects.get(pk=id)
        income.delete()
        messages.success(request, 'Record removed successfully')
    except UserIncome.DoesNotExist:
        messages.error(request, 'Income record not found')
    return redirect('income:index')