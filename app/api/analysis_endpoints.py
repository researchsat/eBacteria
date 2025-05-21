from fastapi import APIRouter, Body
from pydantic import BaseModel
from typing import List, Dict
from app.models.colony_counter import simple_colony_count
from app.models.microbe_identifier import simple_microbe_identification
from app.models.growth_monitor import simple_growth_monitoring
from app.models.antibiotic_resistance import predict_antibiotic_resistance

router = APIRouter()

# Pydantic model for GrowthMonitoringRequest
class GrowthMonitoringRequest(BaseModel):
    image_series: List[str]
    duration_hours: int

# Pydantic model for AntibioticResistanceRequest
class AntibioticResistanceRequest(BaseModel):
    identified_microbe: str
    sensitivity_data: Dict

@router.post("/analyze/colony_count")
async def analyze_colony_count(image_name: str = Body(..., embed=True)):
    """
    Analyzes an image to count colonies.
    """
    count = simple_colony_count(image_name)
    return {"image_name": image_name, "estimated_colony_count": count}

@router.post("/analyze/microbial_identification")
async def analyze_microbial_identification(image_name: str = Body(..., embed=True)):
    """
    Analyzes an image to identify microbes.
    """
    identified_microbe = simple_microbe_identification(image_name)
    return {"image_name": image_name, "identified_microbe": identified_microbe}

@router.post("/analyze/growth_monitoring")
async def analyze_growth_monitoring(request: GrowthMonitoringRequest):
    """
    Analyzes an image series to monitor growth.
    """
    status = simple_growth_monitoring(
        image_series=request.image_series,
        duration_hours=request.duration_hours
    )
    return {
        "image_series": request.image_series,
        "duration_hours": request.duration_hours,
        "growth_status": status
    }

@router.post("/predict/antibiotic_resistance")
async def predict_antibiotic_resistance_endpoint(request: AntibioticResistanceRequest):
    """
    Predicts antibiotic resistance for a given microbe and sensitivity data.
    """
    profile = predict_antibiotic_resistance(
        identified_microbe=request.identified_microbe,
        sensitivity_data=request.sensitivity_data
    )
    return {
        "identified_microbe": request.identified_microbe,
        "sensitivity_data": request.sensitivity_data,
        "resistance_profile": profile
    }
