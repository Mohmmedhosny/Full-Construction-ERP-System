from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from .models import Budget, BudgetCategory, BudgetItem, Invoice, Payment, Expense
from .serializers import (
    BudgetSerializer, BudgetCategorySerializer, BudgetItemSerializer,
    InvoiceSerializer, InvoiceListSerializer, PaymentSerializer, ExpenseSerializer
)


class BudgetCategoryViewSet(viewsets.ModelViewSet):
    queryset = BudgetCategory.objects.all()
    serializer_class = BudgetCategorySerializer


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.select_related('project').prefetch_related('items').all()
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']


class BudgetItemViewSet(viewsets.ModelViewSet):
    queryset = BudgetItem.objects.select_related('budget', 'category').all()
    serializer_class = BudgetItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['budget', 'category']


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('project').prefetch_related('payments').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'invoice_type', 'project']
    search_fields = ['invoice_number', 'description']
    ordering_fields = ['date', 'due_date', 'total_amount']

    def get_serializer_class(self):
        if self.action == 'list':
            return InvoiceListSerializer
        return InvoiceSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        from django.utils import timezone
        today = timezone.now().date()
        invoices = Invoice.objects.filter(due_date__lt=today, status__in=['sent', 'partial'])
        serializer = InvoiceListSerializer(invoices, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        data = Invoice.objects.aggregate(
            total_invoiced=Sum('total_amount'),
            total_paid=Sum('paid_amount'),
        )
        data['total_outstanding'] = (data['total_invoiced'] or 0) - (data['total_paid'] or 0)
        data['by_status'] = list(
            Invoice.objects.values('status').annotate(count=Count('id'), amount=Sum('total_amount'))
        )
        return Response(data)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('invoice').all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['invoice', 'method']
    ordering_fields = ['date', 'amount']

    def perform_create(self, serializer):
        payment = serializer.save(recorded_by=self.request.user)
        invoice = payment.invoice
        invoice.paid_amount = sum(p.amount for p in invoice.payments.all())
        if invoice.paid_amount >= invoice.total_amount:
            invoice.status = 'paid'
        elif invoice.paid_amount > 0:
            invoice.status = 'partial'
        invoice.save()


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related('project', 'submitted_by').all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'category', 'status']
    search_fields = ['description']
    ordering_fields = ['date', 'amount']

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)

    @action(detail=False, methods=['get'])
    def by_project(self, request):
        data = Expense.objects.values('project__code', 'project__name').annotate(
            total=Sum('amount'), count=Count('id')
        )
        return Response(list(data))
