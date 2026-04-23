from rest_framework.routers import DefaultRouter
from .views import (EquipmentCategoryViewSet, EquipmentViewSet,
                    MaterialCategoryViewSet, MaterialViewSet,
                    ResourceAllocationViewSet, MaintenanceRecordViewSet)

router = DefaultRouter()
router.register('equipment-categories', EquipmentCategoryViewSet)
router.register('equipment', EquipmentViewSet)
router.register('material-categories', MaterialCategoryViewSet)
router.register('materials', MaterialViewSet)
router.register('allocations', ResourceAllocationViewSet)
router.register('maintenance', MaintenanceRecordViewSet)

urlpatterns = router.urls
