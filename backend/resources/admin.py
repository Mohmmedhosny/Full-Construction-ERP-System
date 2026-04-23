from django.contrib import admin
from .models import EquipmentCategory, Equipment, MaterialCategory, Material, ResourceAllocation, MaintenanceRecord

admin.site.register(EquipmentCategory)
admin.site.register(Equipment)
admin.site.register(MaterialCategory)
admin.site.register(Material)
admin.site.register(ResourceAllocation)
admin.site.register(MaintenanceRecord)
