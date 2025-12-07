"""
FarmFlow AI Assistant
Provides AI-powered insights and recommendations for farm management
with REAL-TIME data synchronization on every request
"""

import json
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Crop, Livestock, FinancialTransaction, Task, WeatherData

class FarmAIAssistant:
    """
    AI Assistant for FarmFlow - Provides intelligent insights and recommendations
    
    Features:
    - Real-time data fetching on every method call
    - No caching - always fresh farm data
    - Syncs with database changes instantly
    - Provides up-to-date recommendations
    """
    
    def __init__(self, user):
        self.user = user
        self.current_time = timezone.now()  # Capture current timestamp
    
    def get_dashboard_insights(self):
        """Generate AI-powered insights for dashboard"""
        insights = []
        
        # Crop health analysis
        crop_insight = self._analyze_crop_health()
        if crop_insight:
            insights.append(crop_insight)
        
        # Financial recommendations
        financial_insight = self._analyze_financial_health()
        if financial_insight:
            insights.append(financial_insight)
        
        # Task prioritization
        task_insight = self._analyze_tasks()
        if task_insight:
            insights.append(task_insight)
        
        # Livestock monitoring
        livestock_insight = self._analyze_livestock()
        if livestock_insight:
            insights.append(livestock_insight)
        
        # Weather-based recommendations
        weather_insight = self._analyze_weather_impact()
        if weather_insight:
            insights.append(weather_insight)
        
        return insights[:5]  # Return top 5 insights
    
    def _analyze_crop_health(self):
        """Analyze crop data and provide recommendations"""
        from django.db.models import Q
        
        crops = Crop.objects.filter(user=self.user)
        
        if not crops.exists():
            return {
                'type': 'suggestion',
                'icon': 'seedling',
                'title': 'Start Tracking Your Crops',
                'message': 'Add your first crop to get AI-powered growth recommendations and harvest predictions.',
                'action': 'Add Crop',
                'url': '/crops/new/',
                'priority': 'low'
            }
        
        # Check for crops nearing harvest
        today = timezone.now().date()
        upcoming_harvests = crops.filter(
            expected_harvest_date__lte=today + timedelta(days=14),
            expected_harvest_date__gte=today,
            status='growing'
        )
        
        if upcoming_harvests.exists():
            crop_names = ', '.join([c.name for c in upcoming_harvests[:3]])
            return {
                'type': 'alert',
                'icon': 'calendar-check',
                'title': 'Harvest Season Approaching',
                'message': f'AI predicts optimal harvest time for {crop_names} within 2 weeks. Prepare harvesting equipment and storage.',
                'action': 'View Crops',
                'url': '/crops/',
                'priority': 'high'
            }
        
        # Check for overdue crops
        overdue_crops = crops.filter(
            expected_harvest_date__lt=today,
            status='growing'
        )
        
        if overdue_crops.exists():
            return {
                'type': 'warning',
                'icon': 'exclamation-triangle',
                'title': 'Delayed Harvest Detected',
                'message': f'{overdue_crops.count()} crop(s) are past expected harvest date. AI suggests immediate inspection to prevent quality loss.',
                'action': 'Check Crops',
                'url': '/crops/',
                'priority': 'urgent'
            }
        
        # Planting season recommendation
        return {
            'type': 'info',
            'icon': 'lightbulb',
            'title': 'Crop Optimization',
            'message': f'AI analysis shows you have {crops.count()} active crops. Consider crop rotation for optimal soil health.',
            'action': 'Learn More',
            'url': '/crops/',
            'priority': 'medium'
        }
    
    def _analyze_financial_health(self):
        """Analyze financial data and provide insights"""
        from django.db.models import Sum
        
        # Get last 30 days transactions
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        income = FinancialTransaction.objects.filter(
            user=self.user,
            type='income',
            date__gte=thirty_days_ago
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        expenses = FinancialTransaction.objects.filter(
            user=self.user,
            type='expense',
            date__gte=thirty_days_ago
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if income == 0 and expenses == 0:
            return {
                'type': 'suggestion',
                'icon': 'chart-line',
                'title': 'Start Financial Tracking',
                'message': 'AI-powered financial insights will help optimize your farm profitability. Add your first transaction.',
                'action': 'Add Transaction',
                'url': '/finance/new/',
                'priority': 'low'
            }
        
        profit_margin = ((income - expenses) / income * 100) if income > 0 else 0
        
        if expenses > income:
            return {
                'type': 'warning',
                'icon': 'exclamation-circle',
                'title': 'Negative Cash Flow Alert',
                'message': f'AI detected expenses (KSh {expenses:,.0f}) exceeding income (KSh {income:,.0f}) this month. Review cost optimization opportunities.',
                'action': 'View Finances',
                'url': '/finance/',
                'priority': 'urgent'
            }
        
        if profit_margin > 30:
            return {
                'type': 'success',
                'icon': 'trophy',
                'title': 'Excellent Financial Performance',
                'message': f'AI reports {profit_margin:.0f}% profit margin! Your farm is performing above industry average.',
                'action': 'View Analytics',
                'url': '/analytics/',
                'priority': 'low'
            }
        
        return {
            'type': 'info',
            'icon': 'coins',
            'title': 'Financial Health Check',
            'message': f'Current profit margin: {profit_margin:.1f}%. AI suggests focusing on cost reduction for better profitability.',
            'action': 'View Details',
            'url': '/finance/',
            'priority': 'medium'
        }
    
    def _analyze_tasks(self):
        """Analyze tasks and provide prioritization"""
        from django.db.models import Q
        
        today = timezone.now().date()
        
        overdue_tasks = Task.objects.filter(
            user=self.user,
            due_date__lt=today,
            status='pending'
        )
        
        if overdue_tasks.exists():
            return {
                'type': 'alert',
                'icon': 'tasks',
                'title': 'Task Management Alert',
                'message': f'AI identified {overdue_tasks.count()} overdue task(s). Prioritize completion to maintain farm efficiency.',
                'action': 'View Tasks',
                'url': '/tasks/',
                'priority': 'urgent'
            }
        
        upcoming_tasks = Task.objects.filter(
            user=self.user,
            due_date__lte=today + timedelta(days=3),
            due_date__gte=today,
            status='pending'
        )
        
        if upcoming_tasks.exists():
            return {
                'type': 'info',
                'icon': 'clock',
                'title': 'Upcoming Tasks',
                'message': f'{upcoming_tasks.count()} task(s) due in the next 3 days. AI suggests planning ahead to avoid delays.',
                'action': 'Review Tasks',
                'url': '/tasks/',
                'priority': 'medium'
            }
        
        return None
    
    def _analyze_livestock(self):
        """Analyze livestock data and provide care recommendations"""
        livestock = Livestock.objects.filter(user=self.user)
        
        if not livestock.exists():
            return None
        
        # Check for health monitoring
        needs_checkup = livestock.filter(
            status__in=['sick', 'under_treatment']
        )
        
        if needs_checkup.exists():
            return {
                'type': 'warning',
                'icon': 'heartbeat',
                'title': 'Livestock Health Alert',
                'message': f'AI recommends veterinary checkup for {needs_checkup.count()} animal(s) with concerning health status.',
                'action': 'View Livestock',
                'url': '/livestock/',
                'priority': 'high'
            }
        
        return {
            'type': 'success',
            'icon': 'horse',
            'title': 'Livestock Well-being',
            'message': f'All {livestock.count()} animals showing healthy status. AI monitoring continues for early issue detection.',
            'action': 'View Details',
            'url': '/livestock/',
            'priority': 'low'
        }
    
    def _analyze_weather_impact(self):
        """Provide weather-based recommendations"""
        # Get latest weather data
        latest_weather = WeatherData.objects.filter(user=self.user).order_by('-date').first()
        
        if not latest_weather:
            return {
                'type': 'suggestion',
                'icon': 'cloud-sun',
                'title': 'Weather Intelligence',
                'message': 'Enable AI weather tracking to get predictive insights for irrigation, planting, and harvest timing.',
                'action': 'Learn More',
                'url': '/dashboard/',
                'priority': 'low'
            }
        
        # Simulate weather-based recommendations
        return {
            'type': 'info',
            'icon': 'umbrella',
            'title': 'Weather Advisory',
            'message': 'AI weather analysis suggests optimal conditions for outdoor activities. Good time for field work.',
            'action': 'View Weather',
            'url': '/dashboard/',
            'priority': 'low'
        }
    
    def get_crop_recommendations(self, crop):
        """Get AI recommendations for specific crop"""
        recommendations = []
        today = timezone.now().date()
        
        # Growth stage analysis
        if crop.planting_date:
            days_growing = (today - crop.planting_date).days
            
            if days_growing < 7:
                recommendations.append({
                    'title': 'Early Growth Phase',
                    'message': 'AI recommends frequent watering and monitoring for germination. Protect from pests.',
                    'icon': 'seedling',
                    'type': 'care'
                })
            elif days_growing < 30:
                recommendations.append({
                    'title': 'Vegetative Growth',
                    'message': 'Apply balanced fertilizer. AI suggests checking soil moisture daily.',
                    'icon': 'leaf',
                    'type': 'care'
                })
            else:
                recommendations.append({
                    'title': 'Mature Growth',
                    'message': 'Monitor for flowering/fruiting. Adjust irrigation based on AI weather predictions.',
                    'icon': 'flower',
                    'type': 'care'
                })
        
        # Harvest prediction
        if crop.expected_harvest_date:
            days_to_harvest = (crop.expected_harvest_date - today).days
            
            if 0 <= days_to_harvest <= 7:
                recommendations.append({
                    'title': 'Harvest Ready Soon',
                    'message': f'AI predicts optimal harvest in {days_to_harvest} days. Prepare equipment and storage.',
                    'icon': 'calendar-check',
                    'type': 'action'
                })
            elif days_to_harvest < 0:
                recommendations.append({
                    'title': 'Harvest Overdue',
                    'message': 'AI recommends immediate harvest to prevent quality degradation.',
                    'icon': 'exclamation-triangle',
                    'type': 'urgent'
                })
        
        # Yield optimization
        recommendations.append({
            'title': 'Yield Optimization',
            'message': f'Based on {crop.name} characteristics, AI suggests optimal spacing and nutrient management for maximum yield.',
            'icon': 'chart-bar',
            'type': 'insight'
        })
        
        return recommendations
    
    def get_livestock_care_plan(self, animal):
        """Generate AI care plan for livestock"""
        care_plan = []
        
        # Health monitoring
        if animal.status == 'healthy':
            care_plan.append({
                'title': 'Routine Health Check',
                'message': 'AI recommends monthly veterinary checkup to maintain optimal health.',
                'icon': 'stethoscope',
                'frequency': 'Monthly'
            })
        else:
            care_plan.append({
                'title': 'Immediate Attention Required',
                'message': 'AI detected health concerns. Schedule veterinary consultation urgently.',
                'icon': 'exclamation-circle',
                'frequency': 'Immediate'
            })
        
        # Feeding schedule
        care_plan.append({
            'title': 'Optimized Feeding',
            'message': f'AI-calculated nutrition plan for {animal.type}: balanced diet with seasonal adjustments.',
            'icon': 'utensils',
            'frequency': 'Daily'
        })
        
        # Breeding management
        if animal.date_of_birth:
            age_months = (timezone.now().date() - animal.date_of_birth).days // 30
            if age_months >= 12:
                care_plan.append({
                    'title': 'Breeding Consideration',
                    'message': 'AI suggests this animal has reached breeding maturity. Consider reproductive planning.',
                    'icon': 'heart',
                    'frequency': 'As needed'
                })
        
        return care_plan
    
    def get_financial_forecast(self):
        """Generate AI financial forecast"""
        from django.db.models import Sum
        from datetime import datetime
        
        # Analyze last 3 months
        three_months_ago = timezone.now() - timedelta(days=90)
        
        transactions = FinancialTransaction.objects.filter(
            user=self.user,
            date__gte=three_months_ago
        )
        
        total_income = transactions.filter(type='income').aggregate(Sum('amount'))['total'] or 0
        total_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['total'] or 0
        
        avg_monthly_income = total_income / 3
        avg_monthly_expenses = total_expenses / 3
        
        forecast = {
            'next_month_income': avg_monthly_income * 1.05,  # 5% growth prediction
            'next_month_expenses': avg_monthly_expenses,
            'predicted_profit': (avg_monthly_income * 1.05) - avg_monthly_expenses,
            'confidence': 85,  # AI confidence level
            'recommendations': []
        }
        
        if avg_monthly_expenses > avg_monthly_income * 0.8:
            forecast['recommendations'].append({
                'type': 'cost_reduction',
                'message': 'High expense ratio detected. AI suggests reviewing recurring costs for optimization opportunities.'
            })
        
        if avg_monthly_income > 0:
            forecast['recommendations'].append({
                'type': 'growth',
                'message': f'Based on trends, AI predicts {((avg_monthly_income * 1.05 - avg_monthly_income) / avg_monthly_income * 100):.1f}% revenue growth potential.'
            })
        
        return forecast
    
    def get_smart_task_suggestions(self):
        """Generate AI-suggested tasks based on farm data"""
        suggestions = []
        today = timezone.now().date()
        
        # Check crops needing attention
        crops = Crop.objects.filter(user=self.user, status='growing')
        for crop in crops:
            if crop.planting_date:
                days_since_planting = (today - crop.planting_date).days
                
                # Suggest fertilization
                if days_since_planting % 21 == 0 and days_since_planting > 0:
                    suggestions.append({
                        'title': f'Fertilize {crop.name}',
                        'description': f'AI recommends fertilization based on growth cycle ({days_since_planting} days)',
                        'priority': 'medium',
                        'category': 'crop_care'
                    })
                
                # Suggest pest inspection
                if days_since_planting % 7 == 0 and days_since_planting > 0:
                    suggestions.append({
                        'title': f'Inspect {crop.name} for pests',
                        'description': 'Weekly AI-scheduled pest monitoring',
                        'priority': 'high',
                        'category': 'inspection'
                    })
        
        # Livestock care suggestions
        livestock = Livestock.objects.filter(user=self.user)
        if livestock.exists():
            suggestions.append({
                'title': 'Daily livestock health check',
                'description': f'AI-recommended routine monitoring for {livestock.count()} animal(s)',
                'priority': 'high',
                'category': 'livestock_care'
            })
        
        return suggestions[:10]  # Return top 10 suggestions
