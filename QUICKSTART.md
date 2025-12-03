# FarmFlow Quick Start Guide

## Prerequisites Check
- [ ] Python 3.8+ installed
- [ ] pip installed
- [ ] Administrator access (for virtual environment)

## Installation Steps

### 1. Open PowerShell in Project Directory
```powershell
cd "c:\Users\hp\Downloads\farmflow-suite-main(1)\farmflow-suite-main"
```

### 2. Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Note**: If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Required Packages
```powershell
pip install -r requirements.txt
```

### 4. Setup Database
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin Account
```powershell
python manage.py createsuperuser
```
Enter your desired username, email, and password when prompted.

### 6. Create Media Directories
```powershell
New-Item -ItemType Directory -Force -Path media
New-Item -ItemType Directory -Force -Path media\avatars
New-Item -ItemType Directory -Force -Path media\crops
New-Item -ItemType Directory -Force -Path media\livestock
New-Item -ItemType Directory -Force -Path media\activities
New-Item -ItemType Directory -Force -Path media\receipts
New-Item -ItemType Directory -Force -Path static
New-Item -ItemType Directory -Force -Path staticfiles
```

### 7. Start the Server
```powershell
python manage.py runserver
```

### 8. Access the Application
Open your browser and navigate to:
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## First Login

1. Click "Register Now" on the login page
2. Fill in your details:
   - Username
   - First Name and Last Name
   - Email
   - Password (confirm password)
3. Click Register
4. Login with your credentials
5. Complete your profile:
   - Navigate to Profile from the top menu
   - Add farm name, location, size
   - Select your role (Farmer, Manager, Worker, or Consultant)
   - Upload profile picture (optional)

## Quick Feature Tour

### Dashboard
- View overall statistics
- Check upcoming tasks
- Monitor financial summary
- See recent activities

### Add Your First Crop
1. Click "Crops" in sidebar
2. Click "Add New Crop"
3. Fill in details:
   - Crop name (e.g., "Corn")
   - Variety (e.g., "Sweet Corn")
   - Area in acres
   - Planting date
   - Expected harvest date
   - Status (e.g., "Planted")
4. Click "Save Crop"

### Add Livestock
1. Click "Livestock" in sidebar
2. Click "Add New Animal"
3. Enter details:
   - Type (Cattle, Poultry, etc.)
   - Breed
   - Unique tag number
   - Date acquired
   - Gender and status
4. Click "Save"

### Track Inventory
1. Click "Inventory" in sidebar
2. Click "Add Item"
3. Record:
   - Item name (e.g., "Fertilizer - NPK")
   - Category (Fertilizers)
   - Quantity and unit
   - Reorder level (for low stock alerts)
   - Cost per unit
5. Click "Save"

### Record Financial Transaction
1. Click "Finance" in sidebar
2. Click "Add Transaction"
3. Choose:
   - Type (Income or Expense)
   - Category
   - Amount
   - Date
   - Description
4. Upload receipt (optional)
5. Click "Save"

### Create a Task
1. Click "Tasks" in sidebar
2. Click "Add Task"
3. Enter:
   - Task title
   - Description
   - Priority level
   - Due date
   - Assign to (optional)
4. Click "Save"

### Log an Activity
1. Click "Activities" in sidebar
2. Click "Log New Activity"
3. Select:
   - Activity type (Planting, Irrigation, etc.)
   - Title and description
   - Date and time
   - Duration in minutes
   - Related crop or livestock (optional)
4. Click "Save"

## Common Commands

### Stop the Server
Press `Ctrl + C` in the terminal

### Restart the Server
```powershell
python manage.py runserver
```

### Create Database Backup
```powershell
Copy-Item db.sqlite3 "db_backup_$(Get-Date -Format 'yyyy-MM-dd').sqlite3"
```

### Deactivate Virtual Environment
```powershell
deactivate
```

## Tips for Best Use

1. **Regular Backups**: Backup your database weekly
2. **Consistent Logging**: Log activities daily for accurate records
3. **Set Reorder Levels**: Configure inventory reorder levels to get low stock alerts
4. **Use Tasks**: Create tasks for upcoming farm activities
5. **Review Analytics**: Check analytics weekly to track performance
6. **Team Collaboration**: Add team members with appropriate roles
7. **Upload Images**: Add photos to crops and livestock for better tracking
8. **Financial Tracking**: Record all transactions immediately

## Troubleshooting

### Can't Activate Virtual Environment
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Database Locked Error
- Close all browser tabs
- Stop the server (Ctrl+C)
- Restart the server

### Static Files Not Loading
```powershell
python manage.py collectstatic
```

### Forgot Admin Password
```powershell
python manage.py changepassword <username>
```

### Module Not Found Error
```powershell
pip install -r requirements.txt
```

## Support

For issues or questions:
1. Check this guide
2. Review README.md
3. Check Django documentation: https://docs.djangoproject.com/
4. Examine error messages in terminal

## Next Steps

After completing setup:
1. ✅ Create your profile
2. ✅ Add your first crop
3. ✅ Record an inventory item
4. ✅ Log today's activities
5. ✅ Set up tasks for the week
6. ✅ Invite team members

Enjoy using FarmFlow to manage your farm efficiently!
