from django.urls import path
from . import views

app_name = 'budget_tracker'
urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login_view'),
    path('process_login', views.process_login, name='process_login'),
    path('register', views.register, name='register'),
    path('process_register', views.process_register, name='process_register'),
    path('income', views.income, name='income'),
    path('add_income', views.add_income, name='add_income'),
    path('expense', views.expense, name='expense'),
    path('add_expense', views.add_expense, name='add_expense'),
    path('logout', views.process_logout, name='process_logout')
]
