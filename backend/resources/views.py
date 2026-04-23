from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import EquipmentCategory, Equipment, MaterialCategory, Material, ResourceAllocation, MaintenanceRecord
from .serializers import (
    EquipmentCategorySerializer, EquipmentSerializer,
    MaterialCategorySerializer, MaterialSerializer,
    ResourceAllocationSerializer, MaintenanceRecordSerializer
)


class EquipmentCategoryViewSet(viewsets.ModelViewSet):
    queryset = EquipmentCategory.objects.all()
    serializer_class = EquipmentCategorySerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.select_related('category').all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['name', 'code', 'serial_number']
    ordering_fields = ['name', 'cost_per_day', 'purchase_date']

    @action(detail=False, methods=['get'])
    def available(self, request):
        equipment = Equipment.objects.filter(status='available')
        serializer = self.get_serializer(equipment, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def maintenance_due(self, request):
        from django.utils import timezone
        today = timezone.now().date()
        equipment = Equipment.objects.filter(next_maintenance__lte=today).exclude(status='retired')
        serializer = self.get_serializer(equipment, many=True)
        return Response(serializer.data)


class MaterialCategoryViewSet(viewsets.ModelViewSet):
    queryset = MaterialCategory.objects.all()
    serializer_class = MaterialCategorySerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.select_related('category').all()
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'unit']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'unit_cost', 'current_stock']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        materials = [m for m in Material.objects.all() if m.needs_reorder]
        serializer = self.get_serializer(materials, many=True)
        return Response(serializer.data)


class ResourceAllocationViewSet(viewsets.ModelViewSet):
    queryset = ResourceAllocation.objects.select_related('project', 'equipment', 'material').all()
    serializer_class = ResourceAllocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'resource_type']


class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.select_related('equipment').all()
    serializer_class = MaintenanceRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['equipment', 'status']
    ordering_fields = ['scheduled_date', 'cost']
