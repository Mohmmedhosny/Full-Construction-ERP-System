from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class DocumentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Document Categories'

    def __str__(self):
        return self.name


class Document(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('superseded', 'Superseded'),
        ('archived', 'Archived'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, related_name='documents')
    name = models.CharField(max_length=300)
    document_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/', null=True, blank=True)
    file_size = models.PositiveBigIntegerField(default=0)
    version = models.CharField(max_length=20, default='1.0')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    tags = models.CharField(max_length=500, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_documents')
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project.code} - {self.name} v{self.version}"


class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    version = models.CharField(max_length=20)
    file = models.FileField(upload_to='documents/versions/%Y/%m/')
    change_notes = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.document.name} v{self.version}"


class DrawingSet(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='drawing_sets')
    name = models.CharField(max_length=200)
    discipline = models.CharField(max_length=100, blank=True)
    revision = models.CharField(max_length=20, blank=True)
    issued_date = models.DateField(null=True, blank=True)
    documents = models.ManyToManyField(Document, blank=True, related_name='drawing_sets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.code} - {self.name}"
