from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    UserProfile, Crop, Livestock, InventoryItem,
    FinancialTransaction, Task, Activity, WeatherData
)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'farm_name', 'location', 'farm_size', 'avatar']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'farm_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'farm_size': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = [
            'name', 'variety', 'area', 'planting_date', 'expected_harvest_date',
            'actual_harvest_date', 'status', 'expected_yield', 'actual_yield', 'notes', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'variety': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'planting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_harvest_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actual_harvest_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'expected_yield': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_yield': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LivestockForm(forms.ModelForm):
    class Meta:
        model = Livestock
        fields = [
            'type', 'breed', 'tag_number', 'date_acquired', 'date_of_birth',
            'gender', 'status', 'weight', 'purchase_price', 'current_value', 'notes', 'image'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'tag_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_acquired': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            'name', 'category', 'quantity', 'unit', 'reorder_level',
            'cost_per_unit', 'supplier', 'purchase_date', 'expiry_date', 'location', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_per_unit': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FinancialTransactionForm(forms.ModelForm):
    class Meta:
        model = FinancialTransaction
        fields = [
            'type', 'category', 'amount', 'date', 'description',
            'payment_method', 'reference_number', 'notes', 'receipt'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'priority', 'status', 'assigned_to',
            'due_date', 'completed_date', 'related_crop', 'related_livestock', 'notes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'related_crop': forms.Select(attrs={'class': 'form-control'}),
            'related_livestock': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'activity_type', 'title', 'description', 'date', 'duration',
            'related_crop', 'related_livestock', 'labor_cost', 'materials_used', 'notes', 'images'
        ]
        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'related_crop': forms.Select(attrs={'class': 'form-control'}),
            'related_livestock': forms.Select(attrs={'class': 'form-control'}),
            'labor_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'materials_used': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class WeatherDataForm(forms.ModelForm):
    class Meta:
        model = WeatherData
        fields = [
            'date', 'temperature_high', 'temperature_low', 'humidity',
            'rainfall', 'wind_speed', 'conditions', 'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'temperature_high': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature_low': forms.NumberInput(attrs={'class': 'form-control'}),
            'humidity': forms.NumberInput(attrs={'class': 'form-control'}),
            'rainfall': forms.NumberInput(attrs={'class': 'form-control'}),
            'wind_speed': forms.NumberInput(attrs={'class': 'form-control'}),
            'conditions': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
