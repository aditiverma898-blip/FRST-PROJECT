import React, { useState, useEffect } from 'react';
import PreferenceForm from '../components/PreferenceForm';
import RecommendationCard from '../components/RecommendationCard';
import LoadingState from '../components/LoadingState';
import EmptyState from '../components/EmptyState';
import { fetchMetadata, fetchRecommendations } from '../services/api';

export default function Home() {
  const [locations, setLocations] = useState([]);
  const [cuisines, setCuisines] = useState([]);
  const [preferences, setPreferences] = useState({
    location: '',
    budget: 'medium',
    cuisine: 'any',
    minRating: 4.5,
    vibe: ''
  });
  
  const [recommendations, setRecommendations] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    fetchMetadata().then(data => {
      setLocations(data.locations);
      setCuisines(data.cuisines);
      setPreferences(prev => ({ ...prev, location: data.locations[0] }));
    });
  }, []);

  const handleSearch = async () => {
    setIsLoading(true);
    setRecommendations(null); // Clear old results to show skeleton
    try {
      const results = await fetchRecommendations(preferences);
      setRecommendations(results);
    } catch (error) {
      console.error("Failed to fetch recommendations", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex-grow w-full max-w-[1200px] mx-auto px-edge-margin py-stack-lg grid grid-cols-1 md:grid-cols-12 gap-gutter">
      {/* Left Column: Preferences */}
      <PreferenceForm 
        preferences={preferences} 
        setPreferences={setPreferences} 
        onSubmit={handleSearch}
        isLoading={isLoading}
        locations={locations}
        cuisines={cuisines}
      />
      
      {/* Right Column: Recommendations */}
      <div className="col-span-1 md:col-span-7 flex flex-col gap-6">
        
        {/* Results Header Banner */}
        {recommendations && (
          <div className="ai-banner-gradient border border-outline-variant rounded-xl p-5 flex gap-4 items-start relative overflow-hidden">
            <div className="absolute -right-4 -top-4 opacity-10">
              <span className="material-symbols-outlined text-9xl">auto_awesome</span>
            </div>
            <div className="text-zomato-red mt-1 shrink-0 z-10">
              <span className="material-symbols-outlined">auto_awesome</span>
            </div>
            <div className="z-10">
              <p className="text-body-md font-body-md text-on-surface italic text-lg leading-relaxed">
                "Based on your preferences, these top picks offer the best experience in {preferences.location}."
              </p>
            </div>
          </div>
        )}

        <div className="flex flex-col gap-5">
          {!isLoading && !recommendations && <EmptyState />}
          
          {isLoading && (
            <>
              <LoadingState />
              <LoadingState />
              <LoadingState />
            </>
          )}

          {!isLoading && recommendations && recommendations.map(rest => (
            <RecommendationCard key={rest.rank} restaurant={rest} />
          ))}
        </div>
      </div>
    </main>
  );
}
