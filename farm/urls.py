from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.homepage, name='homepage'),
    
    # Authentication
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Crops
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/<int:pk>/', views.crop_detail, name='crop_detail'),
    path('crops/new/', views.crop_create, name='crop_create'),
    path('crops/<int:pk>/edit/', views.crop_update, name='crop_update'),
    path('crops/<int:pk>/delete/', views.crop_delete, name='crop_delete'),
    
    # Livestock
    path('livestock/', views.livestock_list, name='livestock_list'),
    path('livestock/<int:pk>/', views.livestock_detail, name='livestock_detail'),
    path('livestock/new/', views.livestock_create, name='livestock_create'),
    path('livestock/<int:pk>/edit/', views.livestock_update, name='livestock_update'),
    path('livestock/<int:pk>/delete/', views.livestock_delete, name='livestock_delete'),
    
    # Inventory
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/<int:pk>/', views.inventory_detail, name='inventory_detail'),
    path('inventory/new/', views.inventory_create, name='inventory_create'),
    path('inventory/<int:pk>/edit/', views.inventory_update, name='inventory_update'),
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),
    
    # Finance
    path('finance/', views.finance_list, name='finance_list'),
    path('finance/new/', views.finance_create, name='finance_create'),
    path('finance/<int:pk>/edit/', views.finance_update, name='finance_update'),
    path('finance/<int:pk>/delete/', views.finance_delete, name='finance_delete'),
    
    # Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    
    # Activities
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/new/', views.activity_create, name='activity_create'),
    path('activities/<int:pk>/edit/', views.activity_update, name='activity_update'),
    path('activities/<int:pk>/delete/', views.activity_delete, name='activity_delete'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
]
