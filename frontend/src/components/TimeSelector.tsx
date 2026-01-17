'use client';

import { PresetOption } from '@/types';

interface TimeSelectorProps {
  value: number;
  presets: PresetOption[];
  onChange: (value: number) => void;
}

export function TimeSelector({ value, presets, onChange }: TimeSelectorProps) {
  const formatTime = (hours: number) => {
    if (hours < 1) {
      return `${Math.round(hours * 60)} mins`;
    }
    if (hours === 1) {
      return '1 hour';
    }
    return `${hours} hours`;
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <label className="block text-lg font-semibold text-himalaya-800">
          Time Available
        </label>
        <span className="text-xl font-bold text-accent-600">
          ⏱️ {formatTime(value)}
        </span>
      </div>

      {/* Time buttons */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {presets.map((preset) => (
          <button
            key={preset.value}
            onClick={() => onChange(preset.value)}
            className={`
              p-3 rounded-xl font-medium transition-all text-center
              ${value === preset.value 
                ? 'bg-gradient-to-br from-accent-400 to-accent-600 text-white shadow-lg scale-105' 
                : 'bg-white border-2 border-himalaya-200 text-himalaya-700 hover:border-accent-300 hover:bg-accent-50'
              }
            `}
          >
            <div className="text-2xl mb-1">
              {preset.value <= 1 ? '⚡' : preset.value <= 2 ? '☕' : preset.value <= 4 ? '🌅' : '🌄'}
            </div>
            <div className="text-sm">{preset.label}</div>
          </button>
        ))}
      </div>

      {/* Custom slider */}
      <div className="pt-2">
        <input
          type="range"
          min="0.5"
          max="8"
          step="0.5"
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full h-2 bg-himalaya-200 rounded-full appearance-none cursor-pointer
            [&::-webkit-slider-thumb]:appearance-none
            [&::-webkit-slider-thumb]:w-5
            [&::-webkit-slider-thumb]:h-5
            [&::-webkit-slider-thumb]:rounded-full
            [&::-webkit-slider-thumb]:bg-accent-500
            [&::-webkit-slider-thumb]:shadow-md
            [&::-webkit-slider-thumb]:cursor-pointer
          "
        />
        <div className="flex justify-between text-xs text-himalaya-400 mt-1">
          <span>30 min</span>
          <span>8+ hours</span>
        </div>
      </div>
    </div>
  );
}
