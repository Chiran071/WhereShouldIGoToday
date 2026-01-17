"""
Rule-Based Weighted Scoring Engine
===================================
Explainable, deterministic recommendation logic for hackathon demo.

Scoring Factors & Weights:
- Mood Match: 35% (primary=100%, secondary=70%, tertiary=50%, quaternary=30%)
- Budget Fit: 25% (within range = 100%, close = partial)
- Time Fit: 20% (matches available time)
- Weather Match: 15% (sunny/cloudy/rainy preference)
- Rating Bonus: 5% (quality factor)

Total Score = weighted sum normalized to 0-100
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class UserPreferences:
    """User input preferences for recommendation."""
    mood: str
    budget: int  # NPR
    time_available: float  # hours
    weather_preference: str  # 'sunny', 'cloudy', 'rainy', 'any'
    city: str = 'kathmandu'


@dataclass
class ScoredPlace:
    """Place with computed score and explanation."""
    place: Any  # Place model instance
    total_score: float
    mood_score: float
    budget_score: float
    time_score: float
    weather_score: float
    rating_score: float
    explanation: str
    match_reasons: List[str]


class RecommendationEngine:
    """
    Rule-based weighted scoring engine.
    Designed for explainability and hackathon demo.
    """
    
    # Scoring weights (must sum to 1.0)
    WEIGHTS = {
        'mood': 0.35,
        'budget': 0.25,
        'time': 0.20,
        'weather': 0.15,
        'rating': 0.05,
    }
    
    def __init__(self):
        pass
    
    def calculate_mood_score(self, place, user_mood: str) -> tuple[float, str]:
        """
        Calculate mood match score.
        Primary mood = 100%, Secondary = 70%, Tertiary = 50%, Quaternary = 30%
        """
        if place.primary_mood == user_mood:
            return 100.0, f"Perfect for {user_mood} mood"
        elif place.secondary_mood == user_mood:
            return 70.0, f"Great for {user_mood}"
        elif place.tertiary_mood == user_mood:
            return 50.0, f"Good option for {user_mood}"
        elif place.quaternary_mood == user_mood:
            return 30.0, f"Can work for {user_mood}"
        else:
            # Partial score based on mood compatibility
            mood_compatibility = {
                ('relax', 'nature'): 40,
                ('nature', 'relax'): 40,
                ('adventure', 'nature'): 35,
                ('nature', 'adventure'): 35,
                ('food', 'socialize'): 45,
                ('socialize', 'food'): 45,
                ('relax', 'food'): 30,
                ('food', 'relax'): 30,
                ('shopping', 'socialize'): 40,
                ('socialize', 'shopping'): 40,
                ('shopping', 'food'): 35,
                ('food', 'shopping'): 35,
            }
            score = mood_compatibility.get((place.primary_mood, user_mood), 15)
            return float(score), f"Alternative for {user_mood}"
    
    def calculate_budget_score(self, place, user_budget: int) -> tuple[float, str]:
        """
        Calculate budget fit score.
        Within range = 100%, proportionally less outside.
        """
        min_b, max_b = place.min_budget, place.max_budget
        
        if min_b <= user_budget <= max_b:
            return 100.0, f"Fits your ₹{user_budget} budget perfectly"
        elif user_budget > max_b:
            # Under budget is good
            surplus_ratio = (user_budget - max_b) / max_b
            score = min(100, 80 + surplus_ratio * 20)
            return score, f"Well under budget (costs ₹{min_b}-{max_b})"
        else:
            # Over budget - penalize proportionally
            deficit_ratio = (min_b - user_budget) / min_b
            score = max(0, 100 - deficit_ratio * 150)
            if score > 50:
                return score, f"Slightly over budget (needs ₹{min_b}+)"
            return score, f"May exceed budget (needs ₹{min_b}+)"
    
    def calculate_time_score(self, place, user_time: float) -> tuple[float, str]:
        """
        Calculate time fit score.
        Perfect fit if user time is within place's time range.
        """
        min_t, max_t = place.min_time_hours, place.max_time_hours
        
        if min_t <= user_time <= max_t:
            return 100.0, f"Perfect for {user_time}h visit"
        elif user_time > max_t:
            # More time than needed - still good
            return 85.0, f"You'll have extra time ({min_t}-{max_t}h needed)"
        else:
            # Less time than minimum needed
            time_ratio = user_time / min_t
            score = max(0, time_ratio * 100)
            if score > 60:
                return score, f"Quick visit possible ({min_t}h ideal)"
            return score, f"Might feel rushed (needs {min_t}h+)"
    
    def calculate_weather_score(self, place, user_pref: str) -> tuple[float, str]:
        """
        Calculate weather suitability score.
        Primary weather = 100%, Secondary = 70%
        """
        primary = place.primary_weather
        secondary = place.secondary_weather
        
        if user_pref == 'any':
            weather_icons = {'sunny': '☀️', 'cloudy': '☁️', 'rainy': '🌧️'}
            icon = weather_icons.get(primary, '🌤️')
            return 80.0, f"{icon} Best for {primary} weather"
        
        if primary == user_pref:
            weather_msgs = {
                'sunny': "☀️ Perfect for sunny day",
                'cloudy': "☁️ Great for cloudy weather", 
                'rainy': "🌧️ Perfect for rainy day"
            }
            return 100.0, weather_msgs.get(user_pref, "Weather match")
        elif secondary == user_pref:
            return 70.0, f"Good for {user_pref} weather too"
        else:
            return 30.0, "Better suited for different weather"
    
    def calculate_rating_score(self, place) -> tuple[float, str]:
        """Convert 1-10 rating to 0-100 score."""
        score = place.rating * 10
        if score >= 80:
            return score, "Highly rated spot"
        elif score >= 60:
            return score, "Well-reviewed place"
        return score, "Hidden gem"
    
    def score_place(self, place, prefs: UserPreferences) -> ScoredPlace:
        """
        Calculate total weighted score for a place.
        Returns ScoredPlace with breakdown and explanation.
        """
        # Calculate individual scores
        mood_score, mood_reason = self.calculate_mood_score(place, prefs.mood)
        budget_score, budget_reason = self.calculate_budget_score(place, prefs.budget)
        time_score, time_reason = self.calculate_time_score(place, prefs.time_available)
        weather_score, weather_reason = self.calculate_weather_score(place, prefs.weather_preference)
        rating_score, rating_reason = self.calculate_rating_score(place)
        
        # Calculate weighted total
        total_score = (
            mood_score * self.WEIGHTS['mood'] +
            budget_score * self.WEIGHTS['budget'] +
            time_score * self.WEIGHTS['time'] +
            weather_score * self.WEIGHTS['weather'] +
            rating_score * self.WEIGHTS['rating']
        )
        
        # Build explanation and reasons
        match_reasons = []
        if mood_score >= 50:
            match_reasons.append(mood_reason)
        if budget_score >= 70:
            match_reasons.append(budget_reason)
        if time_score >= 70:
            match_reasons.append(time_reason)
        if weather_score >= 70:
            match_reasons.append(weather_reason)
        
        # Generate main explanation
        if total_score >= 80:
            explanation = f"Excellent match! {match_reasons[0] if match_reasons else 'Great choice for you'}"
        elif total_score >= 60:
            explanation = f"Good option. {match_reasons[0] if match_reasons else 'Worth considering'}"
        else:
            explanation = f"Alternative choice. {match_reasons[0] if match_reasons else 'Could work'}"
        
        return ScoredPlace(
            place=place,
            total_score=round(total_score, 1),
            mood_score=round(mood_score, 1),
            budget_score=round(budget_score, 1),
            time_score=round(time_score, 1),
            weather_score=round(weather_score, 1),
            rating_score=round(rating_score, 1),
            explanation=explanation,
            match_reasons=match_reasons[:3]  # Top 3 reasons
        )
    
    def get_recommendations(self, places, prefs: UserPreferences, top_n: int = 3) -> List[ScoredPlace]:
        """
        Score all places and return top N recommendations.
        """
        # Filter by city first (if specified)
        if prefs.city and prefs.city != 'any':
            filtered_places = [p for p in places if p.city == prefs.city]
            # If no places in city, use all
            if not filtered_places:
                filtered_places = list(places)
        else:
            filtered_places = list(places)
        
        # Score all places
        scored_places = [self.score_place(p, prefs) for p in filtered_places]
        
        # Sort by total score descending
        scored_places.sort(key=lambda x: x.total_score, reverse=True)
        
        return scored_places[:top_n]


# Singleton instance for easy import
engine = RecommendationEngine()
