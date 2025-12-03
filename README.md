# FarmFlow - Farm Management System

## Overview

FarmFlow is a comprehensive web-based farm management system designed to empower farmers, agribusinesses, and agricultural cooperatives with modern digital tools for efficient farm operations. Built with Django and SQLite3, this application provides a centralized platform where users can plan, monitor, and analyze every aspect of their farming activities.

## Features

### Core Modules

1. **Dashboard**
   - Real-time statistics and key metrics
   - Active crops and livestock count
   - Monthly financial overview (income, expenses, net balance)
   - Low stock inventory alerts
   - Upcoming tasks and harvest schedules
   - Recent farm activities log

2. **Crop Management**
   - Track complete crop lifecycle (planting to harvest)
   - Record planting dates, expected yields, and actual harvests
   - Monitor crop status (planned, planted, growing, harvested, sold)
   - Upload crop images and maintain detailed notes
   - Calculate days to harvest automatically

3. **Livestock Management**
   - Manage multiple livestock types (cattle, poultry, sheep, goats, pigs)
   - Track individual animals with unique tag numbers
   - Monitor health status (healthy, sick, under treatment, pregnant)
   - Record weight, purchase price, and current value

4. **Inventory Management**
   - Track seeds, fertilizers, pesticides, equipment, and supplies
   - Monitor stock levels with automatic reorder alerts
   - Calculate total inventory value
   - Track suppliers and purchase dates

5. **Financial Management**
   - Record income and expenses with categories
   - Track crop sales, livestock sales, and input purchases
   - Upload receipts and maintain payment records
   - Generate financial reports and summaries

6. **Task Management**
   - Create and assign tasks to team members
   - Set priorities (low, medium, high, urgent)
   - Track task status (pending, in progress, completed)
   - Link tasks to specific crops or livestock

7. **Activity Logging**
   - Log daily farm activities in real-time
   - Track planting, irrigation, fertilization, harvesting
   - Record animal feeding, vaccination, and health checks
   - Monitor labor costs and materials used

8. **Analytics & Reports**
   - Crop status distribution charts
   - Livestock type statistics
   - Monthly financial trends (12-month view)
   - Activity distribution analysis

9. **User Management**
   - Multi-user support with role-based access
   - Roles: Farmer, Farm Manager, Worker, Consultant
   - User profiles with farm information

## Technology Stack

- **Backend**: Django 5.0 (Python web framework)
- **Database**: SQLite3 (lightweight, file-based database)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **Icons**: Font Awesome 6.4
- **Forms**: Django Crispy Forms with Bootstrap 4

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step 1: Navigate to Project Directory

```powershell
cd "c:\Users\hp\Downloads\farmflow-suite-main(1)\farmflow-suite-main"
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you encounter execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Database Setup

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)

```powershell
python manage.py createsuperuser
```

### Step 6: Create Media Directories

```powershell
New-Item -ItemType Directory -Force -Path media, static, staticfiles
New-Item -ItemType Directory -Force -Path media\avatars, media\crops, media\livestock, media\activities, media\receipts
```

### Step 7: Run Development Server

```powershell
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage Guide

### First Time Setup

1. Open browser and go to `http://127.0.0.1:8000/`
2. Click "Register Now" to create account
3. Login and complete your profile with farm details

### Daily Operations

- **Add Crops**: Navigate to Crops → Add New Crop
- **Manage Livestock**: Go to Livestock → Add New Animal
- **Track Inventory**: Access Inventory → Add Item
- **Record Finances**: Navigate to Finance → Add Transaction
- **Manage Tasks**: Go to Tasks → Add Task
- **Log Activities**: Click Activities → Log New Activity

### Admin Panel

Access at `http://127.0.0.1:8000/admin/` with superuser credentials to:
- Manage all users and profiles
- View and edit all records
- Perform bulk operations

## Database Backup

```powershell
# Backup database
Copy-Item db.sqlite3 "db_backup_$(Get-Date -Format 'yyyy-MM-dd').sqlite3"

# Backup media files
Copy-Item -Path media -Destination "media_backup_$(Get-Date -Format 'yyyy-MM-dd')" -Recurse
```

## Troubleshooting

1. **Import Error**: Activate virtual environment and install dependencies
2. **Database Locked**: Close all other connections
3. **Static Files Not Loading**: Run `python manage.py collectstatic`

## Project Structure

```
farmflow-suite-main/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3               # SQLite database (created after migration)
├── farmflow/                # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI configuration
├── farm/                    # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── urls.py              # App URL patterns
│   └── admin.py             # Admin configuration
├── templates/               # HTML templates
│   ├── base.html            # Base template with navigation
│   └── farm/                # App-specific templates
└── media/                   # User uploads
    ├── avatars/
    ├── crops/
    ├── livestock/
    └── receipts/
```

## Future Enhancements

- Weather API integration
- Mobile app (iOS/Android)
- Email notifications
- Export reports to PDF/Excel
- Multi-farm management
- GPS field mapping

## Credits

Built with Django, Bootstrap, Font Awesome, and Crispy Forms

---

**FarmFlow** - Empowering Modern Agriculture through Technology
