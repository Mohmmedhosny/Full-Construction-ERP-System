from rest_framework.routers import DefaultRouter
from .views import BudgetCategoryViewSet, BudgetViewSet, BudgetItemViewSet, InvoiceViewSet, PaymentViewSet, ExpenseViewSet

router = DefaultRouter()
router.register('budget-categories', BudgetCategoryViewSet)
router.register('budgets', BudgetViewSet)
router.register('budget-items', BudgetItemViewSet)
router.register('invoices', InvoiceViewSet)
router.register('payments', PaymentViewSet)
router.register('expenses', ExpenseViewSet)

urlpatterns = router.urls
