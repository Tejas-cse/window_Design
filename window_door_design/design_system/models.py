from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class PricingRate(models.Model):
    """Stores predefined pricing rates for materials and components"""
    MATERIAL_TYPE_CHOICES = [
        ('aluminum', 'Aluminum'),
        ('upvc', 'UPVC'),
        ('steel', 'Steel'),
        ('wood', 'Wood'),
    ]
    
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)
    rate_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    labor_cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    glass_cost_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    mesh_cost_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    profile_cost_per_meter = models.DecimalField(max_digits=10, decimal_places=2, default=150)
    
    class Meta:
        verbose_name_plural = "Pricing Rates"
    
    def __str__(self):
        return f"{self.get_material_type_display()} - Rates"


class WindowDoorDesign(models.Model):
    """Main model to store window/door design specifications"""
    TYPE_CHOICES = [
        ('sliding', 'Sliding'),
        ('casement', 'Casement'),
        ('awning', 'Awning'),
        ('tilt_turn', 'Tilt & Turn'),
        ('fixed', 'Fixed'),
        ('bifold', 'Bifold'),
        ('revolving', 'Revolving'),
    ]
    
    GLASS_TYPE_CHOICES = [
        ('clear', 'Clear Glass'),
        ('tinted', 'Tinted Glass'),
        ('frosted', 'Frosted Glass'),
        ('double_glazed', 'Double Glazed'),
        ('tempered', 'Tempered Glass'),
    ]
    
    FINISH_TYPE_CHOICES = [
        ('anodized', 'Anodized'),
        ('powder_coated', 'Powder Coated'),
        ('raw', 'Raw'),
        ('painted', 'Painted'),
        ('natural_wood', 'Natural Wood'),
    ]
    
    MATERIAL_CHOICES = [
        ('aluminum', 'Aluminum'),
        ('upvc', 'UPVC'),
        ('steel', 'Steel'),
        ('wood', 'Wood'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1)])  # in meters
    height = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.1)])  # in meters
    type_choice = models.CharField(max_length=20, choices=TYPE_CHOICES)
    glass_type = models.CharField(max_length=20, choices=GLASS_TYPE_CHOICES)
    has_mesh = models.BooleanField(default=False)
    finish_type = models.CharField(max_length=20, choices=FINISH_TYPE_CHOICES)
    number_of_units = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, default='aluminum')
    
    # Calculated fields
    total_area = models.DecimalField(max_digits=10, decimal_places=4, editable=False, default=0)
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, editable=False, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Window/Door Designs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def calculate_area(self):
        """Calculate total area in square meters"""
        return (self.width * self.height * self.number_of_units)
    
    def save(self, *args, **kwargs):
        self.total_area = self.calculate_area()
        super().save(*args, **kwargs)


class DesignReport(models.Model):
    """Store generated reports for designs"""
    REPORT_TYPE_CHOICES = [
        ('quotation', 'Quotation'),
        ('boq', 'Bill of Quantities'),
        ('cutting_list', 'Cutting List'),
        ('material_summary', 'Material Summary'),
    ]
    
    design = models.ForeignKey(WindowDoorDesign, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    file_path = models.FileField(upload_to='reports/%Y/%m/%d/', blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Design Reports"
    
    def __str__(self):
        return f"{self.design.name} - {self.get_report_type_display()}"
