from rest_framework import serializers
from .models import Budget, BudgetCategory, BudgetItem, Invoice, Payment, Expense


class BudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = '__all__'


class BudgetItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    variance = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = BudgetItem
        fields = '__all__'


class BudgetSerializer(serializers.ModelSerializer):
    items = BudgetItemSerializer(many=True, read_only=True)
    project_code = serializers.CharField(source='project.code', read_only=True)
    contingency_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    allocated_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    spent_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Budget
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    project_code = serializers.CharField(source='project.code', read_only=True)
    balance_due = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceListSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(source='project.code', read_only=True)
    balance_due = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'project', 'project_code', 'invoice_type',
                  'date', 'due_date', 'total_amount', 'paid_amount', 'balance_due', 'status']


class ExpenseSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(source='project.code', read_only=True)
    submitted_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = '__all__'

    def get_submitted_by_name(self, obj):
        if obj.submitted_by:
            return f"{obj.submitted_by.first_name} {obj.submitted_by.last_name}".strip() or obj.submitted_by.username
        return None
