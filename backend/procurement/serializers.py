from rest_framework import serializers
from .models import Vendor, PurchaseOrder, PurchaseOrderItem, GoodsReceipt, GoodsReceiptItem, InventoryTransaction


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)
    material_code = serializers.CharField(source='material.code', read_only=True)
    material_unit = serializers.CharField(source='material.unit', read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    project_code = serializers.CharField(source='project.code', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PurchaseOrderListSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    project_code = serializers.CharField(source='project.code', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'project', 'project_code', 'vendor', 'vendor_name',
                  'date', 'expected_delivery', 'status', 'total_amount']


class GoodsReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsReceiptItem
        fields = '__all__'


class GoodsReceiptSerializer(serializers.ModelSerializer):
    items = GoodsReceiptItemSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsReceipt
        fields = '__all__'


class InventoryTransactionSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)
    material_code = serializers.CharField(source='material.code', read_only=True)
    project_code = serializers.CharField(source='project.code', read_only=True)

    class Meta:
        model = InventoryTransaction
        fields = '__all__'
