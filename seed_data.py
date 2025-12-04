"""
Seed script to populate the FarmFlow database with sample data
Run this script with: python manage.py shell < seed_data.py
Or: python seed_data.py
"""
import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmflow.settings')
django.setup()

from django.contrib.auth.models import User
from farm.models import (
    UserProfile, Crop, Livestock, InventoryItem,
    FinancialTransaction, Task, Activity, WeatherData
)
from django.utils import timezone

def clear_existing_data():
    """Clear existing sample data (optional)"""
    print("Clearing existing data...")
    Activity.objects.all().delete()
    Task.objects.all().delete()
    FinancialTransaction.objects.all().delete()
    InventoryItem.objects.all().delete()
    Livestock.objects.all().delete()
    Crop.objects.all().delete()
    WeatherData.objects.all().delete()
    print("✓ Existing data cleared")

def get_random_date(days_back_min=0, days_back_max=180):
    """Generate a random date within specified range"""
    days_back = random.randint(days_back_min, days_back_max)
    return timezone.now().date() - timedelta(days=days_back)

def get_future_date(days_ahead_min=30, days_ahead_max=120):
    """Generate a random future date"""
    days_ahead = random.randint(days_ahead_min, days_ahead_max)
    return timezone.now().date() + timedelta(days=days_ahead)

def seed_crops(users):
    """Seed crop data"""
    print("\nSeeding crops...")
    
    crop_data = [
        # Maize varieties
        ('Maize', 'H614', 5.0, 'planted'),
        ('Maize', 'DH04', 3.5, 'growing'),
        ('Maize', 'H513', 4.2, 'growing'),
        ('Maize', 'KH500-19A', 6.0, 'harvested'),
        
        # Wheat varieties
        ('Wheat', 'Kenya Fahari', 4.5, 'planted'),
        ('Wheat', 'Kingbird', 3.0, 'growing'),
        
        # Beans
        ('Beans', 'Rosecoco', 2.0, 'planted'),
        ('Beans', 'Red Haricot', 1.5, 'harvested'),
        ('Beans', 'Mwitemania', 2.5, 'sold'),
        
        # Vegetables
        ('Tomatoes', 'Anna F1', 1.0, 'growing'),
        ('Cabbage', 'Gloria F1', 0.8, 'growing'),
        ('Kale', 'Thousand Headed', 1.2, 'planted'),
        ('Spinach', 'Fordhook Giant', 0.5, 'growing'),
        
        # Cash crops
        ('Coffee', 'Ruiru 11', 8.0, 'growing'),
        ('Tea', 'Clone 6/8', 5.5, 'growing'),
        ('Sugarcane', 'CO421', 4.0, 'planted'),
        
        # Fruits
        ('Bananas', 'Cavendish', 2.0, 'growing'),
        ('Avocado', 'Hass', 3.0, 'growing'),
        ('Mangoes', 'Apple Mango', 2.5, 'harvested'),
    ]
    
    crops_created = []
    for user in users:
        # Each user gets 8-12 random crops
        num_crops = random.randint(8, 12)
        user_crop_data = random.sample(crop_data, min(num_crops, len(crop_data)))
        
        for name, variety, base_area, status in user_crop_data:
            area = Decimal(str(base_area * random.uniform(0.8, 1.5)))
            planting_date = get_random_date(10, 150)
            expected_harvest = planting_date + timedelta(days=random.randint(90, 150))
            
            # Set actual harvest date if status is harvested or sold
            actual_harvest = None
            if status in ['harvested', 'sold']:
                actual_harvest = planting_date + timedelta(days=random.randint(90, 140))
            
            # Calculate yields
            expected_yield = area * Decimal(str(random.uniform(1000, 3000)))
            actual_yield = None
            if status in ['harvested', 'sold']:
                actual_yield = expected_yield * Decimal(str(random.uniform(0.7, 1.2)))
            
            crop = Crop.objects.create(
                user=user,
                name=name,
                variety=variety,
                area=area,
                planting_date=planting_date,
                expected_harvest_date=expected_harvest,
                actual_harvest_date=actual_harvest,
                status=status,
                expected_yield=expected_yield,
                actual_yield=actual_yield,
                notes=f"Growing conditions: Good. Regular monitoring required."
            )
            crops_created.append(crop)
    
    print(f"✓ Created {len(crops_created)} crops")
    return crops_created

def seed_livestock(users):
    """Seed livestock data"""
    print("\nSeeding livestock...")
    
    livestock_data = [
        ('cattle', 'Friesian', 'female', 'healthy', 450, 80000),
        ('cattle', 'Ayrshire', 'female', 'healthy', 420, 75000),
        ('cattle', 'Jersey', 'female', 'pregnant', 380, 70000),
        ('cattle', 'Guernsey', 'male', 'healthy', 500, 85000),
        ('poultry', 'Layers', 'female', 'healthy', 2, 500),
        ('poultry', 'Broilers', 'male', 'healthy', 3, 600),
        ('poultry', 'Kenbro', 'female', 'healthy', 2.5, 550),
        ('sheep', 'Dorper', 'female', 'healthy', 60, 12000),
        ('sheep', 'Merino', 'male', 'healthy', 70, 15000),
        ('goat', 'Dairy Goat', 'female', 'healthy', 45, 8000),
        ('goat', 'Boer', 'male', 'healthy', 55, 10000),
        ('pig', 'Large White', 'female', 'pregnant', 180, 25000),
        ('pig', 'Landrace', 'male', 'healthy', 200, 28000),
    ]
    
    livestock_created = []
    for user in users:
        num_animals = random.randint(10, 20)
        
        for i in range(num_animals):
            animal_type, breed, gender, status, base_weight, base_price = random.choice(livestock_data)
            
            weight = Decimal(str(base_weight * random.uniform(0.8, 1.2)))
            purchase_price = Decimal(str(base_price * random.uniform(0.9, 1.1)))
            current_value = purchase_price * Decimal(str(random.uniform(1.0, 1.3)))
            
            # Generate unique tag number
            tag_number = f"{animal_type[:3].upper()}-{user.id}-{i+1:04d}"
            
            livestock = Livestock.objects.create(
                user=user,
                type=animal_type,
                breed=breed,
                tag_number=tag_number,
                date_acquired=get_random_date(30, 365),
                date_of_birth=get_random_date(365, 1095),
                gender=gender,
                status=status,
                weight=weight,
                purchase_price=purchase_price,
                current_value=current_value,
                notes=f"Regular health monitoring. Last check: {get_random_date(1, 30)}"
            )
            livestock_created.append(livestock)
    
    print(f"✓ Created {len(livestock_created)} livestock")
    return livestock_created

def seed_inventory(users):
    """Seed inventory items"""
    print("\nSeeding inventory...")
    
    inventory_data = [
        ('seed', 'Maize Seeds H614', 50, 'kg', 10, 250),
        ('seed', 'Bean Seeds Rosecoco', 25, 'kg', 5, 300),
        ('seed', 'Tomato Seeds', 2, 'kg', 0.5, 5000),
        ('fertilizer', 'NPK 17:17:17', 500, 'kg', 100, 120),
        ('fertilizer', 'DAP Fertilizer', 400, 'kg', 80, 130),
        ('fertilizer', 'Urea', 300, 'kg', 60, 90),
        ('fertilizer', 'CAN (Calcium Ammonium Nitrate)', 350, 'kg', 70, 100),
        ('pesticide', 'Karate Insecticide', 10, 'ltr', 2, 1500),
        ('pesticide', 'Roundup Herbicide', 15, 'ltr', 3, 1200),
        ('pesticide', 'Fungicide Mancozeb', 20, 'kg', 5, 800),
        ('equipment', 'Watering Cans', 10, 'pcs', 2, 500),
        ('equipment', 'Spades', 8, 'pcs', 2, 800),
        ('equipment', 'Hoes', 12, 'pcs', 3, 600),
        ('equipment', 'Pruning Shears', 6, 'pcs', 1, 1200),
        ('feed', 'Dairy Meal', 1000, 'kg', 200, 45),
        ('feed', 'Layers Mash', 800, 'kg', 150, 50),
        ('feed', 'Pig Grower', 600, 'kg', 100, 48),
        ('medicine', 'Dewormer', 5, 'ltr', 1, 3000),
        ('medicine', 'Antibiotics', 20, 'pcs', 5, 500),
        ('medicine', 'Vitamins Supplement', 15, 'pcs', 3, 400),
        ('fuel', 'Diesel', 200, 'ltr', 50, 150),
        ('fuel', 'Petrol', 100, 'ltr', 20, 170),
    ]
    
    inventory_created = []
    for user in users:
        # Each user gets 12-18 inventory items
        num_items = random.randint(12, 18)
        user_inventory = random.sample(inventory_data, min(num_items, len(inventory_data)))
        
        for category, name, base_qty, unit, reorder, base_cost in user_inventory:
            quantity = Decimal(str(base_qty * random.uniform(0.5, 1.5)))
            cost = Decimal(str(base_cost * random.uniform(0.9, 1.1)))
            reorder_level = Decimal(str(reorder))
            
            purchase_date = get_random_date(10, 120)
            expiry_date = None
            if category in ['seed', 'pesticide', 'medicine', 'feed']:
                expiry_date = purchase_date + timedelta(days=random.randint(180, 730))
            
            item = InventoryItem.objects.create(
                user=user,
                name=name,
                category=category,
                quantity=quantity,
                unit=unit,
                reorder_level=reorder_level,
                cost_per_unit=cost,
                supplier=f"Supplier {random.choice(['A', 'B', 'C', 'D'])} Ltd",
                purchase_date=purchase_date,
                expiry_date=expiry_date,
                location=f"Store {random.choice(['A', 'B', 'Main'])}",
                notes="Regular stock monitoring required"
            )
            inventory_created.append(item)
    
    print(f"✓ Created {len(inventory_created)} inventory items")
    return inventory_created

def seed_financial_transactions(users, crops):
    """Seed financial transactions"""
    print("\nSeeding financial transactions...")
    
    transactions_created = []
    
    for user in users:
        num_transactions = random.randint(30, 50)
        
        for _ in range(num_transactions):
            trans_type = random.choice(['income', 'income', 'expense', 'expense', 'expense'])
            
            if trans_type == 'income':
                category = random.choice(['crop_sale', 'livestock_sale'])
                amount = Decimal(str(random.uniform(5000, 50000)))
                description = f"{category.replace('_', ' ').title()} - {random.choice(['Market', 'Direct buyer', 'Cooperative'])}"
            else:
                category = random.choice([
                    'seed_purchase', 'fertilizer_purchase', 'pesticide_purchase',
                    'equipment_purchase', 'fuel', 'labor', 'veterinary',
                    'maintenance', 'utilities'
                ])
                amount = Decimal(str(random.uniform(500, 20000)))
                description = f"{category.replace('_', ' ').title()} - {random.choice(['Monthly', 'Weekly', 'One-time'])}"
            
            transaction = FinancialTransaction.objects.create(
                user=user,
                type=trans_type,
                category=category,
                amount=amount,
                date=get_random_date(5, 180),
                description=description,
                payment_method=random.choice(['Cash', 'M-Pesa', 'Bank Transfer', 'Cheque']),
                reference_number=f"REF-{random.randint(10000, 99999)}",
                notes="Transaction completed successfully"
            )
            transactions_created.append(transaction)
    
    print(f"✓ Created {len(transactions_created)} financial transactions")
    return transactions_created

def seed_tasks(users, crops, livestock):
    """Seed tasks"""
    print("\nSeeding tasks...")
    
    task_templates = [
        ('Apply fertilizer to crops', 'Apply NPK fertilizer to maize field. Rate: 50kg/acre', 'high'),
        ('Weed the field', 'Remove weeds from beans section. Manual weeding required.', 'medium'),
        ('Check irrigation system', 'Inspect all irrigation pipes and repair leaks if any.', 'high'),
        ('Harvest ready crops', 'Harvest mature crops from section B. Store properly.', 'urgent'),
        ('Vaccinate poultry', 'Administer Newcastle disease vaccine to all layers.', 'high'),
        ('Check cattle health', 'Routine health checkup for all cattle. Note any concerns.', 'medium'),
        ('Apply pesticide', 'Spray insecticide on tomato plants. Use protective gear.', 'high'),
        ('Feed livestock', 'Ensure all animals have adequate feed and clean water.', 'medium'),
        ('Repair farm equipment', 'Service and repair the tractor. Check oil and tires.', 'medium'),
        ('Prepare seedbeds', 'Clear and prepare land for next planting season.', 'low'),
        ('Prune fruit trees', 'Prune mango and avocado trees for better growth.', 'low'),
        ('Clean animal shelters', 'Deep clean all animal shelters and disinfect.', 'medium'),
        ('Test soil pH', 'Collect soil samples and test pH levels. Amend if needed.', 'medium'),
        ('Stock feed supplies', 'Purchase and stock animal feed for the month.', 'high'),
        ('Inspect fencing', 'Check all fences for damage and repair weak sections.', 'medium'),
    ]
    
    tasks_created = []
    for user in users:
        num_tasks = random.randint(15, 25)
        
        for _ in range(num_tasks):
            title, description, priority = random.choice(task_templates)
            status = random.choice(['pending', 'pending', 'in_progress', 'completed'])
            
            due_date = get_future_date(1, 60) if status != 'completed' else get_random_date(1, 30)
            completed_date = due_date if status == 'completed' else None
            
            # Randomly link to crop or livestock
            related_crop = random.choice(crops + [None, None, None])
            related_livestock = random.choice(livestock + [None, None, None])
            
            task = Task.objects.create(
                user=user,
                title=title,
                description=description,
                priority=priority,
                status=status,
                due_date=due_date,
                completed_date=completed_date,
                related_crop=related_crop if related_crop and related_crop.user == user else None,
                related_livestock=related_livestock if related_livestock and related_livestock.user == user else None,
                notes="Task created via management system"
            )
            tasks_created.append(task)
    
    print(f"✓ Created {len(tasks_created)} tasks")
    return tasks_created

def seed_activities(users, crops, livestock):
    """Seed farm activities"""
    print("\nSeeding activities...")
    
    activity_templates = [
        ('planting', 'Planted seeds', 'Planted seeds in prepared field. Weather conditions favorable.'),
        ('irrigation', 'Irrigated crops', 'Watered crops for 2 hours. Soil moisture adequate.'),
        ('fertilization', 'Applied fertilizer', 'Applied NPK fertilizer as per schedule. Even distribution.'),
        ('pesticide_application', 'Sprayed pesticide', 'Applied insecticide to control pests. Used safety equipment.'),
        ('weeding', 'Weeding activity', 'Removed weeds manually. Field now clean.'),
        ('harvesting', 'Harvested crops', 'Harvested mature crops. Good yield observed.'),
        ('feeding', 'Fed animals', 'Provided feed and water to all livestock. All animals healthy.'),
        ('vaccination', 'Vaccination done', 'Administered vaccines to livestock. No adverse reactions.'),
        ('health_check', 'Health inspection', 'Checked all animals for health issues. All clear.'),
        ('milking', 'Milking session', 'Completed morning/evening milking. Good milk production.'),
        ('maintenance', 'Equipment maintenance', 'Serviced farm equipment. All functioning well.'),
    ]
    
    activities_created = []
    for user in users:
        num_activities = random.randint(25, 40)
        
        for _ in range(num_activities):
            activity_type, title, description = random.choice(activity_templates)
            
            date = timezone.make_aware(
                datetime.combine(get_random_date(1, 90), datetime.min.time()) + 
                timedelta(hours=random.randint(6, 18))
            )
            
            duration = random.randint(30, 240)
            labor_cost = Decimal(str(random.uniform(200, 2000)))
            
            # Randomly link to crop or livestock
            related_crop = None
            related_livestock = None
            
            if activity_type in ['planting', 'irrigation', 'fertilization', 'pesticide_application', 'weeding', 'harvesting']:
                user_crops = [c for c in crops if c.user == user]
                if user_crops:
                    related_crop = random.choice(user_crops)
            elif activity_type in ['feeding', 'vaccination', 'health_check', 'milking']:
                user_livestock = [l for l in livestock if l.user == user]
                if user_livestock:
                    related_livestock = random.choice(user_livestock)
            
            activity = Activity.objects.create(
                user=user,
                activity_type=activity_type,
                title=title,
                description=description,
                date=date,
                duration=duration,
                related_crop=related_crop,
                related_livestock=related_livestock,
                labor_cost=labor_cost,
                materials_used=f"Used standard materials. Quantity: {random.randint(1, 10)} units",
                notes="Activity logged automatically"
            )
            activities_created.append(activity)
    
    print(f"✓ Created {len(activities_created)} activities")
    return activities_created

def seed_weather_data(users):
    """Seed weather data"""
    print("\nSeeding weather data...")
    
    weather_conditions = [
        'Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain',
        'Heavy Rain', 'Thunderstorms', 'Overcast', 'Clear'
    ]
    
    weather_created = []
    for user in users:
        # Create weather data for the last 90 days
        for days_back in range(90):
            date = timezone.now().date() - timedelta(days=days_back)
            
            # Generate realistic weather data
            base_temp = random.uniform(18, 28)
            temp_high = Decimal(str(base_temp + random.uniform(2, 8)))
            temp_low = Decimal(str(base_temp - random.uniform(2, 5)))
            
            humidity = random.randint(40, 90)
            rainfall = Decimal(str(random.uniform(0, 50))) if random.random() > 0.6 else Decimal('0')
            wind_speed = Decimal(str(random.uniform(5, 25)))
            conditions = random.choice(weather_conditions)
            
            weather = WeatherData.objects.create(
                user=user,
                date=date,
                temperature_high=temp_high,
                temperature_low=temp_low,
                humidity=humidity,
                rainfall=rainfall,
                wind_speed=wind_speed,
                conditions=conditions,
                notes=f"Weather data for {date}"
            )
            weather_created.append(weather)
    
    print(f"✓ Created {len(weather_created)} weather records")
    return weather_created

def main():
    """Main seeding function"""
    print("=" * 60)
    print("FarmFlow Database Seeding Script")
    print("=" * 60)
    
    # Option to clear existing data
    clear = input("\nClear existing data? (y/n): ").lower()
    if clear == 'y':
        clear_existing_data()
    
    # Get users with farmer/manager roles
    print("\nGetting users...")
    users = list(User.objects.filter(
        profile__role__in=['farmer', 'manager']
    ).select_related('profile'))
    
    if not users:
        print("⚠ No users with farmer/manager roles found!")
        print("Creating test users first...")
        # Use existing test users if they exist
        users = []
        for username in ['farmer_john', 'manager_mary', 'allan']:
            user = User.objects.filter(username=username).first()
            if user:
                users.append(user)
        
        if not users:
            print("⚠ No suitable users found. Please create users first.")
            return
    
    print(f"✓ Found {len(users)} users")
    
    # Seed all data
    crops = seed_crops(users)
    livestock = seed_livestock(users)
    inventory = seed_inventory(users)
    transactions = seed_financial_transactions(users, crops)
    tasks = seed_tasks(users, crops, livestock)
    activities = seed_activities(users, crops, livestock)
    weather = seed_weather_data(users)
    
    # Summary
    print("\n" + "=" * 60)
    print("SEEDING COMPLETE!")
    print("=" * 60)
    print(f"✓ Crops: {len(crops)}")
    print(f"✓ Livestock: {len(livestock)}")
    print(f"✓ Inventory Items: {len(inventory)}")
    print(f"✓ Financial Transactions: {len(transactions)}")
    print(f"✓ Tasks: {len(tasks)}")
    print(f"✓ Activities: {len(activities)}")
    print(f"✓ Weather Records: {len(weather)}")
    print("\nTotal records created:", 
          len(crops) + len(livestock) + len(inventory) + 
          len(transactions) + len(tasks) + len(activities) + len(weather))
    print("\n✓ Database seeded successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
