from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Budget(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='budget')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    contingency_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    notes = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def contingency_amount(self):
        return self.total_amount * (self.contingency_percentage / 100)

    @property
    def allocated_amount(self):
        return sum(item.estimated_amount for item in self.items.all())

    @property
    def spent_amount(self):
        return sum(item.actual_amount for item in self.items.all())

    def __str__(self):
        return f"Budget - {self.project.code}"


class BudgetCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = 'Budget Categories'

    def __str__(self):
        return self.name


class BudgetItem(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='items')
    category = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=300)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=1)
    unit = models.CharField(max_length=50, blank=True)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estimated_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    actual_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    @property
    def variance(self):
        return self.estimated_amount - self.actual_amount

    def __str__(self):
        return f"{self.budget.project.code} - {self.description}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    TYPE_CHOICES = [
        ('client', 'Client Invoice'),
        ('vendor', 'Vendor Invoice'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='client')
    date = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    description = models.TextField(blank=True)
    terms = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.invoice_number


class Payment(models.Model):
    METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('cash', 'Cash'),
        ('online', 'Online Payment'),
        ('credit_card', 'Credit Card'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Payment {self.amount} for {self.invoice.invoice_number}"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('labor', 'Labor'),
        ('materials', 'Materials'),
        ('equipment', 'Equipment'),
        ('subcontractor', 'Subcontractor'),
        ('overhead', 'Overhead'),
        ('transportation', 'Transportation'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='submitted_expenses')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenses')
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.project.code} - {self.description} - {self.amount}"
