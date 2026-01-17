'use client';

import { MoodOption } from '@/types';

interface MoodSelectorProps {
  moods: MoodOption[];
  selected: string | null;
  onSelect: (mood: string) => void;
}

const moodEmojis: Record<string, string> = {
  relax: '😌',
  adventure: '🏔️',
  food: '🍜',
  nature: '🌿',
  socialize: '👥',
};

const moodColors: Record<string, string> = {
  relax: 'from-blue-400 to-blue-600',
  adventure: 'from-orange-400 to-red-500',
  food: 'from-yellow-400 to-orange-500',
  nature: 'from-green-400 to-emerald-600',
  socialize: 'from-purple-400 to-pink-500',
};

export function MoodSelector({ moods, selected, onSelect }: MoodSelectorProps) {
  return (
    <div className="space-y-4">
      <label className="block text-lg font-semibold text-himalaya-800">
        How are you feeling today?
      </label>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        {moods.map((mood) => (
          <button
            key={mood.value}
            onClick={() => onSelect(mood.value)}
            className={`
              mood-btn relative p-4 rounded-2xl border-2 transition-all duration-200
              ${selected === mood.value 
                ? `bg-gradient-to-br ${moodColors[mood.value]} border-transparent text-white shadow-lg active` 
                : 'bg-white border-himalaya-200 hover:border-himalaya-300 text-himalaya-700'
              }
            `}
          >
            <div className="text-3xl mb-2">{moodEmojis[mood.value]}</div>
            <div className={`font-medium ${selected === mood.value ? 'text-white' : 'text-himalaya-800'}`}>
              {mood.value.charAt(0).toUpperCase() + mood.value.slice(1)}
            </div>
            <div className={`text-xs mt-1 ${selected === mood.value ? 'text-white/80' : 'text-himalaya-500'}`}>
              {mood.description}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
