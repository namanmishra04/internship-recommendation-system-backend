# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, Text
from .database import Base

class Internship(Base):
    __tablename__ = "internships"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    min_education = Column(String(100), nullable=False)  # e.g., "Bachelor's", "Master's", "12th Pass"
    skills = Column(Text, nullable=False)  # Comma-separated skills
    sector = Column(String(100), nullable=False)  # e.g., "IT", "Finance", "Marketing"
    location = Column(String(100), nullable=False)  # e.g., "Delhi", "Mumbai", "Remote"
    duration = Column(String(50), nullable=False)  # e.g., "3 months", "6 months"
    no_of_posts = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    description = Column(Text, nullable=False)  # Detailed roles and responsibilities