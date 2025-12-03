from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile for farm management system"""
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('manager', 'Farm Manager'),
        ('worker', 'Worker'),
        ('consultant', 'Consultant'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')
    phone = models.CharField(max_length=20, blank=True)
    farm_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    farm_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Farm size in acres")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Crop(models.Model):
    """Model for managing crops"""
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('planted', 'Planted'),
        ('growing', 'Growing'),
        ('harvested', 'Harvested'),
        ('sold', 'Sold'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in acres")
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    actual_harvest_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    expected_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Expected yield in kg")
    actual_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Actual yield in kg")
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='crops/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-planting_date']
    
    def __str__(self):
        return f"{self.name} - {self.variety} ({self.planting_date})"
    
    @property
    def days_to_harvest(self):
        if self.status in ['harvested', 'sold']:
            return 0
        delta = self.expected_harvest_date - timezone.now().date()
        return max(0, delta.days)


class Livestock(models.Model):
    """Model for managing livestock"""
    TYPE_CHOICES = [
        ('cattle', 'Cattle'),
        ('poultry', 'Poultry'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
        ('pig', 'Pig'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('sick', 'Sick'),
        ('under_treatment', 'Under Treatment'),
        ('pregnant', 'Pregnant'),
        ('sold', 'Sold'),
        ('deceased', 'Deceased'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='livestock')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    breed = models.CharField(max_length=100)
    tag_number = models.CharField(max_length=50, unique=True)
    date_acquired = models.DateField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='healthy')
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='livestock/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_acquired']
        verbose_name_plural = 'Livestock'
    
    def __str__(self):
        return f"{self.type} - {self.tag_number}"


class InventoryItem(models.Model):
    """Model for managing farm inventory"""
    CATEGORY_CHOICES = [
        ('seed', 'Seeds'),
        ('fertilizer', 'Fertilizers'),
        ('pesticide', 'Pesticides'),
        ('equipment', 'Equipment'),
        ('feed', 'Animal Feed'),
        ('medicine', 'Veterinary Medicine'),
        ('fuel', 'Fuel'),
        ('other', 'Other'),
    ]
    
    UNIT_CHOICES = [
        ('kg', 'Kilograms'),
        ('lbs', 'Pounds'),
        ('ltr', 'Liters'),
        ('gal', 'Gallons'),
        ('bag', 'Bags'),
        ('pcs', 'Pieces'),
        ('unit', 'Units'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, help_text="Minimum quantity before reorder")
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=200, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True, help_text="Storage location")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
    
    @property
    def needs_reorder(self):
        return self.quantity <= self.reorder_level
    
    @property
    def total_value(self):
        return self.quantity * self.cost_per_unit


class FinancialTransaction(models.Model):
    """Model for managing financial transactions"""
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    CATEGORY_CHOICES = [
        ('crop_sale', 'Crop Sale'),
        ('livestock_sale', 'Livestock Sale'),
        ('seed_purchase', 'Seed Purchase'),
        ('fertilizer_purchase', 'Fertilizer Purchase'),
        ('pesticide_purchase', 'Pesticide Purchase'),
        ('equipment_purchase', 'Equipment Purchase'),
        ('fuel', 'Fuel'),
        ('labor', 'Labor Cost'),
        ('veterinary', 'Veterinary Services'),
        ('maintenance', 'Maintenance'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=300)
    payment_method = models.CharField(max_length=50, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.type} - {self.category}: ${self.amount} on {self.date}"


class Task(models.Model):
    """Model for managing farm tasks"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    due_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    related_crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    related_livestock = models.ForeignKey(Livestock, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date', '-priority']
    
    def __str__(self):
        return f"{self.title} - {self.due_date}"
    
    @property
    def is_overdue(self):
        if self.status in ['completed', 'cancelled']:
            return False
        return self.due_date < timezone.now().date()


class Activity(models.Model):
    """Model for logging farm activities"""
    ACTIVITY_TYPE_CHOICES = [
        ('planting', 'Planting'),
        ('irrigation', 'Irrigation'),
        ('fertilization', 'Fertilization'),
        ('pesticide_application', 'Pesticide Application'),
        ('weeding', 'Weeding'),
        ('harvesting', 'Harvesting'),
        ('feeding', 'Animal Feeding'),
        ('vaccination', 'Vaccination'),
        ('health_check', 'Health Check'),
        ('milking', 'Milking'),
        ('maintenance', 'Equipment Maintenance'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in minutes")
    related_crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    related_livestock = models.ForeignKey(Livestock, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    materials_used = models.TextField(blank=True, help_text="Materials and quantities used")
    notes = models.TextField(blank=True)
    images = models.ImageField(upload_to='activities/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Activities'
    
    def __str__(self):
        return f"{self.activity_type} - {self.title} on {self.date.date()}"


class WeatherData(models.Model):
    """Model for storing weather data"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weather_data')
    date = models.DateField(default=timezone.now)
    temperature_high = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperature_low = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    rainfall = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Rainfall in mm")
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    conditions = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Weather Data'
    
    def __str__(self):
        return f"Weather for {self.date}"
