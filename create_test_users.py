#!/usr/bin/env python
"""
Script to create test users for different roles in FarmFlow
Run this with: python manage.py shell < create_test_users.py
"""

from django.contrib.auth.models import User
from farm.models import UserProfile

# Test user data
test_users = [
    {
        'username': 'farmer_john',
        'email': 'farmer@farmflow.com',
        'password': 'farmer123',
        'first_name': 'John',
        'last_name': 'Farmer',
        'role': 'farmer',
        'phone': '+254700123456',
        'farm_name': "John's Green Farm",
        'location': 'Nakuru, Kenya',
        'farm_size': 25.5
    },
    {
        'username': 'manager_mary',
        'email': 'manager@farmflow.com',
        'password': 'manager123',
        'first_name': 'Mary',
        'last_name': 'Manager',
        'role': 'manager',
        'phone': '+254700234567',
        'farm_name': 'FarmFlow Operations',
        'location': 'Eldoret, Kenya',
        'farm_size': 50.0
    },
    {
        'username': 'worker_peter',
        'email': 'worker@farmflow.com',
        'password': 'worker123',
        'first_name': 'Peter',
        'last_name': 'Worker',
        'role': 'worker',
        'phone': '+254700345678',
        'farm_name': '',
        'location': 'Kisumu, Kenya',
        'farm_size': 0
    },
    {
        'username': 'consultant_sarah',
        'email': 'consultant@farmflow.com',
        'password': 'consultant123',
        'first_name': 'Sarah',
        'last_name': 'Consultant',
        'role': 'consultant',
        'phone': '+254700456789',
        'farm_name': 'AgriConsult Services',
        'location': 'Nairobi, Kenya',
        'farm_size': 0
    },
    {
        'username': 'admin',
        'email': 'admin@farmflow.com',
        'password': 'admin123',
        'first_name': 'Admin',
        'last_name': 'User',
        'role': 'manager',
        'phone': '+254700567890',
        'farm_name': 'FarmFlow HQ',
        'location': 'Nairobi, Kenya',
        'farm_size': 100.0,
        'is_staff': True,
        'is_superuser': True
    }
]

print("Creating test users for FarmFlow...")
print("-" * 50)

for user_data in test_users:
    username = user_data['username']
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"[SKIP] User '{username}' already exists. Skipping...")
        continue
    
    # Create user
    user = User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name']
    )
    
    # Set staff/superuser status if specified
    if user_data.get('is_staff'):
        user.is_staff = True
    if user_data.get('is_superuser'):
        user.is_superuser = True
    user.save()
    
    # Create or update user profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.role = user_data['role']
    profile.phone = user_data['phone']
    profile.farm_name = user_data['farm_name']
    profile.location = user_data['location']
    profile.farm_size = user_data['farm_size']
    profile.save()
    
    print(f"[SUCCESS] Created user: {username}")
    print(f"   Email: {user_data['email']}")
    print(f"   Password: {user_data['password']}")
    print(f"   Role: {user_data['role']}")
    print(f"   Name: {user_data['first_name']} {user_data['last_name']}")
    if user_data.get('is_staff'):
        print(f"   Status: Staff/Admin")
    print()

print("-" * 50)
print("Test users created successfully!")
print("\nYou can now log in with these credentials:")
print("\nTEST USER CREDENTIALS:")
print("-" * 50)
print("FARMER:")
print("  Username: farmer_john")
print("  Email: farmer@farmflow.com")
print("  Password: farmer123")
print()
print("MANAGER:")
print("  Username: manager_mary")
print("  Email: manager@farmflow.com")
print("  Password: manager123")
print()
print("WORKER:")
print("  Username: worker_peter")
print("  Email: worker@farmflow.com")
print("  Password: worker123")
print()
print("CONSULTANT:")
print("  Username: consultant_sarah")
print("  Email: consultant@farmflow.com")
print("  Password: consultant123")
print()
print("ADMIN:")
print("  Username: admin")
print("  Email: admin@farmflow.com")
print("  Password: admin123")
print("-" * 50)
