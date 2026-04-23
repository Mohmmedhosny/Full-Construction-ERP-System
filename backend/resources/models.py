from django.db import models
from projects.models import Project


class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Equipment Categories'

    def __str__(self):
        return self.name


class Equipment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
        ('rented', 'Rented Out'),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, related_name='equipment')
    description = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cost_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    location = models.CharField(max_length=200, blank=True)
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class MaterialCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Material Categories'

    def __str__(self):
        return self.name


class Material(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('ton', 'Ton'),
        ('m', 'Meter'),
        ('m2', 'Square Meter'),
        ('m3', 'Cubic Meter'),
        ('unit', 'Unit'),
        ('bag', 'Bag'),
        ('roll', 'Roll'),
        ('liter', 'Liter'),
        ('box', 'Box'),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, related_name='materials')
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='unit')
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_stock = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    minimum_stock = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def needs_reorder(self):
        return self.current_stock <= self.reorder_level


class ResourceAllocation(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('equipment', 'Equipment'),
        ('material', 'Material'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resource_allocations')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True, related_name='allocations')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True, related_name='allocations')
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=1)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        resource = self.equipment or self.material
        return f"{self.project.code} - {resource}"


class MaintenanceRecord(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    performed_by = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment.code} - {self.maintenance_type} - {self.scheduled_date}"
