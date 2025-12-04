"""
Django management command to seed the database with sample data
Run with: python manage.py seed_db
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from farm.models import (
    UserProfile, Crop, Livestock, InventoryItem,
    FinancialTransaction, Task, Activity, WeatherData
)
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample farm data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS('FarmFlow Database Seeding'))
        self.stdout.write("=" * 60)

        if options['clear']:
            self.clear_data()

        users = self.get_users()
        if not users:
            self.stdout.write(self.style.ERROR('No suitable users found!'))
            return

        self.stdout.write(f'\nFound {len(users)} users')

        crops = self.seed_crops(users)
        livestock = self.seed_livestock(users)
        inventory = self.seed_inventory(users)
        transactions = self.seed_transactions(users, crops)
        tasks = self.seed_tasks(users, crops, livestock)
        activities = self.seed_activities(users, crops, livestock)
        weather = self.seed_weather(users)

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS('SEEDING COMPLETE!'))
        self.stdout.write("=" * 60)
        self.stdout.write(f'Crops: {len(crops)}')
        self.stdout.write(f'Livestock: {len(livestock)}')
        self.stdout.write(f'Inventory: {len(inventory)}')
        self.stdout.write(f'Transactions: {len(transactions)}')
        self.stdout.write(f'Tasks: {len(tasks)}')
        self.stdout.write(f'Activities: {len(activities)}')
        self.stdout.write(f'Weather Records: {len(weather)}')
        total = len(crops) + len(livestock) + len(inventory) + len(transactions) + len(tasks) + len(activities) + len(weather)
        self.stdout.write(self.style.SUCCESS(f'\nTotal: {total} records created!'))
        self.stdout.write("=" * 60)

    def clear_data(self):
        self.stdout.write('\nClearing existing data...')
        Activity.objects.all().delete()
        Task.objects.all().delete()
        FinancialTransaction.objects.all().delete()
        InventoryItem.objects.all().delete()
        Livestock.objects.all().delete()
        Crop.objects.all().delete()
        WeatherData.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✓ Data cleared'))

    def get_users(self):
        users = list(User.objects.filter(
            profile__role__in=['farmer', 'manager']
        ).select_related('profile'))
        
        if not users:
            for username in ['farmer_john', 'manager_mary', 'allan', 'admin']:
                user = User.objects.filter(username=username).first()
                if user:
                    users.append(user)
        
        return users

    def get_random_date(self, days_back_min=0, days_back_max=180):
        days_back = random.randint(days_back_min, days_back_max)
        return timezone.now().date() - timedelta(days=days_back)

    def get_future_date(self, days_ahead_min=30, days_ahead_max=120):
        days_ahead = random.randint(days_ahead_min, days_ahead_max)
        return timezone.now().date() + timedelta(days=days_ahead)

    def seed_crops(self, users):
        self.stdout.write('\nSeeding crops...')
        crop_data = [
            ('Maize', 'H614', 5.0, 'planted'),
            ('Maize', 'DH04', 3.5, 'growing'),
            ('Maize', 'H513', 4.2, 'growing'),
            ('Wheat', 'Kenya Fahari', 4.5, 'planted'),
            ('Beans', 'Rosecoco', 2.0, 'planted'),
            ('Beans', 'Red Haricot', 1.5, 'harvested'),
            ('Tomatoes', 'Anna F1', 1.0, 'growing'),
            ('Cabbage', 'Gloria F1', 0.8, 'growing'),
            ('Kale', 'Thousand Headed', 1.2, 'planted'),
            ('Coffee', 'Ruiru 11', 8.0, 'growing'),
            ('Tea', 'Clone 6/8', 5.5, 'growing'),
            ('Bananas', 'Cavendish', 2.0, 'growing'),
            ('Avocado', 'Hass', 3.0, 'growing'),
        ]
        
        crops = []
        for user in users:
            for name, variety, base_area, status in random.sample(crop_data, min(10, len(crop_data))):
                area = Decimal(str(base_area * random.uniform(0.8, 1.5)))
                planting_date = self.get_random_date(10, 150)
                expected_harvest = planting_date + timedelta(days=random.randint(90, 150))
                
                actual_harvest = None
                if status in ['harvested', 'sold']:
                    actual_harvest = planting_date + timedelta(days=random.randint(90, 140))
                
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
                    notes=f"Growing well. Regular monitoring."
                )
                crops.append(crop)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(crops)} crops'))
        return crops

    def seed_livestock(self, users):
        self.stdout.write('\nSeeding livestock...')
        livestock_data = [
            ('cattle', 'Friesian', 'female', 'healthy', 450, 80000),
            ('cattle', 'Ayrshire', 'female', 'pregnant', 420, 75000),
            ('poultry', 'Layers', 'female', 'healthy', 2, 500),
            ('poultry', 'Broilers', 'male', 'healthy', 3, 600),
            ('sheep', 'Dorper', 'female', 'healthy', 60, 12000),
            ('goat', 'Dairy Goat', 'female', 'healthy', 45, 8000),
            ('pig', 'Large White', 'female', 'pregnant', 180, 25000),
        ]
        
        livestock = []
        for user in users:
            for i in range(random.randint(10, 15)):
                animal_type, breed, gender, status, base_weight, base_price = random.choice(livestock_data)
                
                tag_number = f"{animal_type[:3].upper()}-{user.id}-{i+1:04d}-{random.randint(100,999)}"
                
                animal = Livestock.objects.create(
                    user=user,
                    type=animal_type,
                    breed=breed,
                    tag_number=tag_number,
                    date_acquired=self.get_random_date(30, 365),
                    date_of_birth=self.get_random_date(365, 1095),
                    gender=gender,
                    status=status,
                    weight=Decimal(str(base_weight * random.uniform(0.8, 1.2))),
                    purchase_price=Decimal(str(base_price * random.uniform(0.9, 1.1))),
                    current_value=Decimal(str(base_price * random.uniform(1.0, 1.3))),
                    notes=f"Health status: {status}. Last check: recent."
                )
                livestock.append(animal)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(livestock)} livestock'))
        return livestock

    def seed_inventory(self, users):
        self.stdout.write('\nSeeding inventory...')
        inventory_data = [
            ('seed', 'Maize Seeds H614', 50, 'kg', 10, 250),
            ('seed', 'Bean Seeds', 25, 'kg', 5, 300),
            ('fertilizer', 'NPK 17:17:17', 500, 'kg', 100, 120),
            ('fertilizer', 'DAP Fertilizer', 400, 'kg', 80, 130),
            ('pesticide', 'Karate Insecticide', 10, 'ltr', 2, 1500),
            ('pesticide', 'Roundup Herbicide', 15, 'ltr', 3, 1200),
            ('equipment', 'Spades', 8, 'pcs', 2, 800),
            ('equipment', 'Hoes', 12, 'pcs', 3, 600),
            ('feed', 'Dairy Meal', 1000, 'kg', 200, 45),
            ('feed', 'Layers Mash', 800, 'kg', 150, 50),
            ('medicine', 'Dewormer', 5, 'ltr', 1, 3000),
            ('fuel', 'Diesel', 200, 'ltr', 50, 150),
        ]
        
        inventory = []
        for user in users:
            for category, name, base_qty, unit, reorder, base_cost in random.sample(inventory_data, min(12, len(inventory_data))):
                item = InventoryItem.objects.create(
                    user=user,
                    name=name,
                    category=category,
                    quantity=Decimal(str(base_qty * random.uniform(0.5, 1.5))),
                    unit=unit,
                    reorder_level=Decimal(str(reorder)),
                    cost_per_unit=Decimal(str(base_cost * random.uniform(0.9, 1.1))),
                    supplier=f"Supplier {random.choice(['A', 'B', 'C'])} Ltd",
                    purchase_date=self.get_random_date(10, 120),
                    location=f"Store {random.choice(['A', 'Main'])}",
                )
                inventory.append(item)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(inventory)} inventory items'))
        return inventory

    def seed_transactions(self, users, crops):
        self.stdout.write('\nSeeding transactions...')
        transactions = []
        
        for user in users:
            for _ in range(random.randint(30, 40)):
                trans_type = random.choice(['income', 'income', 'expense', 'expense', 'expense'])
                
                if trans_type == 'income':
                    category = random.choice(['crop_sale', 'livestock_sale'])
                    amount = Decimal(str(random.uniform(5000, 50000)))
                    description = f"{category.replace('_', ' ').title()} transaction"
                else:
                    category = random.choice(['seed_purchase', 'fertilizer_purchase', 'fuel', 'labor'])
                    amount = Decimal(str(random.uniform(500, 20000)))
                    description = f"{category.replace('_', ' ').title()} expense"
                
                transaction = FinancialTransaction.objects.create(
                    user=user,
                    type=trans_type,
                    category=category,
                    amount=amount,
                    date=self.get_random_date(5, 180),
                    description=description,
                    payment_method=random.choice(['Cash', 'M-Pesa', 'Bank Transfer']),
                    reference_number=f"REF-{random.randint(10000, 99999)}",
                )
                transactions.append(transaction)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(transactions)} transactions'))
        return transactions

    def seed_tasks(self, users, crops, livestock):
        self.stdout.write('\nSeeding tasks...')
        task_templates = [
            ('Apply fertilizer', 'Apply NPK fertilizer to crops', 'high'),
            ('Weed the field', 'Remove weeds from field', 'medium'),
            ('Check irrigation', 'Inspect irrigation system', 'high'),
            ('Harvest crops', 'Harvest mature crops', 'urgent'),
            ('Vaccinate animals', 'Administer vaccines', 'high'),
            ('Feed livestock', 'Provide feed and water', 'medium'),
            ('Repair equipment', 'Service farm equipment', 'medium'),
        ]
        
        tasks = []
        for user in users:
            for _ in range(random.randint(15, 20)):
                title, description, priority = random.choice(task_templates)
                status = random.choice(['pending', 'pending', 'in_progress', 'completed'])
                
                due_date = self.get_future_date(1, 60) if status != 'completed' else self.get_random_date(1, 30)
                
                task = Task.objects.create(
                    user=user,
                    title=title,
                    description=description,
                    priority=priority,
                    status=status,
                    due_date=due_date,
                    completed_date=due_date if status == 'completed' else None,
                )
                tasks.append(task)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(tasks)} tasks'))
        return tasks

    def seed_activities(self, users, crops, livestock):
        self.stdout.write('\nSeeding activities...')
        activity_templates = [
            ('planting', 'Planted seeds', 'Planted seeds in field'),
            ('irrigation', 'Irrigated crops', 'Watered crops'),
            ('fertilization', 'Applied fertilizer', 'Applied NPK fertilizer'),
            ('weeding', 'Weeding done', 'Removed weeds'),
            ('harvesting', 'Harvested crops', 'Harvested mature crops'),
            ('feeding', 'Fed animals', 'Provided feed to livestock'),
        ]
        
        activities = []
        for user in users:
            for _ in range(random.randint(20, 30)):
                activity_type, title, description = random.choice(activity_templates)
                
                date = timezone.make_aware(
                    datetime.combine(self.get_random_date(1, 90), datetime.min.time()) + 
                    timedelta(hours=random.randint(6, 18))
                )
                
                activity = Activity.objects.create(
                    user=user,
                    activity_type=activity_type,
                    title=title,
                    description=description,
                    date=date,
                    duration=random.randint(30, 240),
                    labor_cost=Decimal(str(random.uniform(200, 2000))),
                )
                activities.append(activity)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(activities)} activities'))
        return activities

    def seed_weather(self, users):
        self.stdout.write('\nSeeding weather data...')
        conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Clear']
        
        weather = []
        for user in users:
            for days_back in range(60):
                date = timezone.now().date() - timedelta(days=days_back)
                
                base_temp = random.uniform(18, 28)
                
                w = WeatherData.objects.create(
                    user=user,
                    date=date,
                    temperature_high=Decimal(str(base_temp + random.uniform(2, 8))),
                    temperature_low=Decimal(str(base_temp - random.uniform(2, 5))),
                    humidity=random.randint(40, 90),
                    rainfall=Decimal(str(random.uniform(0, 50))) if random.random() > 0.6 else Decimal('0'),
                    wind_speed=Decimal(str(random.uniform(5, 25))),
                    conditions=random.choice(conditions),
                )
                weather.append(w)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(weather)} weather records'))
        return weather
