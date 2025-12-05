from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
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


# Custom decorator for superuser-only access
def superuser_required(view_func):
    """Decorator that requires user to be a superuser"""
    decorated_view = user_passes_test(
        lambda u: u.is_superuser,
        login_url='/login/'
    )(view_func)
    return login_required(decorated_view)


def homepage(request):
    """Homepage view"""
    return render(request, 'farm/homepage.html')


def features_page(request):
    """Features page view"""
    return render(request, 'farm/features_page.html')


def about_page(request):
    """About page view"""
    return render(request, 'farm/about_page.html')


def pricing_page(request):
    """Pricing page view"""
    return render(request, 'farm/pricing_page.html')


def contact_page(request):
    """Contact page view"""
    return render(request, 'farm/contact_page.html')


def tutorial_page(request):
    """Tutorial page view"""
    return render(request, 'farm/tutorial_page.html')


def billing(request):
    """Billing page view"""
    return render(request, 'farm/billing.html')


def process_payment(request):
    """Process payment (placeholder for payment gateway integration)"""
    if request.method == 'POST':
        # Here you would integrate with M-Pesa, Airtel Money, or card payment gateway
        plan = request.POST.get('plan')
        cycle = request.POST.get('cycle')
        payment_method = request.POST.get('payment_method')
        
        messages.success(request, 'Payment processing initiated. You will receive a confirmation shortly.')
        return redirect('register')
    
    return redirect('billing')


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
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Try to get user by email
        try:
            from django.contrib.auth.models import User
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'farm/login.html')


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    """Role-based dashboard router"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Route to appropriate dashboard based on role
    if profile.role == 'farmer':
        return farmer_dashboard(request)
    elif profile.role == 'manager':
        return manager_dashboard(request)
    elif profile.role == 'worker':
        return worker_dashboard(request)
    elif profile.role == 'consultant':
        return consultant_dashboard(request)
    else:
        # Default to farmer dashboard
        return farmer_dashboard(request)


@login_required
def farmer_dashboard(request):
    """Farmer-specific dashboard"""
    user = request.user
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Statistics
    total_crops = Crop.objects.filter(user=user).count()
    active_crops = Crop.objects.filter(user=user, status__in=['planted', 'growing']).count()
    total_livestock = Livestock.objects.filter(user=user).exclude(status__in=['sold', 'deceased']).count()
    
    # Financial statistics - Get all income and expenses (not just this month for total view)
    income = FinancialTransaction.objects.filter(
        user=user, type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expenses = FinancialTransaction.objects.filter(
        user=user, type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # This month's income and expenses
    income_this_month = FinancialTransaction.objects.filter(
        user=user, type='income', date__gte=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expenses_this_month = FinancialTransaction.objects.filter(
        user=user, type='expense', date__gte=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    net_income = income - expenses
    net_income_this_month = income_this_month - expenses_this_month
    
    # Tasks
    pending_tasks = Task.objects.filter(user=user, status__in=['pending', 'in_progress']).count()
    overdue_tasks = Task.objects.filter(
        user=user, status__in=['pending', 'in_progress'],
        due_date__lt=timezone.now().date()
    ).count()
    upcoming_tasks = Task.objects.filter(
        user=user, status__in=['pending', 'in_progress']
    ).order_by('due_date')[:5]
    
    # Inventory
    low_stock_items = InventoryItem.objects.filter(user=user, quantity__lte=models.F('reorder_level')).count()
    
    # Recent data
    recent_crops = Crop.objects.filter(user=user, status__in=['planted', 'growing']).order_by('-planting_date')[:5]
    recent_livestock = Livestock.objects.filter(user=user).exclude(status__in=['sold', 'deceased']).order_by('-date_acquired')[:5]
    recent_activities = Activity.objects.filter(user=user).order_by('-date')[:5]
    recent_transactions = FinancialTransaction.objects.filter(user=user).order_by('-date')[:10]
    
    context = {
        'total_crops': total_crops,
        'active_crops': active_crops,
        'total_livestock': total_livestock,
        'income': income,
        'expenses': expenses,
        'net_income': net_income,
        'income_this_month': income_this_month,
        'expenses_this_month': expenses_this_month,
        'net_income_this_month': net_income_this_month,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'low_stock_items': low_stock_items,
        'upcoming_tasks': upcoming_tasks,
        'recent_crops': recent_crops,
        'recent_livestock': recent_livestock,
        'recent_activities': recent_activities,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'farm/farmer_dashboard.html', context)


@login_required
def manager_dashboard(request):
    """Manager-specific dashboard with team and resource management"""
    from django.contrib.auth.models import User
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month = (current_month - timedelta(days=1)).replace(day=1)
    
    # Overall statistics (all users)
    total_crops = Crop.objects.count()
    active_crops = Crop.objects.filter(status__in=['planted', 'growing']).count()
    total_livestock = Livestock.objects.exclude(status__in=['sold', 'deceased']).count()
    healthy_livestock = Livestock.objects.filter(status='healthy').count()
    
    # Financial statistics - Total (all time)
    income = FinancialTransaction.objects.filter(
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expenses = FinancialTransaction.objects.filter(
        type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    net_income = income - expenses
    
    # This month's income for comparison
    income_this_month = FinancialTransaction.objects.filter(
        type='income', date__gte=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    last_month_income = FinancialTransaction.objects.filter(
        type='income', date__gte=last_month, date__lt=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Tasks
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status__in=['pending']).count()
    inprogress_tasks = Task.objects.filter(status='in_progress').count()
    completed_tasks = Task.objects.filter(status='completed').count()
    overdue_tasks = Task.objects.filter(
        status__in=['pending', 'in_progress'],
        due_date__lt=timezone.now().date()
    ).count()
    all_tasks = Task.objects.select_related('assigned_to', 'user').order_by('-due_date')[:20]
    
    # Inventory
    low_stock_items = InventoryItem.objects.filter(quantity__lte=models.F('reorder_level')).count()
    inventory_items = InventoryItem.objects.all()[:20]
    low_stock_list = InventoryItem.objects.filter(quantity__lte=models.F('reorder_level'))[:10]
    
    # Team
    team_members = User.objects.filter(is_active=True).select_related('profile')
    
    # Recent data
    upcoming_harvests = Crop.objects.filter(
        status__in=['planted', 'growing'],
        expected_harvest_date__lte=timezone.now().date() + timedelta(days=30)
    ).order_by('expected_harvest_date')[:10]
    recent_activities = Activity.objects.select_related('user').order_by('-date')[:15]
    
    # Performance data
    harvested_crops = Crop.objects.filter(status__in=['harvested', 'sold']).exclude(
        actual_yield__isnull=True, expected_yield__isnull=True
    )[:10]
    
    context = {
        'total_crops': total_crops,
        'active_crops': active_crops,
        'total_livestock': total_livestock,
        'healthy_livestock': healthy_livestock,
        'income': income,
        'expenses': expenses,
        'net_income': net_income,
        'last_month_income': last_month_income,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'inprogress_tasks': inprogress_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'all_tasks': all_tasks,
        'low_stock_items': low_stock_items,
        'inventory_items': inventory_items,
        'low_stock_list': low_stock_list,
        'team_members': team_members,
        'upcoming_harvests': upcoming_harvests,
        'recent_activities': recent_activities,
        'harvested_crops': harvested_crops,
    }
    
    return render(request, 'farm/manager_dashboard.html', context)


@login_required
def worker_dashboard(request):
    """Worker-specific dashboard focused on assigned tasks"""
    user = request.user
    current_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
    current_month = timezone.now().replace(day=1)
    today = timezone.now().date()
    
    # Task statistics
    total_my_tasks = Task.objects.filter(assigned_to=user).count()
    today_tasks = Task.objects.filter(assigned_to=user, due_date=today).count()
    pending_tasks = Task.objects.filter(assigned_to=user, status='pending').count()
    completed_tasks = Task.objects.filter(assigned_to=user, status='completed', completed_date__gte=current_week).count()
    overdue_tasks = Task.objects.filter(
        assigned_to=user, status__in=['pending', 'in_progress'],
        due_date__lt=today
    ).count()
    
    # Task priority breakdown
    urgent_tasks = Task.objects.filter(assigned_to=user, status__in=['pending', 'in_progress'], priority='urgent').count()
    high_tasks = Task.objects.filter(assigned_to=user, status__in=['pending', 'in_progress'], priority='high').count()
    medium_tasks = Task.objects.filter(assigned_to=user, status__in=['pending', 'in_progress'], priority='medium').count()
    low_tasks = Task.objects.filter(assigned_to=user, status__in=['pending', 'in_progress'], priority='low').count()
    
    # Activities
    my_activities = Activity.objects.filter(user=user, date__gte=current_month).count()
    recent_activities = Activity.objects.filter(user=user).order_by('-date')[:10]
    
    # Assigned tasks
    assigned_tasks = Task.objects.filter(assigned_to=user).exclude(status='completed').order_by('-priority', 'due_date')
    
    context = {
        'total_my_tasks': total_my_tasks,
        'today_tasks': today_tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'urgent_tasks': urgent_tasks,
        'high_tasks': high_tasks,
        'medium_tasks': medium_tasks,
        'low_tasks': low_tasks,
        'my_activities': my_activities,
        'recent_activities': recent_activities,
        'assigned_tasks': assigned_tasks,
    }
    
    return render(request, 'farm/worker_dashboard.html', context)


@login_required
def consultant_dashboard(request):
    """Consultant-specific dashboard with analytics and recommendations"""
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month = (current_month - timedelta(days=1)).replace(day=1)
    
    # Overall statistics
    total_crops = Crop.objects.count()
    active_crops = Crop.objects.filter(status__in=['planted', 'growing']).count()
    total_livestock = Livestock.objects.exclude(status__in=['sold', 'deceased']).count()
    healthy_livestock = Livestock.objects.filter(status='healthy').count()
    sick_livestock = Livestock.objects.filter(status__in=['sick', 'under_treatment']).count()
    
    # Financial statistics - Total (all time)
    income = FinancialTransaction.objects.filter(
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expenses = FinancialTransaction.objects.filter(
        type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    net_income = income - expenses
    profitability_ratio = (net_income / income * 100) if income > 0 else 0
    
    # Crop performance
    harvested_crops = Crop.objects.filter(status__in=['harvested', 'sold'])
    crops_with_yield = harvested_crops.exclude(actual_yield__isnull=True, expected_yield__isnull=True)
    
    # Calculate average performance
    total_performance = 0
    performance_count = 0
    low_performing_crops = 0
    
    for crop in crops_with_yield:
        if crop.expected_yield and crop.actual_yield:
            performance = (crop.actual_yield / crop.expected_yield) * 100
            total_performance += performance
            performance_count += 1
            if performance < 70:
                low_performing_crops += 1
    
    avg_crop_performance = int(total_performance / performance_count) if performance_count > 0 else 0
    
    # Upcoming harvests
    upcoming_harvests = Crop.objects.filter(
        status__in=['planted', 'growing'],
        expected_harvest_date__lte=timezone.now().date() + timedelta(days=30)
    ).order_by('expected_harvest_date')[:10]
    
    # Crop status counts
    planted_crops = Crop.objects.filter(status='planted').count()
    growing_crops = Crop.objects.filter(status='growing').count()
    ready_crops = Crop.objects.filter(
        status='growing',
        expected_harvest_date__lte=timezone.now().date()
    ).count()
    harvested_crops_count = Crop.objects.filter(status='harvested').count()
    
    # Livestock data
    all_livestock = Livestock.objects.exclude(status__in=['sold', 'deceased'])
    sick_or_treatment_livestock = Livestock.objects.filter(status__in=['sick', 'under_treatment'])
    livestock_by_type = Livestock.objects.values('type').annotate(count=Count('type'))
    
    # Financial breakdown
    expense_by_category = FinancialTransaction.objects.filter(
        type='expense', date__gte=current_month
    ).values('category').annotate(total=Sum('amount')).order_by('-total')[:10]
    
    # Recent data
    recent_activities = Activity.objects.select_related('user').order_by('-date')[:15]
    
    context = {
        'total_crops': total_crops,
        'active_crops': active_crops,
        'total_livestock': total_livestock,
        'healthy_livestock': healthy_livestock,
        'sick_livestock': sick_livestock,
        'income': income,
        'expenses': expenses,
        'net_income': net_income,
        'profitability_ratio': profitability_ratio,
        'avg_crop_performance': avg_crop_performance,
        'low_performing_crops': low_performing_crops,
        'crops_with_yield': crops_with_yield,
        'upcoming_harvests': upcoming_harvests,
        'planted_crops': planted_crops,
        'growing_crops': growing_crops,
        'ready_crops': ready_crops,
        'harvested_crops': harvested_crops_count,
        'all_livestock': all_livestock,
        'sick_or_treatment_livestock': sick_or_treatment_livestock,
        'livestock_by_type': livestock_by_type,
        'expense_by_category': expense_by_category,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'farm/consultant_dashboard.html', context)


# Crop Views
def crop_list(request):
    """List all crops or show info page"""
    if not request.user.is_authenticated:
        return render(request, 'farm/crop_info.html')
    
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
def livestock_list(request):
    """List all livestock or show info page"""
    if not request.user.is_authenticated:
        return render(request, 'farm/livestock_info.html')
    
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
def inventory_list(request):
    """List all inventory items or show info page"""
    if not request.user.is_authenticated:
        return render(request, 'farm/inventory_info.html')
    
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
def finance_list(request):
    """List all financial transactions or show info page"""
    if not request.user.is_authenticated:
        return render(request, 'farm/finance_info.html')
    
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
def task_list(request):
    """List all tasks or show info page"""
    if not request.user.is_authenticated:
        return render(request, 'farm/task_info.html')
    
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
    """Analytics and reports view or show info page"""
    if not request.user.is_authenticated:
        return render(request, 'farm/analytics_info.html')
    
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


# Admin Views
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q
import json
from datetime import datetime, timedelta

@superuser_required
def admin_dashboard(request):
    """Main admin dashboard with overview statistics"""
    from django.utils import timezone
    
    # Get all statistics
    total_users = User.objects.count()
    total_crops = Crop.objects.count()
    total_livestock = Livestock.objects.count()
    total_revenue = FinancialTransaction.objects.filter(type='income').aggregate(
        total=Sum('amount'))['total'] or 0
    
    # Recent users
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Activity log
    recent_activities = Activity.objects.select_related('user').order_by('-date')[:20]
    
    # Monthly statistics
    current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0)
    new_users_this_month = User.objects.filter(date_joined__gte=current_month_start).count()
    active_users_today = User.objects.filter(last_login__date=timezone.now().date()).count()
    transactions_this_month = FinancialTransaction.objects.filter(
        date__gte=current_month_start).count()
    
    # Calculate growth rate
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    last_month_users = User.objects.filter(
        date_joined__gte=last_month_start,
        date_joined__lt=current_month_start
    ).count()
    growth_rate = 0
    if last_month_users > 0:
        growth_rate = ((new_users_this_month - last_month_users) / last_month_users) * 100
    
    context = {
        'total_users': total_users,
        'total_crops': total_crops,
        'total_livestock': total_livestock,
        'total_revenue': total_revenue,
        'recent_users': recent_users,
        'recent_activities': recent_activities,
        'new_users_this_month': new_users_this_month,
        'active_users_today': active_users_today,
        'transactions_this_month': transactions_this_month,
        'growth_rate': round(growth_rate, 1),
    }
    return render(request, 'farm/admin_dashboard.html', context)

@superuser_required
def admin_users(request):
    """Manage all users"""
    users = User.objects.all().order_by('-date_joined')
    context = {'users': users}
    return render(request, 'farm/admin_users.html', context)

@superuser_required
def admin_user_detail(request, user_id):
    """View and edit user details including role"""
    from .forms import AdminUserProfileForm
    
    user = get_object_or_404(User, id=user_id)
    profile = UserProfile.objects.get_or_create(user=user)[0]
    
    if request.method == 'POST':
        form = AdminUserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} profile updated successfully!')
            return redirect('admin_user_detail', user_id=user_id)
    else:
        form = AdminUserProfileForm(instance=profile)
    
    user_crops = Crop.objects.filter(user=user)
    user_livestock = Livestock.objects.filter(user=user)
    user_transactions = FinancialTransaction.objects.filter(user=user)[:20]
    
    context = {
        'view_user': user,
        'profile': profile,
        'form': form,
        'user_crops': user_crops,
        'user_livestock': user_livestock,
        'user_transactions': user_transactions,
    }
    return render(request, 'farm/admin_user_detail.html', context)

@superuser_required
def admin_user_delete(request, user_id):
    """Delete a user"""
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.is_superuser:
            return JsonResponse({'success': False, 'message': 'Cannot delete superuser'})
        user.delete()
        return JsonResponse({'success': True, 'message': 'User deleted successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@superuser_required
def admin_crops(request):
    """Manage all crops"""
    crops = Crop.objects.all().select_related('user').order_by('-planting_date')
    context = {'crops': crops}
    return render(request, 'farm/admin_crops.html', context)

@superuser_required
def admin_livestock(request):
    """Manage all livestock"""
    livestock = Livestock.objects.all().select_related('user').order_by('-acquisition_date')
    context = {'livestock': livestock}
    return render(request, 'farm/admin_livestock.html', context)

@superuser_required
def admin_finance(request):
    """Finance overview for all users"""
    transactions = FinancialTransaction.objects.all().select_related('user').order_by('-date')[:100]
    total_income = FinancialTransaction.objects.filter(type='income').aggregate(
        total=Sum('amount'))['total'] or 0
    total_expenses = FinancialTransaction.objects.filter(type='expense').aggregate(
        total=Sum('amount'))['total'] or 0
    
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_total': total_income - total_expenses,
    }
    return render(request, 'farm/admin_finance.html', context)

@superuser_required
def admin_reports(request):
    """Generate system-wide reports"""
    context = {}
    return render(request, 'farm/admin_reports.html', context)

@superuser_required
def admin_settings(request):
    """System settings management"""
    context = {}
    return render(request, 'farm/admin_settings.html', context)

@superuser_required
def admin_backup(request):
    """Backup and restore functionality"""
    context = {}
    return render(request, 'farm/admin_backup.html', context)

@superuser_required
def admin_export_data(request):
    """Export all system data"""
    import csv
    from datetime import datetime
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="farmflow_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Export Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow([])
    
    # Export Users
    writer.writerow(['=== USERS ==='])
    writer.writerow(['ID', 'Username', 'Email', 'Role', 'Farm Name', 'Date Joined'])
    for user in User.objects.all():
        profile = UserProfile.objects.filter(user=user).first()
        writer.writerow([
            user.id,
            user.username,
            user.email,
            profile.get_role_display() if profile else 'N/A',
            profile.farm_name if profile else 'N/A',
            user.date_joined.strftime('%Y-%m-%d')
        ])
    
    writer.writerow([])
    writer.writerow(['=== CROPS ==='])
    writer.writerow(['ID', 'User', 'Name', 'Variety', 'Area', 'Status', 'Planting Date'])
    for crop in Crop.objects.all():
        writer.writerow([
            crop.id,
            crop.user.username,
            crop.name,
            crop.variety,
            crop.area,
            crop.get_status_display(),
            crop.planting_date.strftime('%Y-%m-%d')
        ])
    
    writer.writerow([])
    writer.writerow(['=== LIVESTOCK ==='])
    writer.writerow(['ID', 'User', 'Type', 'Breed', 'Tag', 'Status', 'Date Acquired'])
    for animal in Livestock.objects.all():
        writer.writerow([
            animal.id,
            animal.user.username,
            animal.get_type_display(),
            animal.breed,
            animal.tag_number,
            animal.get_status_display(),
            animal.date_acquired.strftime('%Y-%m-%d')
        ])
    
    writer.writerow([])
    writer.writerow(['=== FINANCIAL TRANSACTIONS ==='])
    writer.writerow(['ID', 'User', 'Type', 'Category', 'Amount', 'Description', 'Date'])
    for trans in FinancialTransaction.objects.all():
        writer.writerow([
            trans.id,
            trans.user.username,
            trans.get_type_display(),
            trans.get_category_display(),
            trans.amount,
            trans.description,
            trans.date.strftime('%Y-%m-%d')
        ])
    
    return response

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
