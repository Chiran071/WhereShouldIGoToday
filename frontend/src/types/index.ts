// API Types for Where To Go Today

export interface Place {
  id: number;
  name: string;
  description: string;
  city: string;
  latitude: number;
  longitude: number;
  primary_mood: string;
  secondary_mood: string | null;
  tertiary_mood: string | null;
  quaternary_mood: string | null;
  mood_display: string;
  min_budget: number;
  max_budget: number;
  min_time_hours: number;
  max_time_hours: number;
  primary_weather: 'sunny' | 'cloudy' | 'rainy';
  secondary_weather: 'sunny' | 'cloudy' | 'rainy' | null;
  primary_weather_display: string;
  image_url: string | null;
  google_maps_url: string | null;
  rating: number;
}

export interface Recommendation {
  place: Place;
  total_score: number;
  mood_score: number;
  budget_score: number;
  time_score: number;
  weather_score: number;
  rating_score: number;
  explanation: string;
  match_reasons: string[];
  budget_range: string;
  time_range: string;
  weather_suitable: string;
}

export interface RecommendationRequest {
  mood: string;
  budget: number;
  time_available: number;
  weather_preference: 'sunny' | 'cloudy' | 'rainy' | 'any';
  city: string;
}

export interface RecommendationResponse {
  recommendations: Recommendation[];
  user_input: RecommendationRequest;
  total_places_considered: number;
}

export interface MoodOption {
  value: string;
  label: string;
  description: string;
}

export interface WeatherOption {
  value: string;
  label: string;
  description: string;
}

export interface CityOption {
  value: string;
  label: string;
}

export interface PresetOption {
  value: number;
  label: string;
}

export interface OptionsResponse {
  moods: MoodOption[];
  weathers: WeatherOption[];
  cities: CityOption[];
  budget_presets: PresetOption[];
  time_presets: PresetOption[];
}
