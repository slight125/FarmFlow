# FarmFlow Setup Script
# This script automates the setup process for FarmFlow

Write-Host "========================================" -ForegroundColor Green
Write-Host "   FarmFlow Setup Script" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, skipping..." -ForegroundColor Cyan
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "`nInstalling required packages..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✓ Packages installed" -ForegroundColor Green

# Create media directories
Write-Host "`nCreating media directories..." -ForegroundColor Yellow
$directories = @(
    "media",
    "media\avatars",
    "media\crops", 
    "media\livestock",
    "media\activities",
    "media\receipts",
    "static",
    "staticfiles"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "✓ Created $dir" -ForegroundColor Green
    } else {
        Write-Host "  $dir already exists" -ForegroundColor Cyan
    }
}

# Run migrations
Write-Host "`nSetting up database..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate
Write-Host "✓ Database setup complete" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "   Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Create a superuser account:" -ForegroundColor White
Write-Host "   python manage.py createsuperuser" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Start the development server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Open your browser and go to:" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/" -ForegroundColor Yellow
Write-Host ""
Write-Host "Admin panel available at:" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/admin/" -ForegroundColor Yellow
Write-Host ""
Write-Host "For detailed instructions, see QUICKSTART.md" -ForegroundColor Cyan
Write-Host ""
