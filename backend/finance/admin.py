from django.contrib import admin
from .models import Budget, BudgetCategory, BudgetItem, Invoice, Payment, Expense

admin.site.register(Budget)
admin.site.register(BudgetCategory)
admin.site.register(BudgetItem)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Expense)
