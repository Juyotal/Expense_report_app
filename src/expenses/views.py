from django.contrib.auth.models import User
from django.core import paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Category, Expense
from .forms import ExpenseForm
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime


@login_required(login_url='/authentication/login')
def index(request, context={}):
    catergories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)

    preference = UserPreference.objects.get(user = request.user)
    currency = preference.currency

    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context['currency']= currency
    context['expenses'] = expenses
    context['categories']= catergories
    context['page_obj'] = page_obj
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request, context={}):

    
    catergories = Category.objects.all()
    context['categories']= catergories
    context['values'] = request.POST

    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')
    
@login_required(login_url='/authentication/login')
def expense_edit(request, pk):
    expense = Expense.objects.get(pk=pk)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit_expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense. date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')

def search_expenses(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        search_str = data['searchText']

        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)

        data = expenses.values()

        return JsonResponse(list(data), safe=False)


def expense_summary(request):
    today = datetime.date.today()
    six_months_ago = today - datetime.timedelta(days=30*6)

    expenses = Expense.objects.filter(date__gte=six_months_ago, owner=request.user)

    final_rep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))


    def get_expense_category_amount(category):
        amount=0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            final_rep[y]= get_expense_category_amount(y)

    return JsonResponse({'expense_data': final_rep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')