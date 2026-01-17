import { RecommendationRequest, RecommendationResponse, OptionsResponse, Place } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

class ApiService {
  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async getRecommendations(request: RecommendationRequest): Promise<RecommendationResponse> {
    return this.fetch<RecommendationResponse>('/recommendations/', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getOptions(): Promise<OptionsResponse> {
    return this.fetch<OptionsResponse>('/options/');
  }

  async getPlaces(): Promise<{ places: Place[]; count: number }> {
    return this.fetch<{ places: Place[]; count: number }>('/places/');
  }

  async getHealth(): Promise<{ status: string; places_count: number }> {
    return this.fetch<{ status: string; places_count: number }>('/health/');
  }
}

export const api = new ApiService();
