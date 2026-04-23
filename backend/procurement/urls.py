from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseOrderViewSet, PurchaseOrderItemViewSet, GoodsReceiptViewSet, InventoryTransactionViewSet

router = DefaultRouter()
router.register('vendors', VendorViewSet)
router.register('purchase-orders', PurchaseOrderViewSet)
router.register('po-items', PurchaseOrderItemViewSet)
router.register('goods-receipts', GoodsReceiptViewSet)
router.register('inventory-transactions', InventoryTransactionViewSet)

urlpatterns = router.urls
