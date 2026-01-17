'use client';

import { Recommendation } from '@/types';
import Image from 'next/image';

interface RecommendationCardProps {
  recommendation: Recommendation;
  rank: number;
}

export function RecommendationCard({ recommendation, rank }: RecommendationCardProps) {
  const { place, total_score, explanation, match_reasons, budget_range, time_range, weather_suitable } = recommendation;
  
  const getRankBadge = (rank: number) => {
    if (rank === 1) return { bg: 'from-yellow-400 to-amber-500', icon: '🥇', label: 'Best Match' };
    if (rank === 2) return { bg: 'from-gray-300 to-gray-400', icon: '🥈', label: 'Great Option' };
    return { bg: 'from-amber-600 to-amber-700', icon: '🥉', label: 'Good Choice' };
  };

  const badge = getRankBadge(rank);
  
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'from-green-400 to-green-500';
    if (score >= 60) return 'from-yellow-400 to-yellow-500';
    return 'from-orange-400 to-orange-500';
  };

  return (
    <div 
      className={`
        card-hover bg-white rounded-3xl overflow-hidden shadow-lg border border-himalaya-100
        animate-slide-up
        ${rank === 1 ? 'ring-2 ring-primary-400 ring-offset-2' : ''}
      `}
      style={{ animationDelay: `${rank * 100}ms` }}
    >
      {/* Image Header */}
      <div className="relative h-48 sm:h-56">
        {place.image_url ? (
          <Image
            src={place.image_url}
            alt={place.name}
            fill
            className="object-cover"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-himalaya-200 to-himalaya-300 flex items-center justify-center">
            <span className="text-6xl">🏔️</span>
          </div>
        )}
        
        {/* Rank Badge */}
        <div className={`absolute top-4 left-4 px-3 py-1.5 rounded-full bg-gradient-to-r ${badge.bg} text-white font-semibold text-sm shadow-lg flex items-center gap-1`}>
          <span>{badge.icon}</span>
          <span>{badge.label}</span>
        </div>

        {/* Score Badge */}
        <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-full px-3 py-1.5 shadow-lg">
          <span className="text-lg font-bold text-himalaya-800">{Math.round(total_score)}</span>
          <span className="text-sm text-himalaya-500">/100</span>
        </div>

        {/* City Badge */}
        <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm rounded-full px-3 py-1 text-sm font-medium text-himalaya-700 shadow">
          📍 {place.city.charAt(0).toUpperCase() + place.city.slice(1)}
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        <h3 className="text-xl font-bold text-himalaya-900 mb-2">{place.name}</h3>
        <p className="text-himalaya-600 text-sm mb-4 line-clamp-2">{place.description}</p>

        {/* Why this place */}
        <div className="bg-gradient-to-r from-primary-50 to-accent-50 rounded-xl p-4 mb-4">
          <p className="text-himalaya-700 font-medium text-sm">
            💡 {explanation}
          </p>
        </div>

        {/* Quick Info Grid */}
        <div className="grid grid-cols-3 gap-3 mb-4">
          <div className="bg-himalaya-50 rounded-xl p-3 text-center">
            <div className="text-lg">💰</div>
            <div className="text-xs text-himalaya-500">Budget</div>
            <div className="text-sm font-semibold text-himalaya-800">{budget_range}</div>
          </div>
          <div className="bg-himalaya-50 rounded-xl p-3 text-center">
            <div className="text-lg">⏱️</div>
            <div className="text-xs text-himalaya-500">Duration</div>
            <div className="text-sm font-semibold text-himalaya-800">{time_range}</div>
          </div>
          <div className="bg-himalaya-50 rounded-xl p-3 text-center">
            <div className="text-lg">{place.primary_weather === 'sunny' ? '☀️' : place.primary_weather === 'rainy' ? '🌧️' : '☁️'}</div>
            <div className="text-xs text-himalaya-500">Weather</div>
            <div className="text-sm font-semibold text-himalaya-800 capitalize">{place.primary_weather}</div>
          </div>
        </div>

        {/* Score Breakdown */}
        <div className="space-y-2 mb-4">
          <ScoreBar label="Mood" score={recommendation.mood_score} icon="😊" />
          <ScoreBar label="Budget" score={recommendation.budget_score} icon="💵" />
          <ScoreBar label="Time" score={recommendation.time_score} icon="⏰" />
          <ScoreBar label="Weather" score={recommendation.weather_score} icon="🌤️" />
        </div>

        {/* Match Reasons */}
        {match_reasons.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-4">
            {match_reasons.map((reason, idx) => (
              <span 
                key={idx}
                className="text-xs bg-accent-100 text-accent-700 px-2 py-1 rounded-full"
              >
                ✓ {reason}
              </span>
            ))}
          </div>
        )}

        {/* Weather Note */}
        <div className="text-sm text-himalaya-500 mb-4">
          {weather_suitable}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          {place.google_maps_url && (
            <a
              href={place.google_maps_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 bg-gradient-to-r from-primary-500 to-primary-600 text-white py-3 px-4 rounded-xl font-semibold text-center hover:from-primary-600 hover:to-primary-700 transition-all shadow-md hover:shadow-lg"
            >
              🗺️ View on Map
            </a>
          )}
          <button
            onClick={() => {
              navigator.share?.({
                title: place.name,
                text: `Check out ${place.name} - ${explanation}`,
                url: place.google_maps_url || window.location.href,
              }).catch(() => {});
            }}
            className="p-3 bg-himalaya-100 rounded-xl hover:bg-himalaya-200 transition-all"
          >
            📤
          </button>
        </div>
      </div>
    </div>
  );
}

function ScoreBar({ label, score, icon }: { label: string; score: number; icon: string }) {
  const getColor = (score: number) => {
    if (score >= 80) return 'bg-gradient-to-r from-green-400 to-green-500';
    if (score >= 60) return 'bg-gradient-to-r from-yellow-400 to-yellow-500';
    if (score >= 40) return 'bg-gradient-to-r from-orange-400 to-orange-500';
    return 'bg-gradient-to-r from-red-400 to-red-500';
  };

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm w-6">{icon}</span>
      <span className="text-xs text-himalaya-500 w-14">{label}</span>
      <div className="flex-1 h-2 bg-himalaya-100 rounded-full overflow-hidden">
        <div 
          className={`h-full score-bar ${getColor(score)} rounded-full`}
          style={{ width: `${score}%` }}
        />
      </div>
      <span className="text-xs font-semibold text-himalaya-600 w-8">{Math.round(score)}</span>
    </div>
  );
}
