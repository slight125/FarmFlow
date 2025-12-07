"""
AI Chat Integration for FarmFlow
Provides conversational AI assistance for farmers
"""

class FarmAIChatBot:
    """AI-powered chatbot for farm management assistance"""
    
    def __init__(self, user):
        self.user = user
        self.conversation_history = []
    
    def get_response(self, user_message):
        """Generate AI response based on user query"""
        # Convert message to lowercase for better matching
        message_lower = user_message.lower()
        
        # Intent classification
        if any(word in message_lower for word in ['crop', 'plant', 'harvest', 'seed']):
            return self._handle_crop_query(message_lower)
        
        elif any(word in message_lower for word in ['livestock', 'animal', 'cattle', 'chicken', 'goat']):
            return self._handle_livestock_query(message_lower)
        
        elif any(word in message_lower for word in ['money', 'finance', 'profit', 'expense', 'income', 'cost']):
            return self._handle_financial_query(message_lower)
        
        elif any(word in message_lower for word in ['task', 'todo', 'schedule', 'reminder']):
            return self._handle_task_query(message_lower)
        
        elif any(word in message_lower for word in ['weather', 'rain', 'temperature', 'climate']):
            return self._handle_weather_query(message_lower)
        
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return self._handle_greeting()
        
        elif any(word in message_lower for word in ['help', 'assist', 'support']):
            return self._handle_help_request()
        
        else:
            return self._handle_general_query(user_message)
    
    def _handle_crop_query(self, message):
        """Handle crop-related queries"""
        from .models import Crop
        
        crops_count = Crop.objects.filter(user=self.user).count()
        active_crops = Crop.objects.filter(user=self.user, status='growing').count()
        
        if 'how many' in message or 'count' in message:
            return {
                'type': 'info',
                'message': f"You currently have {crops_count} total crops, with {active_crops} actively growing. Would you like detailed information about any specific crop?",
                'suggestions': ['Show me my crops', 'Add new crop', 'Crop care tips']
            }
        
        if 'add' in message or 'new' in message:
            return {
                'type': 'action',
                'message': "I can help you add a new crop! Here's what you'll need: crop type, planting date, expected harvest date, and area. Click below to get started.",
                'suggestions': ['Go to add crop', 'What crops grow well now?', 'Show growing guide']
            }
        
        if 'care' in message or 'tips' in message or 'help' in message:
            return {
                'type': 'advice',
                'message': "Here are AI-powered crop care tips:\n\n1. **Watering**: Check soil moisture daily, water early morning or evening\n2. **Fertilization**: Apply balanced nutrients every 2-3 weeks\n3. **Pest Control**: Inspect weekly for signs of pests or disease\n4. **Monitoring**: Track growth stages and adjust care accordingly",
                'suggestions': ['Pest identification', 'Fertilizer recommendations', 'Watering schedule']
            }
        
        return {
            'type': 'info',
            'message': f"You have {active_crops} active crops. I can help you with planting schedules, care recommendations, pest management, and harvest predictions. What would you like to know?",
            'suggestions': ['View my crops', 'Best planting time', 'Harvest predictions']
        }
    
    def _handle_livestock_query(self, message):
        """Handle livestock-related queries"""
        from .models import Livestock
        
        livestock_count = Livestock.objects.filter(user=self.user).count()
        healthy_count = Livestock.objects.filter(user=self.user, status='healthy').count()
        
        if 'health' in message or 'sick' in message:
            return {
                'type': 'health',
                'message': f"Livestock Health Report: {healthy_count} out of {livestock_count} animals are in healthy condition. Regular veterinary checkups are recommended every 3-6 months.",
                'suggestions': ['View livestock details', 'Schedule vet visit', 'Health tracking tips']
            }
        
        if 'feed' in message or 'nutrition' in message:
            return {
                'type': 'advice',
                'message': "Optimal Feeding Guidelines:\n\n• Provide balanced diet based on animal type and age\n• Ensure clean water is always available\n• Adjust portions based on season and activity\n• Include minerals and supplements as needed",
                'suggestions': ['Feeding schedule', 'Nutritional requirements', 'Feed costs']
            }
        
        return {
            'type': 'info',
            'message': f"You're managing {livestock_count} animals. I can assist with health monitoring, feeding schedules, breeding management, and production tracking. How can I help?",
            'suggestions': ['Add animal', 'Health checkup reminders', 'Breeding calendar']
        }
    
    def _handle_financial_query(self, message):
        """Handle financial queries"""
        from .models import FinancialTransaction
        from django.db.models import Sum
        from django.utils import timezone
        from datetime import timedelta
        
        # Get last 30 days data
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        income = FinancialTransaction.objects.filter(
            user=self.user, type='income', date__gte=thirty_days_ago
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expenses = FinancialTransaction.objects.filter(
            user=self.user, type='expense', date__gte=thirty_days_ago
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        profit = income - expenses
        
        if 'profit' in message or 'earning' in message:
            return {
                'type': 'financial',
                'message': f"Financial Summary (Last 30 days):\n\n💰 Income: KSh {income:,.2f}\n💸 Expenses: KSh {expenses:,.2f}\n📊 Net Profit: KSh {profit:,.2f}\n\nYour profit margin is {(profit/income*100 if income > 0 else 0):.1f}%",
                'suggestions': ['View detailed report', 'Add transaction', 'Cost reduction tips']
            }
        
        if 'save' in message or 'reduce' in message or 'cut' in message:
            return {
                'type': 'advice',
                'message': "AI Cost Optimization Suggestions:\n\n1. Review recurring expenses for negotiation opportunities\n2. Bulk purchase inputs during off-season\n3. Implement efficient irrigation to reduce water costs\n4. Use organic fertilizers to cut chemical costs\n5. Optimize feed management to minimize waste",
                'suggestions': ['Expense breakdown', 'Budget planning', 'Investment ideas']
            }
        
        return {
            'type': 'financial',
            'message': f"Your farm's financial health looks {'good' if profit > 0 else 'concerning'}. Last 30 days: KSh {income:,.0f} income, KSh {expenses:,.0f} expenses. I can help with budgeting, forecasting, and optimization.",
            'suggestions': ['Monthly report', 'Add expense', 'Financial forecast']
        }
    
    def _handle_task_query(self, message):
        """Handle task management queries"""
        from .models import Task
        from django.utils import timezone
        
        pending = Task.objects.filter(user=self.user, status='pending').count()
        overdue = Task.objects.filter(
            user=self.user, status='pending', due_date__lt=timezone.now().date()
        ).count()
        
        if overdue > 0:
            return {
                'type': 'alert',
                'message': f"⚠️ Task Alert: You have {overdue} overdue tasks and {pending-overdue} pending tasks. Prioritize completion to maintain farm efficiency.",
                'suggestions': ['View overdue tasks', 'Create new task', 'Task prioritization tips']
            }
        
        return {
            'type': 'info',
            'message': f"You have {pending} pending tasks. I can help you create tasks, set reminders, prioritize activities, and track completion. Stay organized!",
            'suggestions': ['Create task', 'View calendar', 'Smart scheduling']
        }
    
    def _handle_weather_query(self, message):
        """Handle weather-related queries"""
        return {
            'type': 'weather',
            'message': "Weather Intelligence:\n\nBased on current patterns, here are my recommendations:\n\n🌤️ **Today**: Good conditions for field work\n💧 **Irrigation**: Check soil moisture, may need watering\n🌱 **Planting**: Suitable for cool-season crops\n🚜 **Activities**: Ideal for harvesting and outdoor tasks",
            'suggestions': ['7-day forecast', 'Irrigation schedule', 'Planting calendar']
        }
    
    def _handle_greeting(self):
        """Handle greetings"""
        import random
        
        greetings = [
            "Hello! 👋 I'm your AI farm assistant. How can I help optimize your farm today?",
            "Hi there! 🌱 Ready to make your farm more productive? Ask me anything!",
            "Greetings! 🚜 I'm here to provide intelligent insights for your farm. What would you like to know?"
        ]
        
        return {
            'type': 'greeting',
            'message': random.choice(greetings),
            'suggestions': ['Show dashboard insights', 'Financial summary', 'Task recommendations', 'Crop care tips']
        }
    
    def _handle_help_request(self):
        """Handle help requests"""
        return {
            'type': 'help',
            'message': "I'm your AI-powered farm assistant! Here's what I can help you with:\n\n🌾 **Crops**: Planting schedules, care tips, pest management\n🐄 **Livestock**: Health monitoring, feeding guides, breeding\n💰 **Finances**: Profit analysis, budgeting, cost optimization\n✅ **Tasks**: Smart scheduling, reminders, prioritization\n🌤️ **Weather**: Forecasts, irrigation timing, activity planning\n\nJust ask me anything about your farm!",
            'suggestions': ['How many crops do I have?', 'Show my financial status', 'What tasks are pending?', 'Livestock health check']
        }
    
    def _handle_general_query(self, message):
        """Handle general queries"""
        return {
            'type': 'info',
            'message': "I'm learning to understand your question better. Could you rephrase it or choose from these common topics?",
            'suggestions': ['Crop management', 'Livestock care', 'Financial tracking', 'Task planning', 'Get help']
        }
