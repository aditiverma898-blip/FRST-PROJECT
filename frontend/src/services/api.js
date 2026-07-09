const API_BASE = 'http://localhost:8000/api/v1';

export async function fetchMetadata() {
  try {
    const [locationsRes, cuisinesRes] = await Promise.all([
      fetch(`${API_BASE}/locations`),
      fetch(`${API_BASE}/cuisines`)
    ]);
    const locations = await locationsRes.json();
    const cuisines = await cuisinesRes.json();
    return { locations, cuisines };
  } catch (error) {
    console.error("Error fetching metadata:", error);
    return { locations: [], cuisines: [] };
  }
}

export async function fetchRecommendations(preferences) {
  try {
    const cuisinesList = preferences.cuisine && preferences.cuisine !== 'any' 
      ? [preferences.cuisine] 
      : [];
      
    const payload = {
      location: preferences.location,
      budget: preferences.budget,
      cuisines: cuisinesList,
      min_rating: parseFloat(preferences.minRating) || 0.0,
      vibe: preferences.vibe || null
    };

    const response = await fetch(`${API_BASE}/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    return data.recommendations;
  } catch (error) {
    console.error("Error fetching recommendations:", error);
    throw error;
  }
}
