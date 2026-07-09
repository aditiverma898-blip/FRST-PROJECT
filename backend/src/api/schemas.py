from pydantic import BaseModel, Field
from typing import List, Optional

class RecommendationRequest(BaseModel):
    location: str = Field(..., description="City or neighborhood name")
    budget: str = Field(..., description="Budget tier: low, medium, high")
    cuisines: List[str] = Field(default_factory=list, description="Preferred cuisines")
    min_rating: float = Field(0.0, ge=0.0, le=5.0, description="Minimum aggregate rating")
    vibe: Optional[str] = Field(None, description="Free text for specific vibes or constraints")

class RecommendationItem(BaseModel):
    rank: int
    name: str
    cuisine: str
    rating: float
    cost: str
    explanation: str

class RecommendationResponse(BaseModel):
    status: str
    count: int
    recommendations: List[RecommendationItem]
    metadata: dict = {}
