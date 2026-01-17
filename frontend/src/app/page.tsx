'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { MoodSelector, BudgetSlider, TimeSelector, RecommendationCard, LoadingSpinner,EmptyState,ErrorState} from '@/components';
import { OptionsResponse, Recommendation, RecommendationRequest, WeatherOption, CityOption } from '@/types';

// Weather and city component
function WeatherCitySelector({
  weathers,
  cities,
  selectedWeather,
  selectedCity,
  onWeatherChange,
  onCityChange,
}: {
  weathers: WeatherOption[];
  cities: CityOption[];
  selectedWeather: string;
  selectedCity: string;
  onWeatherChange: (w: string) => void;
  onCityChange: (c: string) => void;
}) {
  return (
    <div className="grid md:grid-cols-2 gap-6">
      {/* Weather Selection */}
      <div className="space-y-3">
        <label className="block text-lg font-semibold text-himalaya-800">
          🌤️ Weather Today
        </label>
        <div className="flex flex-wrap gap-2">
          {weathers.map((w) => (
            <button
              key={w.value}
              onClick={() => onWeatherChange(w.value)}
              className={`
                px-4 py-3 rounded-xl font-medium transition-all flex items-center gap-2
                ${selectedWeather === w.value 
                  ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg' 
                  : 'bg-white border-2 border-himalaya-200 text-himalaya-700 hover:border-blue-300'
                }
              `}
            >
              <span className="text-lg">
                {w.value === 'sunny' ? '☀️' : w.value === 'cloudy' ? '☁️' : w.value === 'rainy' ? '🌧️' : '🌤️'}
              </span>
              <div className="text-left">
                <div className="text-sm font-semibold">{w.label.replace(/^[^\s]+\s/, '')}</div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* selects city */}
      <div className="space-y-3">
        <label className="block text-lg font-semibold text-himalaya-800">
          📍 Location
        </label>
        <select
          value={selectedCity}
          onChange={(e) => onCityChange(e.target.value)}
          className="w-full p-4 rounded-xl border-2 border-himalaya-200 bg-white text-himalaya-800 font-medium focus:border-primary-400 focus:ring-2 focus:ring-primary-100 outline-none transition-all cursor-pointer"
        >
          {cities.map((city) => (
            <option key={city.value} value={city.value}>
              {city.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

export default function Home() {
  // options from api 
  const [options, setOptions] = useState<OptionsResponse | null>(null);
  const [optionsLoading, setOptionsLoading] = useState(true);
  
  // Form states
  const [mood, setMood] = useState<string | null>(null);
  const [budget, setBudget] = useState(1500);
  const [timeAvailable, setTimeAvailable] = useState(2);
  const [weather, setWeather] = useState('any');
  const [city, setCity] = useState('kathmandu');
  
  // results states
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  // fetch options
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const data = await api.getOptions();
        setOptions(data);
      } catch (err) {
        console.error('Failed to fetch options:', err);
        // Use fallback option
        setOptions({
          moods: [
            { value: 'relax', label: '😌 Relax', description: 'Unwind and de-stress' },
            { value: 'adventure', label: '🏔️ Adventure', description: 'Excitement and thrills' },
            { value: 'food', label: '🍜 Food', description: 'Culinary experiences' },
            { value: 'nature', label: '🌿 Nature', description: 'Connect with outdoors' },
            { value: 'socialize', label: '👥 Socialize', description: 'Meet people, hangout' },
            { value: 'shopping', label: '🛍️ Shopping', description: 'Retail therapy' },
          ],
          weathers: [
            { value: 'any', label: '🌤️ Any Weather', description: 'No preference' },
            { value: 'sunny', label: '☀️ Sunny', description: 'Clear sunny day' },
            { value: 'cloudy', label: '☁️ Cloudy', description: 'Overcast weather' },
            { value: 'rainy', label: '🌧️ Rainy', description: 'Rainy day activities' },
          ],
          cities: [
            { value: 'kathmandu', label: 'Kathmandu' },
            { value: 'lalitpur', label: 'Lalitpur (Patan)' },
            { value: 'bhaktapur', label: 'Bhaktapur' },
            { value: 'pokhara', label: 'Pokhara' },
            { value: 'butwal', label: 'Butwal' },
            { value: 'any', label: 'Any Location' },
          ],
          budget_presets: [
            { value: 500, label: 'Budget (₹500)' },
            { value: 1500, label: 'Moderate (₹1,500)' },
            { value: 3000, label: 'Comfortable (₹3,000)' },
            { value: 5000, label: 'Premium (₹5,000+)' },
          ],
          time_presets: [
            { value: 1, label: '1 hour' },
            { value: 2, label: '2 hours' },
            { value: 3, label: 'Half day (3-4h)' },
            { value: 6, label: 'Full day (6h+)' },
          ],
        });
      } finally {
        setOptionsLoading(false);
      }
    };
    fetchOptions();
  }, []);

  const handleSearch = async () => {
    if (!mood) {
      setError('Please select your mood first! ');
      return;
    }

    setLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const request: RecommendationRequest = {
        mood,
        budget,
        time_available: timeAvailable,
        weather_preference: weather as 'sunny' | 'cloudy' | 'rainy' | 'any',
        city,
      };

      const response = await api.getRecommendations(request);
      setRecommendations(response.recommendations);
    } catch (err) {
      console.error('Failed to get recommendations:', err);
      setError('Failed to get recommendations. Make sure the backend server is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  if (optionsLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <main className="min-h-screen">
      {/* Hero Header */}
      <header className="relative bg-gradient-to-br from-primary-500 via-primary-600 to-primary-700 text-white overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 text-8xl"></div>
          <div className="absolute top-20 right-20 text-6xl"></div>
          <div className="absolute bottom-10 left-1/4 text-7xl"></div>
          <div className="absolute bottom-20 right-10 text-5xl"></div>
        </div>
        
        <div className="relative max-w-6xl mx-auto px-4 py-12 sm:py-16 text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-4 animate-fade-in">
            Where Should I Go
            <span className="block text-yellow-300">Today?</span>
          </h1>
          <p className="text-lg sm:text-xl text-white/90 max-w-2xl mx-auto animate-fade-in">
            Discover the perfect place in Nepal based on your mood, budget, and time. 
            No planning needed — just tell us how you feel! 🇳🇵
          </p>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-4 py-8 sm:py-12">
        {/* Preference Form */}
        <div className="glass rounded-3xl shadow-xl p-6 sm:p-8 mb-8 border border-white/20">
          <div className="space-y-8">
            {/* Mood Selection */}
            {options && (
              <MoodSelector 
                moods={options.moods} 
                selected={mood} 
                onSelect={setMood} 
              />
            )}

            {/* Budget and time row */}
            <div className="grid md:grid-cols-2 gap-8">
              {options && (
                <>
                  <BudgetSlider
                    value={budget}
                    presets={options.budget_presets}
                    onChange={setBudget}
                  />
                  <TimeSelector
                    value={timeAvailable}
                    presets={options.time_presets}
                    onChange={setTimeAvailable}
                  />
                </>
              )}
            </div>

            {/* Weather and city */}
            {options && (
              <WeatherCitySelector
                weathers={options.weathers}
                cities={options.cities}
                selectedWeather={weather}
                selectedCity={city}
                onWeatherChange={setWeather}
                onCityChange={setCity}
              />
            )}

            {/* search button */}
            <div className="pt-4">
              <button
                onClick={handleSearch}
                disabled={loading || !mood}
                className={`
                  w-full py-4 px-8 rounded-2xl text-lg font-bold transition-all
                  ${mood 
                    ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg hover:shadow-xl hover:from-primary-600 hover:to-primary-700 active:scale-[0.98]' 
                    : 'bg-himalaya-200 text-himalaya-400 cursor-not-allowed'
                  }
                `}
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                    Finding your spot...
                  </span>
                ) : (
                  <span className="flex items-center justify-center gap-2">
                     Find My Spot!
                  </span>
                )}
              </button>
              
              {!mood && (
                <p className="text-center text-himalaya-500 mt-2 text-sm">
                   Select your mood to get started
                </p>
              )}
            </div>
          </div>
        </div>

        {/* results section */}
        <div className="mb-8">
          {error && (
            <ErrorState 
              message={error} 
              onRetry={() => {
                setError(null);
                handleSearch();
              }} 
            />
          )}

          {loading && <LoadingSpinner />}

          {!loading && !error && hasSearched && recommendations.length === 0 && (
            <div className="text-center py-12 bg-himalaya-50 rounded-2xl">
              <div className="text-6xl mb-4">🤷</div>
              <h3 className="text-xl font-semibold text-himalaya-800 mb-2">
                No matches found
              </h3>
              <p className="text-himalaya-600">
                Try adjusting your preferences or selecting a different city
              </p>
            </div>
          )}

          {!loading && !error && recommendations.length > 0 && (
            <div>
              <div className="text-center mb-8">
                <h2 className="text-2xl sm:text-3xl font-bold text-himalaya-900 mb-2">
                  🎉 Your Perfect Spots
                </h2>
                <p className="text-himalaya-600">
                  Based on your preferences, here are the top recommendations
                </p>
              </div>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations.map((rec, idx) => (
                  <RecommendationCard 
                    key={rec.place.id} 
                    recommendation={rec} 
                    rank={idx + 1} 
                  />
                ))}
              </div>
            </div>
          )}

          {!loading && !error && !hasSearched && <EmptyState />}
        </div>

        {/* how it works section */}
        <div className="bg-white rounded-3xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-himalaya-900 text-center mb-8">
            How It Works ✨
          </h2>
          <div className="grid sm:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">😊</span>
              </div>
              <h3 className="font-semibold text-himalaya-800 mb-2">1. Tell Us Your Mood</h3>
              <p className="text-sm text-himalaya-500">
                Feeling adventurous? Want to relax? Craving food? Let us know!
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-accent-100 to-accent-200 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">⚙️</span>
              </div>
              <h3 className="font-semibold text-himalaya-800 mb-2">2. Set Preferences</h3>
              <p className="text-sm text-himalaya-500">
                Budget, time available, indoor or outdoor — customize your search
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-yellow-100 to-yellow-200 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">🎯</span>
              </div>
              <h3 className="font-semibold text-himalaya-800 mb-2">3. Get Perfect Matches</h3>
              <p className="text-sm text-himalaya-500">
                Our smart scoring finds the best spots for you in seconds!
              </p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center py-8 text-himalaya-500 text-sm">
          <p className="mb-2">
            Built with 💙 for Nepal 🇳🇵
          </p>
          <p className="text-xs">
            Hackathon Demo • No login required • All data is static
          </p>
        </footer>
      </div>
    </main>
  );
}
