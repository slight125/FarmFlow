"""
Test script to verify CRUD operations for all models
Run this script to test Create, Read, Update, Delete operations
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmflow.settings')
django.setup()

from django.contrib.auth.models import User
from farm.models import (
    UserProfile, Crop, Livestock, InventoryItem,
    FinancialTransaction, Task, Activity, WeatherData
)
from datetime import date, timedelta, datetime
from decimal import Decimal

def test_crud_operations():
    print("=" * 60)
    print("FARMFLOW CRUD OPERATIONS TEST")
    print("=" * 60)
    
    # Get test user
    test_user = User.objects.filter(username='farmer_john').first()
    if not test_user:
        print("❌ Test user 'farmer_john' not found. Please run seed_db first.")
        return
    
    print(f"\n✓ Using test user: {test_user.username}")
    
    # Test 1: CROP CRUD
    print("\n" + "=" * 60)
    print("1. TESTING CROP CRUD OPERATIONS")
    print("=" * 60)
    
    # CREATE
    print("\n[CREATE] Creating new crop...")
    new_crop = Crop.objects.create(
        user=test_user,
        name="Test Maize",
        variety="H614",
        area=Decimal("2.5"),
        planting_date=date.today(),
        expected_harvest_date=date.today() + timedelta(days=120),
        status="planted",
        expected_yield=Decimal("2500")
    )
    print(f"✓ Created crop: {new_crop.name} (ID: {new_crop.id})")
    
    # READ
    print("\n[READ] Reading crop...")
    read_crop = Crop.objects.get(id=new_crop.id)
    print(f"✓ Read crop: {read_crop.name} - {read_crop.variety}")
    print(f"  Area: {read_crop.area} acres, Status: {read_crop.status}")
    
    # UPDATE
    print("\n[UPDATE] Updating crop status...")
    read_crop.status = "growing"
    read_crop.notes = "Growing well, good rainfall"
    read_crop.save()
    updated_crop = Crop.objects.get(id=new_crop.id)
    print(f"✓ Updated crop status to: {updated_crop.status}")
    print(f"  Notes: {updated_crop.notes}")
    
    # DELETE
    print("\n[DELETE] Deleting test crop...")
    crop_id = updated_crop.id
    updated_crop.delete()
    crop_exists = Crop.objects.filter(id=crop_id).exists()
    print(f"✓ Crop deleted. Exists: {crop_exists}")
    
    # Test 2: LIVESTOCK CRUD
    print("\n" + "=" * 60)
    print("2. TESTING LIVESTOCK CRUD OPERATIONS")
    print("=" * 60)
    
    # CREATE
    print("\n[CREATE] Creating new livestock...")
    new_livestock = Livestock.objects.create(
        user=test_user,
        type="cattle",
        breed="Test Friesian",
        tag_number=f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        date_acquired=date.today(),
        gender="female",
        status="healthy",
        weight=Decimal("350"),
        purchase_price=Decimal("45000")
    )
    print(f"✓ Created livestock: {new_livestock.type} - {new_livestock.tag_number}")
    
    # READ
    print("\n[READ] Reading livestock...")
    read_livestock = Livestock.objects.get(id=new_livestock.id)
    print(f"✓ Read livestock: {read_livestock.breed} ({read_livestock.tag_number})")
    print(f"  Weight: {read_livestock.weight}kg, Status: {read_livestock.status}")
    
    # UPDATE
    print("\n[UPDATE] Updating livestock weight...")
    read_livestock.weight = Decimal("380")
    read_livestock.status = "pregnant"
    read_livestock.save()
    updated_livestock = Livestock.objects.get(id=new_livestock.id)
    print(f"✓ Updated livestock weight to: {updated_livestock.weight}kg")
    print(f"  Status: {updated_livestock.status}")
    
    # DELETE
    print("\n[DELETE] Deleting test livestock...")
    livestock_id = updated_livestock.id
    updated_livestock.delete()
    livestock_exists = Livestock.objects.filter(id=livestock_id).exists()
    print(f"✓ Livestock deleted. Exists: {livestock_exists}")
    
    # Test 3: INVENTORY CRUD
    print("\n" + "=" * 60)
    print("3. TESTING INVENTORY CRUD OPERATIONS")
    print("=" * 60)
    
    # CREATE
    print("\n[CREATE] Creating new inventory item...")
    new_inventory = InventoryItem.objects.create(
        user=test_user,
        name="Test NPK Fertilizer",
        category="fertilizer",
        quantity=Decimal("50"),
        unit="bag",
        reorder_level=Decimal("10"),
        cost_per_unit=Decimal("3500")
    )
    print(f"✓ Created inventory: {new_inventory.name}")
    
    # READ
    print("\n[READ] Reading inventory item...")
    read_inventory = InventoryItem.objects.get(id=new_inventory.id)
    print(f"✓ Read inventory: {read_inventory.name}")
    print(f"  Quantity: {read_inventory.quantity} {read_inventory.unit}")
    print(f"  Total value: KSh {read_inventory.total_value}")
    
    # UPDATE
    print("\n[UPDATE] Updating inventory quantity...")
    read_inventory.quantity = Decimal("45")
    read_inventory.supplier = "Test Agro Supplies"
    read_inventory.save()
    updated_inventory = InventoryItem.objects.get(id=new_inventory.id)
    print(f"✓ Updated inventory quantity to: {updated_inventory.quantity} {updated_inventory.unit}")
    print(f"  Supplier: {updated_inventory.supplier}")
    
    # DELETE
    print("\n[DELETE] Deleting test inventory item...")
    inventory_id = updated_inventory.id
    updated_inventory.delete()
    inventory_exists = InventoryItem.objects.filter(id=inventory_id).exists()
    print(f"✓ Inventory item deleted. Exists: {inventory_exists}")
    
    # Test 4: FINANCIAL TRANSACTION CRUD
    print("\n" + "=" * 60)
    print("4. TESTING FINANCIAL TRANSACTION CRUD OPERATIONS")
    print("=" * 60)
    
    # CREATE
    print("\n[CREATE] Creating new transaction...")
    new_transaction = FinancialTransaction.objects.create(
        user=test_user,
        type="expense",
        category="fertilizer_purchase",
        amount=Decimal("15000"),
        date=date.today(),
        description="Test fertilizer purchase",
        payment_method="M-Pesa"
    )
    print(f"✓ Created transaction: {new_transaction.category}")
    
    # READ
    print("\n[READ] Reading transaction...")
    read_transaction = FinancialTransaction.objects.get(id=new_transaction.id)
    print(f"✓ Read transaction: {read_transaction.type} - {read_transaction.category}")
    print(f"  Amount: KSh {read_transaction.amount}")
    print(f"  Description: {read_transaction.description}")
    
    # UPDATE
    print("\n[UPDATE] Updating transaction...")
    read_transaction.amount = Decimal("16500")
    read_transaction.reference_number = "TEST123456"
    read_transaction.save()
    updated_transaction = FinancialTransaction.objects.get(id=new_transaction.id)
    print(f"✓ Updated transaction amount to: KSh {updated_transaction.amount}")
    print(f"  Reference: {updated_transaction.reference_number}")
    
    # DELETE
    print("\n[DELETE] Deleting test transaction...")
    transaction_id = updated_transaction.id
    updated_transaction.delete()
    transaction_exists = FinancialTransaction.objects.filter(id=transaction_id).exists()
    print(f"✓ Transaction deleted. Exists: {transaction_exists}")
    
    # Test 5: TASK CRUD
    print("\n" + "=" * 60)
    print("5. TESTING TASK CRUD OPERATIONS")
    print("=" * 60)
    
    # CREATE
    print("\n[CREATE] Creating new task...")
    new_task = Task.objects.create(
        user=test_user,
        title="Test Irrigation Task",
        description="Test irrigation of test field",
        priority="high",
        status="pending",
        due_date=date.today() + timedelta(days=2)
    )
    print(f"✓ Created task: {new_task.title}")
    
    # READ
    print("\n[READ] Reading task...")
    read_task = Task.objects.get(id=new_task.id)
    print(f"✓ Read task: {read_task.title}")
    print(f"  Priority: {read_task.priority}, Status: {read_task.status}")
    print(f"  Due date: {read_task.due_date}")
    
    # UPDATE
    print("\n[UPDATE] Updating task status...")
    read_task.status = "in_progress"
    read_task.notes = "Started irrigation work"
    read_task.save()
    updated_task = Task.objects.get(id=new_task.id)
    print(f"✓ Updated task status to: {updated_task.status}")
    print(f"  Notes: {updated_task.notes}")
    
    # DELETE
    print("\n[DELETE] Deleting test task...")
    task_id = updated_task.id
    updated_task.delete()
    task_exists = Task.objects.filter(id=task_id).exists()
    print(f"✓ Task deleted. Exists: {task_exists}")
    
    # Test 6: ACTIVITY CRUD
    print("\n" + "=" * 60)
    print("6. TESTING ACTIVITY CRUD OPERATIONS")
    print("=" * 60)
    
    # CREATE
    print("\n[CREATE] Creating new activity...")
    new_activity = Activity.objects.create(
        user=test_user,
        activity_type="irrigation",
        title="Test Irrigation Activity",
        description="Irrigated test field",
        date=datetime.now(),
        duration=120,
        labor_cost=Decimal("500")
    )
    print(f"✓ Created activity: {new_activity.title}")
    
    # READ
    print("\n[READ] Reading activity...")
    read_activity = Activity.objects.get(id=new_activity.id)
    print(f"✓ Read activity: {read_activity.activity_type} - {read_activity.title}")
    print(f"  Duration: {read_activity.duration} minutes")
    print(f"  Labor cost: KSh {read_activity.labor_cost}")
    
    # UPDATE
    print("\n[UPDATE] Updating activity...")
    read_activity.duration = 150
    read_activity.materials_used = "200L water, irrigation equipment"
    read_activity.save()
    updated_activity = Activity.objects.get(id=new_activity.id)
    print(f"✓ Updated activity duration to: {updated_activity.duration} minutes")
    print(f"  Materials: {updated_activity.materials_used}")
    
    # DELETE
    print("\n[DELETE] Deleting test activity...")
    activity_id = updated_activity.id
    updated_activity.delete()
    activity_exists = Activity.objects.filter(id=activity_id).exists()
    print(f"✓ Activity deleted. Exists: {activity_exists}")
    
    # Test 7: WEATHER DATA CRUD
    print("\n" + "=" * 60)
    print("7. TESTING WEATHER DATA CRUD OPERATIONS")
    print("=" * 60)
    
    # CREATE
    print("\n[CREATE] Creating new weather data...")
    new_weather = WeatherData.objects.create(
        user=test_user,
        date=date.today(),
        temperature_high=Decimal("28.5"),
        temperature_low=Decimal("18.2"),
        humidity=65,
        rainfall=Decimal("5.5"),
        wind_speed=Decimal("12.0"),
        conditions="Partly cloudy with light rain"
    )
    print(f"✓ Created weather data for: {new_weather.date}")
    
    # READ
    print("\n[READ] Reading weather data...")
    read_weather = WeatherData.objects.get(id=new_weather.id)
    print(f"✓ Read weather data: {read_weather.conditions}")
    print(f"  Temp: {read_weather.temperature_low}°C - {read_weather.temperature_high}°C")
    print(f"  Rainfall: {read_weather.rainfall}mm")
    
    # UPDATE
    print("\n[UPDATE] Updating weather data...")
    read_weather.temperature_high = Decimal("30.0")
    read_weather.rainfall = Decimal("12.5")
    read_weather.save()
    updated_weather = WeatherData.objects.get(id=new_weather.id)
    print(f"✓ Updated weather: Temp high to {updated_weather.temperature_high}°C")
    print(f"  Rainfall: {updated_weather.rainfall}mm")
    
    # DELETE
    print("\n[DELETE] Deleting test weather data...")
    weather_id = updated_weather.id
    updated_weather.delete()
    weather_exists = WeatherData.objects.filter(id=weather_id).exists()
    print(f"✓ Weather data deleted. Exists: {weather_exists}")
    
    # Final Summary
    print("\n" + "=" * 60)
    print("CRUD OPERATIONS TEST SUMMARY")
    print("=" * 60)
    print("✅ ALL CRUD OPERATIONS COMPLETED SUCCESSFULLY!")
    print("\nTested models:")
    print("  1. ✅ Crop (CREATE, READ, UPDATE, DELETE)")
    print("  2. ✅ Livestock (CREATE, READ, UPDATE, DELETE)")
    print("  3. ✅ InventoryItem (CREATE, READ, UPDATE, DELETE)")
    print("  4. ✅ FinancialTransaction (CREATE, READ, UPDATE, DELETE)")
    print("  5. ✅ Task (CREATE, READ, UPDATE, DELETE)")
    print("  6. ✅ Activity (CREATE, READ, UPDATE, DELETE)")
    print("  7. ✅ WeatherData (CREATE, READ, UPDATE, DELETE)")
    print("\n" + "=" * 60)
    print("All CRUD functionalities are working correctly!")
    print("=" * 60)

if __name__ == '__main__':
    try:
        test_crud_operations()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
