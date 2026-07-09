from fastapi import APIRouter, HTTPException, Depends
from typing import List
import time
from .schemas import RecommendationRequest, RecommendationResponse, RecommendationItem
from core.filter import apply_filters
from core.ranker import pre_rank
from llm.client import GroqClient
from llm.prompt_builder import build_prompt
from llm.parser import parse_recommendations

router = APIRouter()
llm_client = GroqClient()

def get_dataframe():
    from .app import app_state
    if app_state.get("df") is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded yet")
    return app_state["df"]

@router.get("/health")
async def health_check():
    from .app import app_state
    return {
        "status": "ok",
        "dataset_loaded": app_state.get("df") is not None
    }

@router.get("/locations", response_model=List[str])
async def get_locations():
    df = get_dataframe()
    if "city" not in df.columns:
        return []
    locations = sorted(df["city"].dropna().unique().tolist())
    return locations

@router.get("/cuisines", response_model=List[str])
async def get_cuisines():
    df = get_dataframe()
    if "cuisines" not in df.columns:
        return []
    # Extract unique cuisines
    all_cuisines = set()
    for c_str in df["cuisines"].dropna():
        for c in c_str.split(","):
            all_cuisines.add(c.strip())
    return sorted(list(all_cuisines))

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    start_time = time.time()
    df = get_dataframe()
    
    prefs = {
        "city": request.location,
        "budget": request.budget,
        "cuisines": request.cuisines,
        "min_rating": request.min_rating,
    }
    
    filtered_df = apply_filters(df, prefs)
    ranked_df = pre_rank(filtered_df, top_n=15)
    
    if ranked_df.empty:
        return RecommendationResponse(
            status="success",
            count=0,
            recommendations=[],
            metadata={"message": "No restaurants found matching your criteria."}
        )
    
    system_prompt, user_prompt = build_prompt(
        candidates=ranked_df,
        preferences={**prefs, "additional_preferences": request.vibe}
    )
    
    try:
        response_text = llm_client.get_recommendation(system_prompt, user_prompt)
        parsed_recs = parse_recommendations(response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {str(e)}")
        
    # Map parsed recs to RecommendationItem
    items = []
    for rec in parsed_recs:
        items.append(RecommendationItem(
            rank=rec.get("rank", 0),
            name=rec.get("restaurant_name", "Unknown"),
            cuisine=rec.get("cuisine", "Various"),
            rating=rec.get("rating", 0.0),
            cost=f"₹{rec.get('cost_for_two', 0)} for two",
            explanation=rec.get("explanation", "")
        ))
        
    return RecommendationResponse(
        status="success",
        count=len(items),
        recommendations=items,
        metadata={
            "processing_time_ms": int((time.time() - start_time) * 1000)
        }
    )
