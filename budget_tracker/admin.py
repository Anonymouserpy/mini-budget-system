from django.contrib import admin
from . import models

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'gender', 'email')

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'income_type', 'amount', 'date')

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('profile', 'expense_type', 'amount', 'date')

admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Income, IncomeAdmin)
admin.site.register(models.Expense, ExpenseAdmin)