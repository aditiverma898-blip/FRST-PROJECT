import React from 'react';

export default function PreferenceForm({ preferences, setPreferences, onSubmit, isLoading, locations, cuisines }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setPreferences(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="col-span-1 md:col-span-5 flex flex-col gap-6">
      <h2 className="text-headline-md font-headline-md text-on-surface mb-2">Your preferences</h2>
      <div className="bg-[#F8F8F8] border border-surface-dim rounded-xl p-6 flex flex-col gap-6">
        
        {/* Location Dropdown */}
        <div>
          <label className="block text-label-md font-label-md text-on-surface mb-2">Location</label>
          <div className="relative">
            <span className="material-symbols-outlined absolute left-3 top-3 text-on-surface-variant">location_on</span>
            <select
              name="location"
              value={preferences.location}
              onChange={handleChange}
              className="w-full pl-10 pr-4 py-2 bg-surface border border-surface-dim rounded-lg focus:outline-none focus:border-zomato-red focus:ring-1 focus:ring-zomato-red transition-colors text-body-md font-body-md appearance-none"
            >
              <option value="">Select a city</option>
              {locations.map(loc => (
                <option key={loc} value={loc}>{loc}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Budget */}
        <div>
          <label className="block text-label-md font-label-md text-on-surface mb-2">Budget for two</label>
          <select 
            name="budget"
            value={preferences.budget}
            onChange={handleChange}
            className="w-full px-4 py-2 bg-surface border border-surface-dim rounded-lg focus:outline-none focus:border-zomato-red focus:ring-1 focus:ring-zomato-red transition-colors text-body-md font-body-md appearance-none"
          >
            <option value="low">Low (&lt;₹500)</option>
            <option value="medium">Medium (₹501-1500)</option>
            <option value="high">High (&gt;₹1500)</option>
          </select>
        </div>

        {/* Cuisine */}
        <div>
          <label className="block text-label-md font-label-md text-on-surface mb-2">Cuisine</label>
          <select 
            name="cuisine"
            value={preferences.cuisine}
            onChange={handleChange}
            className="w-full px-4 py-2 bg-surface border border-surface-dim rounded-lg focus:outline-none focus:border-zomato-red focus:ring-1 focus:ring-zomato-red transition-colors text-body-md font-body-md appearance-none"
          >
            <option value="any">Any cuisine</option>
            {cuisines.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </div>

        {/* Rating */}
        <div>
          <div className="flex justify-between mb-2">
            <label className="block text-label-md font-label-md text-on-surface">Minimum Rating</label>
            <span className="text-label-md font-label-md text-zomato-red font-bold">{preferences.minRating}</span>
          </div>
          <input 
            type="range" 
            name="minRating"
            value={preferences.minRating}
            onChange={handleChange}
            min="0" max="5" step="0.1" 
            className="w-full h-2 bg-surface-dim rounded-lg appearance-none cursor-pointer accent-zomato-red" 
          />
          <div className="flex justify-between mt-1 text-label-sm font-label-sm text-on-surface-variant">
            <span>0.0</span>
            <span>5.0</span>
          </div>
        </div>

        {/* Open Text */}
        <div>
          <label className="block text-label-md font-label-md text-on-surface mb-2">Vibe & specifics (Optional)</label>
          <textarea 
            name="vibe"
            value={preferences.vibe}
            onChange={handleChange}
            className="w-full px-4 py-2 bg-surface border border-surface-dim rounded-lg focus:outline-none focus:border-zomato-red focus:ring-1 focus:ring-zomato-red transition-colors text-body-md font-body-md resize-none" 
            placeholder="e.g. family-friendly, quick service, quiet, romantic..." 
            rows="3"
          ></textarea>
        </div>

        {/* Submit Action */}
        <button 
          onClick={onSubmit}
          disabled={isLoading || !preferences.location}
          className="w-full bg-zomato-red text-white py-3 rounded-lg text-label-md font-label-md font-bold hover:bg-primary-container transition-colors mt-2 shadow-sm disabled:opacity-50"
        >
          {isLoading ? 'Getting Recommendations...' : 'Get Recommendations'}
        </button>
      </div>
    </div>
  );
}
