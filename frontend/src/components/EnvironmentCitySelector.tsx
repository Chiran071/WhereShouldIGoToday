'use client';

import { EnvironmentOption, CityOption } from '@/types';

interface EnvironmentCitySelectorProps {
  environments: EnvironmentOption[];
  cities: CityOption[];
  selectedEnvironment: string;
  selectedCity: string;
  onEnvironmentChange: (value: string) => void;
  onCityChange: (value: string) => void;
}

const envIcons: Record<string, string> = {
  any: '🌤️',
  indoor: '🏠',
  outdoor: '☀️',
};

export function EnvironmentCitySelector({
  environments,
  cities,
  selectedEnvironment,
  selectedCity,
  onEnvironmentChange,
  onCityChange,
}: EnvironmentCitySelectorProps) {
  return (
    <div className="grid md:grid-cols-2 gap-6">
      {/* Environment */}
      <div className="space-y-3">
        <label className="block text-lg font-semibold text-himalaya-800">
          Weather Preference
        </label>
        <div className="flex gap-2">
          {environments.map((env) => (
            <button
              key={env.value}
              onClick={() => onEnvironmentChange(env.value)}
              className={`
                flex-1 p-3 rounded-xl font-medium transition-all text-center
                ${selectedEnvironment === env.value 
                  ? 'bg-gradient-to-br from-sky-400 to-blue-500 text-white shadow-lg' 
                  : 'bg-white border-2 border-himalaya-200 text-himalaya-700 hover:border-sky-300'
                }
              `}
            >
              <div className="text-xl">{envIcons[env.value]}</div>
              <div className="text-sm mt-1">{env.label.split(' ')[1] || env.label}</div>
            </button>
          ))}
        </div>
        <p className="text-xs text-himalaya-500 text-center">
          {selectedEnvironment === 'indoor' && '☔ Good for rainy days'}
          {selectedEnvironment === 'outdoor' && '☀️ Best for sunny weather'}
          {selectedEnvironment === 'any' && '🌤️ Works for any weather'}
        </p>
      </div>

      {/* City */}
      <div className="space-y-3">
        <label className="block text-lg font-semibold text-himalaya-800">
          Location
        </label>
        <select
          value={selectedCity}
          onChange={(e) => onCityChange(e.target.value)}
          className="w-full p-4 rounded-xl border-2 border-himalaya-200 bg-white text-himalaya-700 
            font-medium focus:border-primary-400 focus:ring-2 focus:ring-primary-100 
            transition-all cursor-pointer appearance-none
            bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23475569%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E')]
            bg-[length:12px] bg-[right_16px_center] bg-no-repeat
          "
        >
          {cities.map((city) => (
            <option key={city.value} value={city.value}>
              📍 {city.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
