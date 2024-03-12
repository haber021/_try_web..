from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from .models import Category, Expense
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.utils.dateparse import parse_date

from userpreferences.models import UserPreferences


#search bar backend
from .models import Expense  # Import the Expense model

from django.db.models import Q

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            Q(amount__istartswith=search_str) |
            Q(date__icontains=search_str) |
            Q(description__icontains=search_str) |
            Q(category__name__icontains=search_str),
            owner=request.user
        )
        data = [
            {
                'amount': expense.amount,
                'expense': expense.category.name if expense.category else "Uncategorized",
                'description': expense.description,
                'date': expense.date.strftime('%Y-%m-%d')  # Format date as needed
            }
            for expense in expenses
        ]
        return JsonResponse(data, safe=False)






@login_required(login_url='/authentication/login/')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator=Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj=Paginator.get_page(paginator, page_number)
    currency = UserPreferences.objects.get(user=request.user).currency
    context = {
        'expenses':expenses,
        'page_obj':page_obj,
        'currency': currency,
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/authentication/login/')
def logout(request):
    if not request.session.get('refreshed', False):
        request.session['refreshed'] = True
        django_logout(request)
        # Redirect to the home page after a delay of 3 seconds (3000 milliseconds)
        return redirect('expenses:index')  # Corrected redirection to 'expenses:index'
    else:
        # Redirect to the login page if already refreshed
        return redirect('authentication:login')

@login_required(login_url='/authentication/login/')
def add_expenses(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('expense_date')
        category_name = request.POST.get('category')  # Get the category name from the form

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expenses.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expenses.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expenses.html', context)

        if not category_name:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expenses.html', context)

        try:
            # Get the Category instance based on the name provided in the form
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category')
            return render(request, 'expenses/add_expenses.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date, 
                               category=category, description=description)
        
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses:index')  # Redirect to the index view of expenses app

    return render(request, 'expenses/add_expenses.html', context)


#edit
def Edit_expenses(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
    }

    if request.method == 'GET':
        return render(request, 'expenses/edit_data.html', context)
    
    elif request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('expense_date')
        category_name = request.POST.get('category')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_data.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit_data.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/edit_data.html', context)

        if not category_name:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/edit_data.html', context)

        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category')
            return render(request, 'expenses/edit_data.html', context)

        # Update the expense object with the new values
        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.category = category
        expense.save()

        messages.success(request, 'Expense updated successfully')

        return redirect('expenses:index')

#delete
from django.shortcuts import get_object_or_404

def delete_data(request, id):
    expense = get_object_or_404(Expense, pk=id)
    expense.delete()
    messages.success(request, 'Expense removed successfully')
    return redirect('expenses:index')