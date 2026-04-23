from rest_framework import serializers
from .models import DocumentCategory, Document, DocumentVersion, DrawingSet


class DocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = '__all__'


class DocumentVersionSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = DocumentVersion
        fields = '__all__'

    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            return f"{obj.uploaded_by.first_name} {obj.uploaded_by.last_name}".strip() or obj.uploaded_by.username
        return None


class DocumentSerializer(serializers.ModelSerializer):
    versions = DocumentVersionSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    project_code = serializers.CharField(source='project.code', read_only=True)
    uploaded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = '__all__'

    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            return f"{obj.uploaded_by.first_name} {obj.uploaded_by.last_name}".strip() or obj.uploaded_by.username
        return None


class DocumentListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    project_code = serializers.CharField(source='project.code', read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'name', 'document_number', 'project', 'project_code', 'category',
                  'category_name', 'version', 'status', 'tags', 'file_size', 'created_at']


class DrawingSetSerializer(serializers.ModelSerializer):
    documents = DocumentListSerializer(many=True, read_only=True)
    project_code = serializers.CharField(source='project.code', read_only=True)

    class Meta:
        model = DrawingSet
        fields = '__all__'
