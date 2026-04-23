from rest_framework import serializers
from .models import EquipmentCategory, Equipment, MaterialCategory, Material, ResourceAllocation, MaintenanceRecord


class EquipmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'


class MaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    needs_reorder = serializers.BooleanField(read_only=True)

    class Meta:
        model = Material
        fields = '__all__'


class ResourceAllocationSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    material_name = serializers.CharField(source='material.name', read_only=True)
    project_code = serializers.CharField(source='project.code', read_only=True)

    class Meta:
        model = ResourceAllocation
        fields = '__all__'


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)

    class Meta:
        model = MaintenanceRecord
        fields = '__all__'
