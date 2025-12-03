from django.contrib import admin
from .models import (
    UserProfile, Crop, Livestock, InventoryItem, 
    FinancialTransaction, Task, Activity, WeatherData
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'farm_name', 'location', 'farm_size']
    list_filter = ['role']
    search_fields = ['user__username', 'farm_name', 'location']


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'variety', 'area', 'planting_date', 'status', 'user']
    list_filter = ['status', 'planting_date']
    search_fields = ['name', 'variety']
    date_hierarchy = 'planting_date'


@admin.register(Livestock)
class LivestockAdmin(admin.ModelAdmin):
    list_display = ['tag_number', 'type', 'breed', 'status', 'weight', 'user']
    list_filter = ['type', 'status', 'gender']
    search_fields = ['tag_number', 'breed']


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'quantity', 'unit', 'needs_reorder', 'user']
    list_filter = ['category', 'unit']
    search_fields = ['name', 'supplier']


@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'category', 'amount', 'description', 'user']
    list_filter = ['type', 'category', 'date']
    search_fields = ['description', 'reference_number']
    date_hierarchy = 'date'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'status', 'due_date', 'assigned_to', 'user']
    list_filter = ['priority', 'status', 'due_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'due_date'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'date', 'user']
    list_filter = ['activity_type', 'date']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['date', 'temperature_high', 'temperature_low', 'humidity', 'rainfall', 'user']
    list_filter = ['date']
    date_hierarchy = 'date'
