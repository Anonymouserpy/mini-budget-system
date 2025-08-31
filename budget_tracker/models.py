from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class Profile(models.Model):
    GENDER_CHOICES = [ 
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    fname = models.CharField(max_length=200, verbose_name='First Name')
    lname = models.CharField(max_length=200, verbose_name='Last Name')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True, max_length=200, verbose_name='Email')
    password = models.CharField(max_length=200, default=True)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"{self.fname} {self.lname}"
    
class Income(models.Model):
    INCOME_TYPE = [
        ('salary', 'Salary'),
        ('freelance', 'Freelance Work'),
        ('business', 'Business Income'),
        ('commission', 'Commission'),
        ('allowance', 'Allowance'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    income_type = models.CharField(max_length=200, choices=INCOME_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.profile.email} {self.income_type} {self.amount} {self.date}"
    
class Expense(models.Model):
    EXPENSE_TYPE = [
        ('food', 'Food & Dining'),
        ('transport', 'Transportation'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=100, choices=EXPENSE_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.profile.email} {self.expense_type} {self.amount} {self.date}"
    
