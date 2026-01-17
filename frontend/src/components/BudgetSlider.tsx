'use client';

import { PresetOption } from '@/types';

interface BudgetSliderProps {
  value: number;
  presets: PresetOption[];
  onChange: (value: number) => void;
}

export function BudgetSlider({ value, presets, onChange }: BudgetSliderProps) {
  const formatBudget = (val: number) => {
    if (val >= 1000) {
      return `₹${(val / 1000).toFixed(val % 1000 === 0 ? 0 : 1)}k`;
    }
    return `₹${val}`;
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <label className="block text-lg font-semibold text-himalaya-800">
          Your Budget
        </label>
        <span className="text-2xl font-bold text-primary-500">
          {formatBudget(value)}
        </span>
      </div>
      
      {/* Slider */}
      <div className="relative">
        <input
          type="range"
          min="100"
          max="10000"
          step="100"
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full h-3 bg-himalaya-200 rounded-full appearance-none cursor-pointer
            [&::-webkit-slider-thumb]:appearance-none
            [&::-webkit-slider-thumb]:w-6
            [&::-webkit-slider-thumb]:h-6
            [&::-webkit-slider-thumb]:rounded-full
            [&::-webkit-slider-thumb]:bg-gradient-to-br
            [&::-webkit-slider-thumb]:from-primary-400
            [&::-webkit-slider-thumb]:to-primary-600
            [&::-webkit-slider-thumb]:shadow-lg
            [&::-webkit-slider-thumb]:cursor-pointer
            [&::-webkit-slider-thumb]:transition-transform
            [&::-webkit-slider-thumb]:hover:scale-110
          "
        />
        <div 
          className="absolute top-0 left-0 h-3 bg-gradient-to-r from-primary-400 to-primary-500 rounded-full pointer-events-none"
          style={{ width: `${((value - 100) / 9900) * 100}%` }}
        />
      </div>

      {/* Quick presets */}
      <div className="flex flex-wrap gap-2">
        {presets.map((preset) => (
          <button
            key={preset.value}
            onClick={() => onChange(preset.value)}
            className={`
              px-4 py-2 rounded-full text-sm font-medium transition-all
              ${value === preset.value 
                ? 'bg-primary-500 text-white shadow-md' 
                : 'bg-himalaya-100 text-himalaya-600 hover:bg-himalaya-200'
              }
            `}
          >
            {preset.label}
          </button>
        ))}
      </div>
    </div>
  );
}
