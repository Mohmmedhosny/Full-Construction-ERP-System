from rest_framework.routers import DefaultRouter
from .views import DocumentCategoryViewSet, DocumentViewSet, DocumentVersionViewSet, DrawingSetViewSet

router = DefaultRouter()
router.register('categories', DocumentCategoryViewSet)
router.register('documents', DocumentViewSet)
router.register('versions', DocumentVersionViewSet)
router.register('drawing-sets', DrawingSetViewSet)

urlpatterns = router.urls
