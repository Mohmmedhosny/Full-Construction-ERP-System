from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import DocumentCategory, Document, DocumentVersion, DrawingSet
from .serializers import (
    DocumentCategorySerializer, DocumentSerializer, DocumentListSerializer,
    DocumentVersionSerializer, DrawingSetSerializer
)


class DocumentCategoryViewSet(viewsets.ModelViewSet):
    queryset = DocumentCategory.objects.all()
    serializer_class = DocumentCategorySerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('project', 'category', 'uploaded_by').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'category', 'status']
    search_fields = ['name', 'document_number', 'tags', 'description']
    ordering_fields = ['name', 'created_at', 'version']

    def get_serializer_class(self):
        if self.action == 'list':
            return DocumentListSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        file = self.request.data.get('file')
        file_size = file.size if file else 0
        serializer.save(uploaded_by=self.request.user, file_size=file_size)

    @action(detail=True, methods=['post'])
    def new_version(self, request, pk=None):
        document = self.get_object()
        serializer = DocumentVersionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(document=document, uploaded_by=request.user)
            document.version = request.data.get('version', document.version)
            document.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        from django.utils import timezone
        from datetime import timedelta
        threshold = timezone.now().date() + timedelta(days=30)
        docs = Document.objects.filter(expiry_date__lte=threshold, expiry_date__isnull=False)
        serializer = DocumentListSerializer(docs, many=True)
        return Response(serializer.data)


class DocumentVersionViewSet(viewsets.ModelViewSet):
    queryset = DocumentVersion.objects.select_related('document', 'uploaded_by').all()
    serializer_class = DocumentVersionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['document']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class DrawingSetViewSet(viewsets.ModelViewSet):
    queryset = DrawingSet.objects.select_related('project').prefetch_related('documents').all()
    serializer_class = DrawingSetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['project']
    search_fields = ['name', 'discipline']
