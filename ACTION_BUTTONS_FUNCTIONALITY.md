# Admin Dashboard Action Buttons Functionality

## Overview
This document describes all the action button functionalities implemented in the admin dashboard and how they work.

## Implemented Features

### 1. **Admin Dashboard** (`/admin-dashboard/`)

#### User Management Actions
Located in the "Users" tab of the admin dashboard.

**View Button (Eye Icon)**
- **URL Pattern**: `/admin/user/{user_id}/`
- **Function**: `viewUser(userId)`
- **Action**: Redirects to the user detail page where you can:
  - View complete user information
  - See user's role, farm details, and status
  - View user's crops, livestock, and transactions
  - Edit user profile and change role
  - Delete user (if not a superuser)

**Edit Button (Pencil Icon)**
- **URL Pattern**: `/admin/user/{user_id}/`
- **Function**: `editUser(userId)`
- **Action**: Same as View button - redirects to user detail page for editing
- **Features**:
  - Edit user profile information (phone, farm name, location, farm size)
  - Change user's role (Farmer, Manager, Worker, Consultant)
  - Upload/update avatar

**Delete Button (Trash Icon)**
- **URL Pattern**: `/admin/user/{user_id}/delete/`
- **Function**: `deleteUser(userId)`
- **Method**: POST (AJAX request)
- **Action**: Deletes user after confirmation
- **Security**:
  - Shows confirmation dialog
  - Cannot delete superuser accounts
  - Uses CSRF token for security
  - Returns JSON response with success/error message
  - Automatically reloads page on success

#### Quick Actions
Located in the "Quick Actions" section.

1. **Django Admin** - Links to Django's built-in admin panel (`/admin/`)
2. **Manage Users** - Links to full user management page (`/admin/users/`)
3. **Manage Crops** - Links to crops management (`/admin/crops/`)
4. **Manage Livestock** - Links to livestock management (`/admin/livestock/`)
5. **Finance Overview** - Links to financial overview (`/admin/finance/`)
6. **Generate Reports** - Links to reports page (`/admin/reports/`)
7. **System Settings** - Links to settings page (`/admin/settings/`)
8. **Backup & Restore** - Links to backup page (`/admin/backup/`)

#### Export Data Button
- **URL Pattern**: `/admin/export/all/`
- **Function**: `exportSystemData()`
- **Action**: Downloads a CSV file containing all system data
- **Exported Data**:
  - All users with their profiles and roles
  - All crops with details
  - All livestock records
  - All financial transactions
- **File Format**: CSV (farmflow_export.csv)

### 2. **User Detail Page** (`/admin/user/{user_id}/`)

#### Features Available:
1. **Profile Editing**
   - Update user's phone, farm name, location, farm size
   - Change user's role (admin-only)
   - Upload/change avatar image

2. **View User's Data**
   - Recent crops planted
   - Livestock owned
   - Financial transactions (last 20)

3. **Delete User** (Danger Zone)
   - Red delete button in the sidebar
   - Shows confirmation dialog
   - Cannot delete superuser accounts
   - Redirects to users list after successful deletion

### 3. **Users List Page** (`/admin/users/`)

#### Features:
- View all system users in a table
- Displays: Username, Full Name, Email, Role, Farm Name, Status, Join Date
- **Edit Button** for each user - redirects to user detail page

## Technical Implementation

### CSRF Protection
All POST requests (especially delete operations) are protected with CSRF tokens:
- CSRF token added as meta tag in base.html: `<meta name="csrf-token" content="{{ csrf_token }}">`
- JavaScript functions retrieve token from meta tag or cookie
- Token included in all AJAX requests

### JavaScript Functions

```javascript
// Navigate to user detail/edit page
function viewUser(userId) {
    window.location.href = `/admin/user/${userId}/`;
}

// Same as viewUser (edit page = detail page)
function editUser(userId) {
    window.location.href = `/admin/user/${userId}/`;
}

// Delete user with AJAX
function deleteUser(userId) {
    if (confirm('Are you sure...')) {
        fetch(`/admin/user/${userId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('User deleted successfully!');
                location.reload();
            }
        });
    }
}

// Export all system data
function exportSystemData() {
    window.location.href = '/admin/export/all/';
}
```

### Django Views

```python
@superuser_required
def admin_user_detail(request, user_id):
    """View and edit user details including role"""
    # Handles both GET (view) and POST (edit) requests
    # Uses AdminUserProfileForm which includes role field

@superuser_required
def admin_user_delete(request, user_id):
    """Delete a user"""
    # POST only
    # Returns JSON: {'success': True/False, 'message': '...'}
    # Prevents deletion of superuser accounts

@superuser_required
def admin_export_data(request):
    """Export all system data"""
    # Generates CSV file with all users, crops, livestock, transactions
```

### URL Patterns
```python
path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
path('admin/users/', views.admin_users, name='admin_users'),
path('admin/user/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
path('admin/user/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
path('admin/export/all/', views.admin_export_data, name='admin_export_data'),
```

## Security Features

1. **Superuser-Only Access**: All admin functions require superuser status (`@superuser_required` decorator)
2. **CSRF Protection**: All POST/DELETE operations protected with CSRF tokens
3. **Cannot Delete Superusers**: System prevents deletion of superuser accounts
4. **Confirmation Dialogs**: User must confirm destructive actions
5. **Login Required**: All admin pages require authentication

## Testing the Actions

### To Test View Button:
1. Go to Admin Dashboard (`/admin-dashboard/`)
2. Click "Users" tab
3. Click eye icon (View) on any user
4. Should redirect to user detail page showing all user information

### To Test Edit Button:
1. Go to Admin Dashboard
2. Click "Users" tab
3. Click pencil icon (Edit) on any user
4. Should redirect to user detail page
5. Modify any field (e.g., role, phone, farm name)
6. Click "Update Profile & Role" button
7. Should show success message

### To Test Delete Button:
1. Go to Admin Dashboard
2. Click "Users" tab
3. Click trash icon (Delete) on a non-superuser
4. Confirm deletion in dialog
5. User should be deleted and page reloads

### To Test Export Data:
1. Go to Admin Dashboard
2. Click "Export All Data" button (top right)
3. CSV file should download automatically

## Notes

- All admin actions require you to be logged in as a superuser (like 'allan' or 'admin' account)
- Regular users with roles (farmer, manager, worker, consultant) cannot access these features
- The Admin Panel only appears in the sidebar for superuser accounts
- All action buttons use smooth transitions and hover effects for better UX
