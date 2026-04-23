from django.contrib import admin
from .models import Vendor, PurchaseOrder, PurchaseOrderItem, GoodsReceipt, InventoryTransaction

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(GoodsReceipt)
admin.site.register(InventoryTransaction)
