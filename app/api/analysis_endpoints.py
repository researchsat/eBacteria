from fastapi import APIRouter, Body
from app.models.colony_counter import simple_colony_count

router = APIRouter()

@router.post("/analyze/colony_count")
async def analyze_colony_count(image_name: str = Body(..., embed=True)):
    """
    Analyzes an image to count colonies.
    """
    count = simple_colony_count(image_name)
    return {"image_name": image_name, "estimated_colony_count": count}
