# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class InternshipBase(BaseModel):
    title: str
    min_education: str
    skills: str
    sector: str
    location: str
    duration: str
    no_of_posts: int
    is_active: bool
    description: str

class InternshipCreate(InternshipBase):
    pass

class InternshipResponse(InternshipBase):
    id: int
    
    class Config:
        from_attributes = True

class StudentForm(BaseModel):
    education: str
    skills: List[str]  # List of skills
    sector: str
    preferred_location: str
    description: str

class FormOptions(BaseModel):
    education_options: List[str]
    skills_options: List[str]
    sector_options: List[str]
    location_options: List[str]

class RecommendationResponse(BaseModel):
    id: int
    title: str
    sector: str
    location: str
    skills: str
    duration: str
    description: str
    match_score: float
    
    class Config:
        from_attributes = True