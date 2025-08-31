from django.shortcuts import render, redirect, reverse
from . import models 
from django.utils import timezone
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def login_view(request):
    return render(request, 'budget/login.html')

def process_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            profile = models.Profile.objects.get(email=email)
            if profile.check_password(password):
                request.session['profile_id'] = profile.id
                return redirect('budget_tracker:home')
            else:
                return render(request, 'budget/login.html', {
                    'error_message': "Invalid email or password"
                })
        except models.Profile.DoesNotExist:
            return render(request, 'budget/login.html', {
                'error_messge': "Invalid email or password"
            })
        
def register(request):
    genders = models.Profile.GENDER_CHOICES
    return render(request, 'budget/register.html', {
        'genders': genders
    })

def process_register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if models.Profile.objects.filter(email=email).exists():
            return render(request, 'budget/register.html', {
                'error_message': "Email already registered"
            })
        
        profile = models.Profile(
            fname=fname,
            lname=lname,
            gender=gender,
            email=email,
        )
        profile.set_password(password)
        profile.save()

        return redirect('budget_tracker:login_view')

def home(request):
    profile_id = request.session.get('profile_id')
    profile = None
    incomes = []
    expenses = []
    total_income = 0
    total_expense = 0
    balance = 0
    if profile_id:
        try: 
            profile = models.Profile.objects.get(id=profile_id)

            incomes = models.Income.objects.filter(profile=profile).order_by('-date')
            expenses = models.Expense.objects.filter(profile=profile).order_by('-date')

            total_income = sum(i.amount for i in incomes)
            total_expense = sum(e.amount for e in expenses)

            balance = total_income - total_expense

        except models.Profile.DoesNotExist:
            pass

    return render(request, 'budget/home.html', {
        'profile': profile,
        'incomes': incomes,
        'expenses': expenses, 
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    })

def income(request):
    profile_id = request.session.get('profile_id')
    incomes =models.Income.INCOME_TYPE
    return render(request, 'budget/add_income.html',{
        'profile_id':profile_id,
        'incomes': incomes,
        })

def add_income(request):
    profile_id = request.session.get('profile_id')
    if not profile_id:
        return redirect('budget_tracker:login_view')
    
    if request.method == 'POST':
        income_type = request.POST.get('income_type')
        amount = request.POST.get('amount')

        if income_type and amount:
            try:
                profile = models.Profile.objects.get(id=profile_id)
                models.Income.objects.create(
                    profile=profile,
                    income_type=income_type,
                    amount=amount,
                    date = timezone.now()
                )
                return redirect('budget_tracker:home')
            except models.Profile.DoesNotExist:
                pass

    return render(request, 'budget/add_income.html')

def expense(request):
    profile_id = request.session.get('prodile_id')
    expenses = models.Expense.EXPENSE_TYPE
    expense = request.POST.get('expense')
    return render(request, 'budget/add_expense.html', {
        'profile_id': profile_id,
        'expenses': expenses,
        
    })

def add_expense(request):
    profile_id = request.session.get('profile_id')
    if not profile_id:
        return redirect('budget_tracker:login_view')
    
    if request.method == 'POST':
        expense_type = request.POST.get('expense_type')
        custom_expense = request.POST.get('custom_expense')
        amount = request.POST.get('amount')

        if expense_type == "custom" and custom_expense:
            expense_type = custom_expense


        if expense_type and amount:
            try:
                profile = models.Profile.objects.get(id=profile_id)
                models.Expense.objects.create(
                    profile=profile,
                    expense_type=expense_type,
                    amount=amount,
                    date=timezone.now()
                )
                return redirect('budget_tracker:home')
            except models.Profile.DoesNotExist:
                pass

    return render(request, 'budget/add_expense.html',{
        'expenses': models.Expense.EXPENSE_TYPE
    })

def process_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('budget_tracker:home'))
