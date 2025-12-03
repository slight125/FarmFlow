from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    UserProfile, Crop, Livestock, InventoryItem,
    FinancialTransaction, Task, Activity, WeatherData
)
from .forms import (
    UserRegisterForm, UserProfileForm, CropForm, LivestockForm,
    InventoryItemForm, FinancialTransactionForm, TaskForm,
    ActivityForm, WeatherDataForm
)


def homepage(request):
    """Homepage view"""
    return render(request, 'farm/homepage.html')


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'farm/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'farm/login.html')


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    """Main dashboard view with statistics and overview"""
    user = request.user
    
    # Get statistics
    total_crops = Crop.objects.filter(user=user).count()
    active_crops = Crop.objects.filter(user=user, status__in=['planted', 'growing']).count()
    total_livestock = Livestock.objects.filter(user=user).exclude(status__in=['sold', 'deceased']).count()
    
    # Financial statistics
    current_month = timezone.now().replace(day=1)
    income = FinancialTransaction.objects.filter(
        user=user, type='income', date__gte=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expenses = FinancialTransaction.objects.filter(
        user=user, type='expense', date__gte=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    net_income = income - expenses
    
    # Inventory alerts
    low_stock_items = InventoryItem.objects.filter(user=user, quantity__lte=models.F('reorder_level')).count()
    
    # Upcoming tasks
    upcoming_tasks = Task.objects.filter(
        user=user, status__in=['pending', 'in_progress']
    ).order_by('due_date')[:5]
    
    # Recent activities
    recent_activities = Activity.objects.filter(user=user).order_by('-date')[:10]
    
    # Crops near harvest
    upcoming_harvests = Crop.objects.filter(
        user=user, status__in=['planted', 'growing'],
        expected_harvest_date__lte=timezone.now().date() + timedelta(days=30)
    ).order_by('expected_harvest_date')[:5]
    
    # Recent transactions
    recent_transactions = FinancialTransaction.objects.filter(user=user).order_by('-date')[:5]
    
    context = {
        'total_crops': total_crops,
        'active_crops': active_crops,
        'total_livestock': total_livestock,
        'income': income,
        'expenses': expenses,
        'net_income': net_income,
        'low_stock_items': low_stock_items,
        'upcoming_tasks': upcoming_tasks,
        'recent_activities': recent_activities,
        'upcoming_harvests': upcoming_harvests,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'farm/dashboard.html', context)


# Crop Views
@login_required
def crop_list(request):
    """List all crops"""
    crops = Crop.objects.filter(user=request.user).order_by('-planting_date')
    status_filter = request.GET.get('status')
    if status_filter:
        crops = crops.filter(status=status_filter)
    
    context = {
        'crops': crops,
        'status_filter': status_filter,
    }
    return render(request, 'farm/crop_list.html', context)


@login_required
def crop_detail(request, pk):
    """View crop details"""
    crop = get_object_or_404(Crop, pk=pk, user=request.user)
    activities = crop.activities.all().order_by('-date')[:10]
    tasks = crop.tasks.all().order_by('due_date')
    
    context = {
        'crop': crop,
        'activities': activities,
        'tasks': tasks,
    }
    return render(request, 'farm/crop_detail.html', context)


@login_required
def crop_create(request):
    """Create new crop"""
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.user = request.user
            crop.save()
            messages.success(request, 'Crop added successfully!')
            return redirect('crop_list')
    else:
        form = CropForm()
    return render(request, 'farm/crop_form.html', {'form': form, 'title': 'Add New Crop'})


@login_required
def crop_update(request, pk):
    """Update crop"""
    crop = get_object_or_404(Crop, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CropForm(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crop updated successfully!')
            return redirect('crop_detail', pk=pk)
    else:
        form = CropForm(instance=crop)
    return render(request, 'farm/crop_form.html', {'form': form, 'title': 'Update Crop'})


@login_required
def crop_delete(request, pk):
    """Delete crop"""
    crop = get_object_or_404(Crop, pk=pk, user=request.user)
    if request.method == 'POST':
        crop.delete()
        messages.success(request, 'Crop deleted successfully!')
        return redirect('crop_list')
    return render(request, 'farm/crop_confirm_delete.html', {'crop': crop})


# Livestock Views
@login_required
def livestock_list(request):
    """List all livestock"""
    livestock = Livestock.objects.filter(user=request.user).order_by('-date_acquired')
    type_filter = request.GET.get('type')
    status_filter = request.GET.get('status')
    
    if type_filter:
        livestock = livestock.filter(type=type_filter)
    if status_filter:
        livestock = livestock.filter(status=status_filter)
    
    context = {
        'livestock': livestock,
        'type_filter': type_filter,
        'status_filter': status_filter,
    }
    return render(request, 'farm/livestock_list.html', context)


@login_required
def livestock_detail(request, pk):
    """View livestock details"""
    animal = get_object_or_404(Livestock, pk=pk, user=request.user)
    activities = animal.activities.all().order_by('-date')[:10]
    tasks = animal.tasks.all().order_by('due_date')
    
    context = {
        'animal': animal,
        'activities': activities,
        'tasks': tasks,
    }
    return render(request, 'farm/livestock_detail.html', context)


@login_required
def livestock_create(request):
    """Create new livestock"""
    if request.method == 'POST':
        form = LivestockForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.user = request.user
            animal.save()
            messages.success(request, 'Livestock added successfully!')
            return redirect('livestock_list')
    else:
        form = LivestockForm()
    return render(request, 'farm/livestock_form.html', {'form': form, 'title': 'Add New Livestock'})


@login_required
def livestock_update(request, pk):
    """Update livestock"""
    animal = get_object_or_404(Livestock, pk=pk, user=request.user)
    if request.method == 'POST':
        form = LivestockForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livestock updated successfully!')
            return redirect('livestock_detail', pk=pk)
    else:
        form = LivestockForm(instance=animal)
    return render(request, 'farm/livestock_form.html', {'form': form, 'title': 'Update Livestock'})


@login_required
def livestock_delete(request, pk):
    """Delete livestock"""
    animal = get_object_or_404(Livestock, pk=pk, user=request.user)
    if request.method == 'POST':
        animal.delete()
        messages.success(request, 'Livestock deleted successfully!')
        return redirect('livestock_list')
    return render(request, 'farm/livestock_confirm_delete.html', {'animal': animal})


# Inventory Views
@login_required
def inventory_list(request):
    """List all inventory items"""
    items = InventoryItem.objects.filter(user=request.user).order_by('name')
    category_filter = request.GET.get('category')
    low_stock = request.GET.get('low_stock')
    
    if category_filter:
        items = items.filter(category=category_filter)
    if low_stock:
        items = items.filter(quantity__lte=models.F('reorder_level'))
    
    context = {
        'items': items,
        'category_filter': category_filter,
        'low_stock': low_stock,
    }
    return render(request, 'farm/inventory_list.html', context)


@login_required
def inventory_detail(request, pk):
    """View inventory item details"""
    item = get_object_or_404(InventoryItem, pk=pk, user=request.user)
    return render(request, 'farm/inventory_detail.html', {'item': item})


@login_required
def inventory_create(request):
    """Create new inventory item"""
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Inventory item added successfully!')
            return redirect('inventory_list')
    else:
        form = InventoryItemForm()
    return render(request, 'farm/inventory_form.html', {'form': form, 'title': 'Add Inventory Item'})


@login_required
def inventory_update(request, pk):
    """Update inventory item"""
    item = get_object_or_404(InventoryItem, pk=pk, user=request.user)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item updated successfully!')
            return redirect('inventory_detail', pk=pk)
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'farm/inventory_form.html', {'form': form, 'title': 'Update Inventory Item'})


@login_required
def inventory_delete(request, pk):
    """Delete inventory item"""
    item = get_object_or_404(InventoryItem, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Inventory item deleted successfully!')
        return redirect('inventory_list')
    return render(request, 'farm/inventory_confirm_delete.html', {'item': item})


# Financial Views
@login_required
def finance_list(request):
    """List all financial transactions"""
    transactions = FinancialTransaction.objects.filter(user=request.user).order_by('-date')
    type_filter = request.GET.get('type')
    category_filter = request.GET.get('category')
    
    if type_filter:
        transactions = transactions.filter(type=type_filter)
    if category_filter:
        transactions = transactions.filter(category=category_filter)
    
    # Calculate totals
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net = total_income - total_expenses
    
    context = {
        'transactions': transactions,
        'type_filter': type_filter,
        'category_filter': category_filter,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net': net,
    }
    return render(request, 'farm/finance_list.html', context)


@login_required
def finance_create(request):
    """Create new financial transaction"""
    if request.method == 'POST':
        form = FinancialTransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('finance_list')
    else:
        form = FinancialTransactionForm()
    return render(request, 'farm/finance_form.html', {'form': form, 'title': 'Add Transaction'})


@login_required
def finance_update(request, pk):
    """Update financial transaction"""
    transaction = get_object_or_404(FinancialTransaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = FinancialTransactionForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('finance_list')
    else:
        form = FinancialTransactionForm(instance=transaction)
    return render(request, 'farm/finance_form.html', {'form': form, 'title': 'Update Transaction'})


@login_required
def finance_delete(request, pk):
    """Delete financial transaction"""
    transaction = get_object_or_404(FinancialTransaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('finance_list')
    return render(request, 'farm/finance_confirm_delete.html', {'transaction': transaction})


# Task Views
@login_required
def task_list(request):
    """List all tasks"""
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    return render(request, 'farm/task_list.html', context)


@login_required
def task_create(request):
    """Create new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
        form.fields['related_crop'].queryset = Crop.objects.filter(user=request.user)
        form.fields['related_livestock'].queryset = Livestock.objects.filter(user=request.user)
    return render(request, 'farm/task_form.html', {'form': form, 'title': 'Add New Task'})


@login_required
def task_update(request, pk):
    """Update task"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
        form.fields['related_crop'].queryset = Crop.objects.filter(user=request.user)
        form.fields['related_livestock'].queryset = Livestock.objects.filter(user=request.user)
    return render(request, 'farm/task_form.html', {'form': form, 'title': 'Update Task'})


@login_required
def task_delete(request, pk):
    """Delete task"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'farm/task_confirm_delete.html', {'task': task})


# Activity Views
@login_required
def activity_list(request):
    """List all activities"""
    activities = Activity.objects.filter(user=request.user).order_by('-date')
    type_filter = request.GET.get('type')
    
    if type_filter:
        activities = activities.filter(activity_type=type_filter)
    
    context = {
        'activities': activities,
        'type_filter': type_filter,
    }
    return render(request, 'farm/activity_list.html', context)


@login_required
def activity_create(request):
    """Create new activity"""
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            messages.success(request, 'Activity logged successfully!')
            return redirect('activity_list')
    else:
        form = ActivityForm()
        form.fields['related_crop'].queryset = Crop.objects.filter(user=request.user)
        form.fields['related_livestock'].queryset = Livestock.objects.filter(user=request.user)
    return render(request, 'farm/activity_form.html', {'form': form, 'title': 'Log New Activity'})


@login_required
def activity_update(request, pk):
    """Update activity"""
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('activity_list')
    else:
        form = ActivityForm(instance=activity)
        form.fields['related_crop'].queryset = Crop.objects.filter(user=request.user)
        form.fields['related_livestock'].queryset = Livestock.objects.filter(user=request.user)
    return render(request, 'farm/activity_form.html', {'form': form, 'title': 'Update Activity'})


@login_required
def activity_delete(request, pk):
    """Delete activity"""
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity deleted successfully!')
        return redirect('activity_list')
    return render(request, 'farm/activity_confirm_delete.html', {'activity': activity})


# Analytics View
@login_required
def analytics(request):
    """Analytics and reports view"""
    user = request.user
    
    # Crop statistics
    crop_stats = Crop.objects.filter(user=user).values('status').annotate(count=Count('id'))
    
    # Livestock statistics
    livestock_stats = Livestock.objects.filter(user=user).values('type').annotate(count=Count('id'))
    
    # Financial statistics (last 12 months)
    twelve_months_ago = timezone.now() - timedelta(days=365)
    monthly_income = FinancialTransaction.objects.filter(
        user=user, type='income', date__gte=twelve_months_ago
    ).values('date__month').annotate(total=Sum('amount')).order_by('date__month')
    
    monthly_expenses = FinancialTransaction.objects.filter(
        user=user, type='expense', date__gte=twelve_months_ago
    ).values('date__month').annotate(total=Sum('amount')).order_by('date__month')
    
    # Activity statistics
    activity_stats = Activity.objects.filter(user=user).values('activity_type').annotate(count=Count('id'))
    
    context = {
        'crop_stats': crop_stats,
        'livestock_stats': livestock_stats,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'activity_stats': activity_stats,
    }
    return render(request, 'farm/analytics.html', context)


# Profile View
@login_required
def profile(request):
    """User profile view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'farm/profile.html', context)


# Import models at the top to fix the reference
from django.db import models
