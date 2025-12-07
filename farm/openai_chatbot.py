"""
OpenAI-Powered Chatbot for FarmFlow
Provides intelligent, context-aware responses using OpenAI GPT models
with real-time farm data synchronization
"""

import os
from openai import OpenAI
from django.conf import settings
from .models import Crop, Livestock, FinancialTransaction, Task, InventoryItem, Activity
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, Q, F
import logging

logger = logging.getLogger(__name__)


class OpenAIChatBot:
    """AI chatbot powered by OpenAI with real-time data sync"""
    
    def __init__(self, user):
        self.user = user
        self.current_time = timezone.now()
        
        # Configure OpenAI API
        api_key = os.getenv('OPENAI_API_KEY', '').strip()
        if api_key and not api_key.startswith('#'):
            try:
                self.client = OpenAI(api_key=api_key)
                logger.info(f"OpenAI initialized successfully for user: {user.username}")
            except Exception as e:
                self.client = None
                logger.warning(f"OpenAI initialization failed: {str(e)}")
        else:
            self.client = None
            logger.info("OpenAI API key not configured - using fallback AI")
    
    def get_farm_context(self):
        """Gather comprehensive real-time farm data for context"""
        today = self.current_time.date()
        
        context_parts = []
        
        # CROP DATA
        crops = Crop.objects.filter(user=self.user).order_by('-planting_date')
        if crops.exists():
            context_parts.append(f"\n📊 CROPS ({crops.count()} total):")
            crops_by_status = {}
            for crop in crops[:15]:  # Top 15 crops
                status = crop.status
                crops_by_status[status] = crops_by_status.get(status, 0) + 1
                
                days_to_harvest = crop.days_to_harvest
                harvest_info = f"Ready in {days_to_harvest} days" if days_to_harvest > 0 else f"OVERDUE by {abs(days_to_harvest)} days"
                
                context_parts.append(
                    f"  • {crop.name} ({crop.variety}): {status.upper()}, "
                    f"{crop.area} hectares, Planted: {crop.planting_date}, "
                    f"{harvest_info}"
                )
            
            context_parts.append(f"\nStatus Summary: {dict(crops_by_status)}")
        else:
            context_parts.append("\n📊 CROPS: No crops registered yet")
        
        # LIVESTOCK DATA
        livestock = Livestock.objects.filter(user=self.user).order_by('-created_at')
        if livestock.exists():
            context_parts.append(f"\n🐄 LIVESTOCK ({livestock.count()} total):")
            livestock_by_type = {}
            livestock_by_status = {}
            
            for animal in livestock[:15]:  # Top 15 animals
                livestock_by_type[animal.type] = livestock_by_type.get(animal.type, 0) + 1
                livestock_by_status[animal.status] = livestock_by_status.get(animal.status, 0) + 1
                
                age_days = (today - animal.date_of_birth).days if animal.date_of_birth else None
                age_info = f", Age: {age_days // 365}y {(age_days % 365) // 30}m" if age_days else ""
                
                context_parts.append(
                    f"  • {animal.type.title()} - {animal.breed} (#{animal.tag_number}): "
                    f"{animal.status.upper()}{age_info}, Weight: {animal.weight}kg"
                )
            
            context_parts.append(f"\nType Summary: {dict(livestock_by_type)}")
            context_parts.append(f"Status Summary: {dict(livestock_by_status)}")
        else:
            context_parts.append("\n🐄 LIVESTOCK: No livestock registered yet")
        
        # FINANCIAL DATA
        thirty_days_ago = self.current_time - timedelta(days=30)
        transactions = FinancialTransaction.objects.filter(
            user=self.user,
            date__gte=thirty_days_ago
        )
        
        if transactions.exists():
            income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
            expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
            balance = income - expense
            
            context_parts.append(f"\n💰 FINANCES (Last 30 days):")
            context_parts.append(f"  • Total Income: ${income:,.2f}")
            context_parts.append(f"  • Total Expenses: ${expense:,.2f}")
            context_parts.append(f"  • Net Balance: ${balance:,.2f}")
            
            # Recent transactions
            recent = transactions.order_by('-date')[:5]
            context_parts.append("\n  Recent Transactions:")
            for trans in recent:
                symbol = "+" if trans.type == 'income' else "-"
                context_parts.append(f"    {symbol} ${trans.amount:,.2f} - {trans.category} ({trans.date})")
        else:
            context_parts.append("\n💰 FINANCES: No financial records yet")
        
        # TASKS
        tasks = Task.objects.filter(user=self.user)
        pending_tasks = tasks.filter(status='pending')
        overdue_tasks = tasks.filter(due_date__lt=today, status='pending')
        
        if tasks.exists():
            context_parts.append(f"\n✅ TASKS:")
            context_parts.append(f"  • Total: {tasks.count()}")
            context_parts.append(f"  • Pending: {pending_tasks.count()}")
            context_parts.append(f"  • Overdue: {overdue_tasks.count()}")
            
            if overdue_tasks.exists():
                context_parts.append("\n  🔴 OVERDUE TASKS:")
                for task in overdue_tasks[:5]:
                    days_overdue = (today - task.due_date).days
                    context_parts.append(f"    • {task.title} (Due: {task.due_date}, {days_overdue} days overdue)")
        else:
            context_parts.append("\n✅ TASKS: No tasks created yet")
        
        # INVENTORY
        inventory = InventoryItem.objects.filter(user=self.user)
        low_stock = inventory.filter(quantity__lte=F('reorder_level'))
        
        if inventory.exists():
            context_parts.append(f"\n📦 INVENTORY:")
            context_parts.append(f"  • Total Items: {inventory.count()}")
            context_parts.append(f"  • Low Stock Items: {low_stock.count()}")
            
            if low_stock.exists():
                context_parts.append("\n  ⚠️ LOW STOCK ALERTS:")
                for item in low_stock[:5]:
                    context_parts.append(f"    • {item.name}: {item.quantity} {item.unit} (Reorder at: {item.reorder_level})")
        else:
            context_parts.append("\n📦 INVENTORY: No inventory items yet")
        
        return "\n".join(context_parts)
    
    def get_response(self, user_message):
        """Generate AI response using OpenAI"""
        try:
            if not self.client:
                raise Exception("OpenAI API key not configured")
            
            # Get farm context
            farm_context = self.get_farm_context()
            
            # Create system prompt
            system_prompt = f"""You are FarmFlow AI Assistant, an intelligent farming companion helping {self.user.first_name or self.user.username} manage their farm.

Current Date & Time: {self.current_time.strftime('%B %d, %Y at %I:%M %p')}

REAL-TIME FARM DATA:
{farm_context}

YOUR ROLE:
- Provide helpful, accurate advice based on the REAL-TIME data above
- Be conversational, friendly, and supportive
- Use emojis appropriately to make responses engaging
- Provide specific recommendations based on their farm's current state
- Alert them to urgent issues (overdue tasks, harvest dates, low inventory)
- Answer questions about their crops, livestock, finances, and tasks
- Give actionable next steps when relevant

RESPONSE STYLE:
- Be concise but informative
- Use bullet points for clarity
- Highlight urgent matters
- End with helpful suggestions when appropriate"""

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-4o-mini for cost-effectiveness and speed
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            ai_message = response.choices[0].message.content
            
            # Generate contextual suggestions
            suggestions = self._generate_suggestions(user_message, ai_message)
            
            return {
                'message': ai_message,
                'suggestions': suggestions,
                'type': 'success'
            }
            
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            raise
    
    def _generate_suggestions(self, user_message, ai_response):
        """Generate contextual follow-up suggestions"""
        suggestions = []
        
        user_msg_lower = user_message.lower()
        
        if any(word in user_msg_lower for word in ['crop', 'plant', 'harvest', 'grow']):
            suggestions = ['Show livestock status', 'Financial summary', 'Task priorities']
        elif any(word in user_msg_lower for word in ['livestock', 'animal', 'cattle', 'chicken']):
            suggestions = ['Crop health check', 'Inventory status', 'Financial overview']
        elif any(word in user_msg_lower for word in ['money', 'finance', 'cost', 'income', 'expense']):
            suggestions = ['Crop profitability', 'Upcoming expenses', 'Revenue forecast']
        elif any(word in user_msg_lower for word in ['task', 'todo', 'schedule', 'plan']):
            suggestions = ['Show overdue tasks', 'Today\'s priorities', 'Weekly schedule']
        elif any(word in user_msg_lower for word in ['inventory', 'stock', 'supply']):
            suggestions = ['Low stock items', 'Recent purchases', 'Reorder list']
        else:
            suggestions = ['Show dashboard insights', 'What needs attention?', 'Farm summary']
        
        return suggestions[:4]  # Return max 4 suggestions
