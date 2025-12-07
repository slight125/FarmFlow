"""
Gemini AI-Powered Chatbot for FarmFlow
Provides intelligent, context-aware responses using Google's Gemini Pro
with real-time farm data synchronization
"""

import os
import google.generativeai as genai
from django.conf import settings
from .models import Crop, Livestock, FinancialTransaction, Task, InventoryItem, Activity
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, Q, F


class GeminiChatBot:
    """AI chatbot powered by Google Gemini Pro with real-time data sync"""
    
    def __init__(self, user):
        self.user = user
        self.current_time = timezone.now()
        
        # Configure Gemini API with environment variable
        import logging
        logger = logging.getLogger(__name__)
        
        api_key = os.getenv('GEMINI_API_KEY', '')
        if api_key:
            genai.configure(api_key=api_key)
            # Use Gemini 2.5 Flash - latest stable model with safety settings
            from google.generativeai.types import HarmCategory, HarmBlockThreshold
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            self.model = genai.GenerativeModel('gemini-2.5-flash', safety_settings=safety_settings)
            logger.info(f"Gemini AI initialized successfully for user: {user.username}")
        else:
            self.model = None
            logger.warning("Gemini API key not found - AI will use fallback mode")
    
    def get_farm_context(self):
        """Gather comprehensive real-time farm data for context"""
        import logging
        logger = logging.getLogger(__name__)
        
        today = self.current_time.date()
        
        context = {
            'timestamp': str(self.current_time),
            'crops': [],
            'livestock': [],
            'finances': {},
            'tasks': {},
            'inventory': [],
            'recent_activities': [],
            'statistics': {},
            'alerts': []
        }
        
        # REAL-TIME CROP DATA with detailed status (FRESH QUERY - NO CACHE)
        crops = Crop.objects.filter(user=self.user).order_by('-planting_date')
        logger.info(f"Fetching REAL-TIME crop data: {crops.count()} total crops found")
        
        crops_by_status = crops.values('status').annotate(count=Count('id'))
        context['statistics']['crops_by_status'] = {item['status']: item['count'] for item in crops_by_status}
        
        # Include ALL crops for accurate AI responses
        for crop in crops:  # All crops, not limited
            days_to_harvest = crop.days_to_harvest
            context['crops'].append({
                'name': crop.name,
                'variety': crop.variety,
                'status': crop.status,
                'area': float(crop.area),
                'planting_date': str(crop.planting_date),
                'expected_harvest': str(crop.expected_harvest_date),
                'days_to_harvest': days_to_harvest,
                'expected_yield': float(crop.expected_yield) if crop.expected_yield else None,
                'actual_yield': float(crop.actual_yield) if crop.actual_yield else None,
                'notes': crop.notes[:100] if crop.notes else None,
                'last_updated': str(crop.updated_at)
            })
            
            # Add harvest alerts
            if days_to_harvest <= 7 and days_to_harvest >= 0 and crop.status == 'growing':
                context['alerts'].append(f"⚠️ {crop.name} ready for harvest in {days_to_harvest} days")
            elif days_to_harvest < 0 and crop.status == 'growing':
                context['alerts'].append(f"🔴 URGENT: {crop.name} harvest overdue by {abs(days_to_harvest)} days")
        
        # REAL-TIME LIVESTOCK DATA with health tracking
        livestock = Livestock.objects.filter(user=self.user).order_by('-created_at')
        
        livestock_by_status = livestock.values('status').annotate(count=Count('id'))
        context['statistics']['livestock_by_status'] = {item['status']: item['count'] for item in livestock_by_status}
        
        # Include ALL livestock for accurate AI responses
        for animal in livestock:  # All animals, not limited
            animal_data = {
                'type': animal.type,
                'breed': animal.breed,
                'status': animal.status,
                'tag': animal.tag_number,
                'gender': animal.gender,
                'weight': float(animal.weight) if animal.weight else None,
                'purchase_price': float(animal.purchase_price) if animal.purchase_price else None,
                'current_value': float(animal.current_value) if animal.current_value else None,
                'date_acquired': str(animal.date_acquired),
                'notes': animal.notes[:100] if animal.notes else None
            }
            
            if animal.date_of_birth:
                age_days = (today - animal.date_of_birth).days
                animal_data['age_days'] = age_days
                animal_data['age_months'] = age_days // 30
            
            context['livestock'].append(animal_data)
            
            # Add health alerts
            if animal.status in ['sick', 'under_treatment']:
                context['alerts'].append(f"🔴 {animal.breed} {animal.type} (Tag: {animal.tag_number}) needs medical attention")
        
        # REAL-TIME FINANCIAL DATA with trends
        month_start = today.replace(day=1)
        week_ago = today - timedelta(days=7)
        
        # Current month
        month_income = FinancialTransaction.objects.filter(
            user=self.user,
            type='income',
            date__gte=month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        month_expenses = FinancialTransaction.objects.filter(
            user=self.user,
            type='expense',
            date__gte=month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Last week
        week_income = FinancialTransaction.objects.filter(
            user=self.user,
            type='income',
            date__gte=week_ago
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        week_expenses = FinancialTransaction.objects.filter(
            user=self.user,
            type='expense',
            date__gte=week_ago
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Recent transactions
        recent_transactions = FinancialTransaction.objects.filter(
            user=self.user
        ).order_by('-date')[:10]
        
        context['finances'] = {
            'month': {
                'income': float(month_income),
                'expenses': float(month_expenses),
                'net': float(month_income - month_expenses)
            },
            'week': {
                'income': float(week_income),
                'expenses': float(week_expenses),
                'net': float(week_income - week_expenses)
            },
            'recent_transactions': [
                {
                    'type': t.type,
                    'amount': float(t.amount),
                    'category': t.category,
                    'date': str(t.date),
                    'description': t.description[:50] if t.description else None
                }
                for t in recent_transactions
            ]
        }
        
        # Financial alerts
        if month_expenses > month_income:
            deficit = month_expenses - month_income
            context['alerts'].append(f"⚠️ Monthly deficit: ${deficit:.2f}")
        
        # REAL-TIME TASK DATA with priorities
        pending_tasks = Task.objects.filter(
            user=self.user,
            status='pending'
        ).order_by('due_date')
        
        overdue_tasks = pending_tasks.filter(due_date__lt=today)
        urgent_tasks = pending_tasks.filter(due_date__lte=today + timedelta(days=3))
        
        context['tasks'] = {
            'pending_count': pending_tasks.count(),
            'overdue_count': overdue_tasks.count(),
            'urgent_count': urgent_tasks.count(),
            'pending': [
                {
                    'title': task.title,
                    'description': task.description[:100] if task.description else None,
                    'due_date': str(task.due_date),
                    'priority': task.priority,
                    'days_until_due': (task.due_date - today).days,
                    'is_overdue': task.due_date < today
                }
                for task in pending_tasks[:15]  # Show more tasks
            ]
        }
        
        # Task alerts
        if overdue_tasks.exists():
            context['alerts'].append(f"🔴 URGENT: {overdue_tasks.count()} overdue tasks")
        
        # REAL-TIME INVENTORY with stock levels
        all_inventory = InventoryItem.objects.filter(user=self.user)
        low_stock = all_inventory.filter(quantity__lte=F('reorder_level'))
        out_of_stock = all_inventory.filter(quantity=0)
        
        context['inventory'] = {
            'total_items': all_inventory.count(),
            'low_stock_count': low_stock.count(),
            'out_of_stock_count': out_of_stock.count(),
            'items': [
                {
                    'name': item.name,
                    'quantity': float(item.quantity),
                    'unit': item.unit,
                    'reorder_level': float(item.reorder_level),
                    'is_low': item.quantity <= item.reorder_level,
                    'last_updated': str(item.updated_at)
                }
                for item in all_inventory.order_by('quantity')[:15]  # Show more inventory items
            ]
        }
        
        # Inventory alerts
        if out_of_stock.exists():
            for item in out_of_stock[:3]:
                context['alerts'].append(f"🔴 OUT OF STOCK: {item.name}")
        elif low_stock.exists():
            for item in low_stock[:3]:
                context['alerts'].append(f"⚠️ Low stock: {item.name} ({item.quantity} {item.unit})")
        
        # RECENT ACTIVITIES for context awareness
        recent_activities = Activity.objects.filter(
            user=self.user
        ).order_by('-date')[:15]
        
        context['recent_activities'] = [
            {
                'title': activity.title,
                'description': activity.description[:100] if activity.description else None,
                'date': str(activity.date),
                'category': activity.activity_type
            }
            for activity in recent_activities
        ]
        
        # OVERALL STATISTICS
        context['statistics']['total_crops'] = crops.count()
        context['statistics']['total_livestock'] = livestock.count()
        context['statistics']['total_tasks'] = Task.objects.filter(user=self.user).count()
        context['statistics']['completed_tasks'] = Task.objects.filter(user=self.user, status='completed').count()
        
        return context
    
    def get_response(self, user_message):
        """Get AI response using Gemini Pro"""
        
        if not self.model:
            return {
                'type': 'error',
                'message': 'Gemini API key not configured. Please add GEMINI_API_KEY to your .env file.',
                'suggestions': ['How to get Gemini API key?']
            }
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            # Get REAL-TIME farm context (fresh data every request - NO CACHING)
            farm_context = self.get_farm_context()
            
            logger.info(f"AI Context: {farm_context['statistics']['total_crops']} crops, "
                       f"{farm_context['statistics']['total_livestock']} livestock, "
                       f"{farm_context['tasks']['pending_count']} pending tasks")
            
            # Build concise prompt with key farm data
            crop_summary = ', '.join([f"{c['name']}" for c in farm_context['crops'][:5]])
            livestock_summary = ', '.join([f"{l['breed']} {l['type']}" for l in farm_context['livestock'][:5]])
            
            system_prompt = f"""You are FarmFlow AI Assistant, an expert agricultural advisor.

FARM DATA SUMMARY:
- You have {farm_context['statistics']['total_crops']} crops: {crop_summary}{' and more' if len(farm_context['crops']) > 5 else ''}
- You have {farm_context['statistics']['total_livestock']} animals: {livestock_summary}{' and more' if len(farm_context['livestock']) > 5 else ''}
- Tasks: {farm_context['tasks']['pending_count']} pending, {farm_context['tasks']['overdue_count']} overdue
- Finances this month: ${farm_context['finances']['month']['income']:.0f} income, ${farm_context['finances']['month']['expenses']:.0f} expenses

ALERTS: {', '.join(farm_context['alerts'][:3]) if farm_context['alerts'] else 'None'}

USER QUESTION: {user_message}

INSTRUCTIONS:
1. CRITICAL: Always use the EXACT numbers from the FARM OVERVIEW section (e.g., if it says "11 active crops", you must say 11, not 8 or any other number)
2. Provide specific, actionable advice based on the farm's ACTUAL REAL-TIME data shown above
3. Be concise and clear (2-4 well-structured paragraphs)
4. Use emojis sparingly for clarity (e.g., ✅, 🌾, 💰, ⚠️)
5. Apply agricultural best practices and modern farming techniques
6. Consider seasons, weather, and timing when relevant
7. Prioritize practical, implementable solutions
8. Reference specific crops, livestock, or data points when answering
9. If the data is limited, acknowledge it and provide general best practices
10. Be conversational but professional
11. Structure your response with clear paragraph breaks (use \n\n between paragraphs)

USER QUESTION: {user_message}

Provide a helpful, expert response that directly addresses their question using their farm's real-time data:"""

            # Configure generation parameters for better responses
            generation_config = {
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40,
                'max_output_tokens': 800,
            }

            # Generate response using Gemini
            response = self.model.generate_content(
                system_prompt,
                generation_config=generation_config
            )
            
            # Check if response has valid content
            if not response.parts:
                logger.warning(f"Gemini returned no content. Finish reason: {response.candidates[0].finish_reason}")
                return {
                    'type': 'error',
                    'message': "I apologize, but I need to rephrase my response. Could you please ask your question in a different way?",
                    'suggestions': ['How many crops do I have?', 'Show livestock status', 'Financial summary']
                }
            
            # Clean and format the response
            response_text = response.text.strip()
            
            # Extract suggestions from response
            suggestions = self._extract_suggestions(response_text, user_message)
            
            return {
                'type': 'gemini',
                'message': response_text,
                'suggestions': suggestions
            }
            
        except Exception as e:
            # Fallback to basic response
            return {
                'type': 'error',
                'message': f'AI Assistant temporarily unavailable. Error: {str(e)}',
                'suggestions': ['Try again', 'View dashboard', 'Check farm data']
            }
    
    def _format_alerts(self, alerts):
        """Format urgent alerts"""
        if not alerts:
            return "  ✅ No urgent alerts - Farm operations running smoothly"
        return "\n".join([f"  {alert}" for alert in alerts])
    
    def _format_crops_detailed(self, crops):
        """Format detailed crop data with real-time info"""
        if not crops:
            return "  No crops currently being tracked"
        
        lines = []
        for crop in crops:
            status_emoji = {'planned': '📋', 'planted': '🌱', 'growing': '🌿', 'harvested': '✅', 'sold': '💰'}
            emoji = status_emoji.get(crop['status'], '🌾')
            
            line = f"  {emoji} {crop['name']} ({crop['variety']}): {crop['status'].upper()}"
            line += f"\n     Area: {crop['area']} acres | Planted: {crop['planting_date']}"
            line += f"\n     Harvest: {crop['expected_harvest']} ({crop['days_to_harvest']} days)"
            
            if crop.get('expected_yield'):
                line += f" | Expected Yield: {crop['expected_yield']} kg"
            if crop.get('actual_yield'):
                line += f" | Actual Yield: {crop['actual_yield']} kg"
            if crop.get('notes'):
                line += f"\n     Notes: {crop['notes']}"
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def _format_livestock_detailed(self, livestock):
        """Format detailed livestock data with real-time health info"""
        if not livestock:
            return "  No livestock currently being tracked"
        
        lines = []
        for animal in livestock:
            status_emoji = {'healthy': '✅', 'sick': '🔴', 'under_treatment': '🏥', 'pregnant': '🤰', 'sold': '💰', 'deceased': '💀'}
            emoji = status_emoji.get(animal['status'], '🐄')
            
            line = f"  {emoji} {animal['breed']} {animal['type']} (Tag: {animal['tag']}): {animal['status'].upper()}"
            line += f"\n     Gender: {animal['gender']} | Acquired: {animal['date_acquired']}"
            
            if animal.get('weight'):
                line += f" | Weight: {animal['weight']} kg"
            if animal.get('age_months'):
                line += f" | Age: {animal['age_months']} months"
            if animal.get('current_value'):
                line += f"\n     Current Value: ${animal['current_value']}"
            if animal.get('notes'):
                line += f"\n     Notes: {animal['notes']}"
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def _format_transactions(self, transactions):
        """Format recent financial transactions"""
        if not transactions:
            return "  No recent transactions"
        
        lines = []
        for t in transactions:
            emoji = '💰' if t['type'] == 'income' else '💸'
            lines.append(f"  {emoji} ${t['amount']:.2f} - {t['category']} ({t['date']})")
            if t.get('description'):
                lines.append(f"     {t['description']}")
        
        return "\n".join(lines)
    
    def _format_tasks_detailed(self, tasks):
        """Format detailed task data with urgency"""
        if not tasks:
            return "  No pending tasks"
        
        lines = []
        for task in tasks:
            if task['is_overdue']:
                emoji = '🔴 OVERDUE'
            elif task['days_until_due'] <= 1:
                emoji = '⚠️ TODAY/TOMORROW'
            elif task['days_until_due'] <= 3:
                emoji = '🟡 URGENT'
            else:
                emoji = '🟢'
            
            line = f"  {emoji} {task['title']} - Due: {task['due_date']} ({task['priority']} priority)"
            if task['days_until_due'] >= 0:
                line += f" | {task['days_until_due']} days left"
            else:
                line += f" | {abs(task['days_until_due'])} days overdue"
            
            if task.get('description'):
                line += f"\n     {task['description']}"
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def _format_inventory_detailed(self, inventory):
        """Format detailed inventory with stock status"""
        if not inventory:
            return "  All inventory levels adequate"
        
        lines = []
        for item in inventory:
            if item['is_low']:
                emoji = '🔴' if item['quantity'] == 0 else '⚠️'
            else:
                emoji = '✅'
            
            line = f"  {emoji} {item['name']}: {item['quantity']} {item['unit']}"
            line += f" (reorder at {item['reorder_level']})"
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def _format_activities(self, activities):
        """Format recent activities"""
        if not activities:
            return "  No recent activities logged"
        
        lines = []
        for activity in activities:
            lines.append(f"  • {activity['date']}: {activity['title']} ({activity['category']})")
            if activity.get('description'):
                lines.append(f"    {activity['description']}")
        
        return "\n".join(lines)
    
    def _extract_suggestions(self, response_text, original_question):
        """Extract or generate relevant follow-up suggestions"""
        
        # Smart suggestions based on question keywords
        keywords = original_question.lower()
        suggestions = []
        
        if 'crop' in keywords or 'plant' in keywords or 'harvest' in keywords:
            suggestions = [
                'Show crop health details',
                'Harvest timing recommendations',
                'Pest and disease prevention tips'
            ]
        elif 'livestock' in keywords or 'animal' in keywords or 'cattle' in keywords:
            suggestions = [
                'Livestock feeding schedule',
                'Vaccination and health checkups',
                'Breeding management advice'
            ]
        elif 'financ' in keywords or 'money' in keywords or 'profit' in keywords:
            suggestions = [
                'Cost reduction strategies',
                'Revenue optimization tips',
                'Investment recommendations'
            ]
        elif 'task' in keywords or 'schedule' in keywords or 'plan' in keywords:
            suggestions = [
                'Prioritize urgent tasks',
                'Create weekly plan',
                'Task automation ideas'
            ]
        elif 'weather' in keywords or 'rain' in keywords or 'season' in keywords:
            suggestions = [
                'Seasonal planning advice',
                'Weather-based activities',
                'Climate adaptation strategies'
            ]
        else:
            suggestions = [
                'Tell me about my farm performance',
                'What should I focus on today?',
                'Any urgent issues to address?'
            ]
        
        return suggestions[:3]  # Return max 3 suggestions


# Import models at the end to avoid circular imports
from django.db import models
