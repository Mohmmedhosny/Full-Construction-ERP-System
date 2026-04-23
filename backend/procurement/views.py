from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from .models import Vendor, PurchaseOrder, PurchaseOrderItem, GoodsReceipt, GoodsReceiptItem, InventoryTransaction
from .serializers import (
    VendorSerializer, PurchaseOrderSerializer, PurchaseOrderListSerializer,
    PurchaseOrderItemSerializer, GoodsReceiptSerializer, GoodsReceiptItemSerializer,
    InventoryTransactionSerializer
)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['name', 'code', 'contact_person', 'email']
    ordering_fields = ['name', 'rating']


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.select_related('project', 'vendor').prefetch_related('items').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'project', 'vendor']
    search_fields = ['po_number']
    ordering_fields = ['date', 'total_amount']

    def get_serializer_class(self):
        if self.action == 'list':
            return PurchaseOrderListSerializer
        return PurchaseOrderSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def pending_delivery(self, request):
        pos = PurchaseOrder.objects.filter(status__in=['approved', 'sent', 'partial'])
        serializer = PurchaseOrderListSerializer(pos, many=True)
        return Response(serializer.data)


class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderItem.objects.select_related('purchase_order', 'material').all()
    serializer_class = PurchaseOrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['purchase_order']


class GoodsReceiptViewSet(viewsets.ModelViewSet):
    queryset = GoodsReceipt.objects.select_related('purchase_order').prefetch_related('items').all()
    serializer_class = GoodsReceiptSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['purchase_order']

    def perform_create(self, serializer):
        serializer.save(received_by=self.request.user)


class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransaction.objects.select_related('material', 'project').all()
    serializer_class = InventoryTransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['material', 'transaction_type', 'project']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        transaction = serializer.save(created_by=self.request.user)
        material = transaction.material
        if transaction.transaction_type in ['receipt', 'return', 'adjustment']:
            material.current_stock += transaction.quantity
        elif transaction.transaction_type == 'issue':
            material.current_stock -= transaction.quantity
        material.save()

    @action(detail=False, methods=['get'])
    def stock_summary(self, request):
        from resources.models import Material
        from resources.serializers import MaterialSerializer
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)
