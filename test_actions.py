"""
Test script to verify admin dashboard action functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmflow.settings')
django.setup()

from django.contrib.auth.models import User
from farm.models import UserProfile

print("=" * 60)
print("ADMIN DASHBOARD ACTIONS - VERIFICATION TEST")
print("=" * 60)

# Check if admin dashboard view exists
try:
    from farm.views import (
        admin_dashboard, 
        admin_users, 
        admin_user_detail, 
        admin_user_delete,
        admin_export_data
    )
    print("\n✓ All admin views imported successfully")
except ImportError as e:
    print(f"\n✗ Error importing views: {e}")

# Check URL patterns
try:
    from django.urls import reverse
    urls_to_test = [
        ('admin_dashboard', {}),
        ('admin_users', {}),
        ('admin_user_detail', {'user_id': 1}),
        ('admin_user_delete', {'user_id': 1}),
        ('admin_export_data', {}),
    ]
    
    print("\n✓ Testing URL patterns:")
    for url_name, kwargs in urls_to_test:
        try:
            url = reverse(url_name, kwargs=kwargs)
            print(f"  ✓ {url_name}: {url}")
        except Exception as e:
            print(f"  ✗ {url_name}: {e}")
except Exception as e:
    print(f"\n✗ Error testing URLs: {e}")

# Check if superuser exists
try:
    superusers = User.objects.filter(is_superuser=True)
    print(f"\n✓ Found {superusers.count()} superuser(s):")
    for su in superusers:
        profile = UserProfile.objects.filter(user=su).first()
        role = profile.get_role_display() if profile else "No Profile"
        print(f"  - {su.username} (Role: {role}, Active: {su.is_active})")
except Exception as e:
    print(f"\n✗ Error checking superusers: {e}")

# Check regular users
try:
    regular_users = User.objects.filter(is_superuser=False)
    print(f"\n✓ Found {regular_users.count()} regular user(s):")
    for user in regular_users[:5]:  # Show first 5
        profile = UserProfile.objects.filter(user=user).first()
        role = profile.get_role_display() if profile else "No Profile"
        print(f"  - {user.username} (Role: {role}, Active: {user.is_active})")
except Exception as e:
    print(f"\n✗ Error checking users: {e}")

# Check if templates exist
import os
from django.conf import settings

print("\n✓ Checking template files:")
templates_to_check = [
    'farm/admin_dashboard.html',
    'farm/admin_users.html',
    'farm/admin_user_detail.html',
]

for template in templates_to_check:
    template_path = os.path.join(settings.BASE_DIR, 'templates', template)
    if os.path.exists(template_path):
        print(f"  ✓ {template}")
    else:
        print(f"  ✗ {template} - NOT FOUND")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
All action buttons should work as follows:

1. VIEW BUTTON (Eye Icon):
   - Redirects to /admin/user/{id}/
   - Shows user details, crops, livestock, transactions
   
2. EDIT BUTTON (Pencil Icon):
   - Redirects to /admin/user/{id}/
   - Same as view but with editable form
   - Can change user's role
   
3. DELETE BUTTON (Trash Icon):
   - AJAX POST to /admin/user/{id}/delete/
   - Shows confirmation dialog
   - Cannot delete superusers
   - Reloads page on success
   
4. EXPORT DATA BUTTON:
   - Downloads CSV file with all system data
   - URL: /admin/export/all/

TO TEST:
1. Login as superuser (allan or admin)
2. Go to /admin-dashboard/
3. Click "Users" tab
4. Try each action button
""")
print("=" * 60)
