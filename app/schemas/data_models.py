from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str = Field(..., example="researcher@example.com")

class UserCreate(UserBase):
    password: str = Field(..., example="securepassword123")

class UserRead(UserBase):
    id: int
    is_active: bool = True

    class Config:
        orm_mode = True # For SQLAlchemy or other ORM compatibility

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ImageMetadataCreate(BaseModel):
    filename: str = Field(..., example="plate_01_day1.png")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    content_type: Optional[str] = Field(None, example="image/png")
    size_bytes: Optional[int] = Field(None, example=102400) # In bytes

class ImageMetadataRead(ImageMetadataCreate):
    id: int
    uploader_id: int # Foreign key to User

    class Config:
        orm_mode = True

class AnalysisResultBase(BaseModel):
    image_id: int # Foreign key to ImageMetadata
    analysis_type: str = Field(..., example="colony_count") # e.g., "colony_count", "identification", "growth_monitoring"
    ran_at: datetime = Field(default_factory=datetime.utcnow)
    confidence_score: Optional[float] = Field(None, example=0.95, ge=0.0, le=1.0) # Added confidence score
    
class AnalysisResultCreate(AnalysisResultBase):
    result_data: dict # Flexible field to store various result structures

class AnalysisResultRead(AnalysisResultCreate):
    id: int

    class Config:
        orm_mode = True
