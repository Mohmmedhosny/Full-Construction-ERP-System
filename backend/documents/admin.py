from django.contrib import admin
from .models import DocumentCategory, Document, DocumentVersion, DrawingSet

admin.site.register(DocumentCategory)
admin.site.register(Document)
admin.site.register(DocumentVersion)
admin.site.register(DrawingSet)
