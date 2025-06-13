from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime

# Create your views here.
@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user)
    total = sum(exp.amount for exp in expenses)
    
    # Calculate monthly total
    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_expenses = expenses.filter(date__month=current_month, date__year=current_year)
    monthly_total = sum(exp.amount for exp in monthly_expenses)
    
    return render(request, 'expenses/home.html', {
        'expenses': expenses,
        'total': total,
        'monthly_total': monthly_total
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            return redirect('expense:home')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def logout(request):
    return render(request, 'expenses/logout.html')
