import pandas as pd
import numpy as np

class Subject:
    def __init__(self, name, difficulty, days_left):
        self.name = name
        self.difficulty = difficulty  # 1-5
        self.days_left = days_left
        self.total_allocated_hours = 0
        self.base_priority = self.calculate_base_priority()
        
    def calculate_base_priority(self):
        """
        Calculates the initial priority based on difficulty and urgency.
        Formula: (Difficulty * 3) + (20 / DaysLeft)
        """
        days_factor = 20 / max(self.days_left, 1) 
        return (self.difficulty * 3) + days_factor

    def get_dynamic_priority(self, current_day_allocated):
        """
        Adjusts priority based on progress to ensure fairness.
        """
        progress_penalty = self.total_allocated_hours * 1.5
        return self.base_priority - progress_penalty

    @property
    def priority_level(self):
        if self.base_priority > 25: return "High"
        if self.base_priority > 15: return "Medium"
        return "Low"

class SmartGreedyPlanner:
    def __init__(self, daily_hours, total_days):
        self.daily_hours = daily_hours
        self.total_days = total_days
        self.subjects = []

    def add_subject(self, name, difficulty, days_left):
        self.subjects.append(Subject(name, difficulty, days_left))

    def generate_schedule(self):
        schedule_data = []
        
        for day in range(1, self.total_days + 1):
            remaining_daily_hours = self.daily_hours
            day_allocation = {"Day": f"Day {day}"}
            
            for sub in self.subjects:
                day_allocation[sub.name] = 0
            
            # Allocation in 1-hour blocks for better distribution (Dynamic Greedy)
            while remaining_daily_hours > 0:
                available_subs = [s for s in self.subjects if day_allocation[s.name] < 2]
                if not available_subs:
                    break
                    
                best_sub = max(available_subs, key=lambda x: x.get_dynamic_priority(day_allocation[x.name]))
                
                day_allocation[best_sub.name] += 1
                best_sub.total_allocated_hours += 1
                remaining_daily_hours -= 1
                
            schedule_data.append(day_allocation)
            
        return pd.DataFrame(schedule_data), self.subjects

    def get_dashboard_metrics(self):
        if not self.subjects:
            return {"total_subs": 0, "avg_priority": 0, "total_hours": 0}
            
        avg_priority = sum(s.base_priority for s in self.subjects) / len(self.subjects)
        total_allocated = sum(s.total_allocated_hours for s in self.subjects)
        
        return {
            "total_subs": len(self.subjects),
            "avg_priority": round(avg_priority, 1),
            "total_hours": total_allocated,
            "top_subject": max(self.subjects, key=lambda x: x.base_priority).name if self.subjects else "None"
        }
