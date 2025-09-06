# app/crud.py
from sqlalchemy.orm import Session
from typing import List, Dict
from . import models, schemas
from .scoring import calculate_total_score

def get_all_internships(db: Session):
    return db.query(models.Internship).filter(models.Internship.is_active == True).all()

def create_internship(db: Session, internship: schemas.InternshipCreate):
    db_internship = models.Internship(**internship.dict())
    db.add(db_internship)
    db.commit()
    db.refresh(db_internship)
    return db_internship

def get_form_options(db: Session) -> Dict:
    """
    Get unique values for form dropdowns
    """
    internships = get_all_internships(db)
    
    education_options = set()
    skills_options = set()
    sector_options = set()
    location_options = set()
    
    for internship in internships:
        education_options.add(internship.min_education)
        sector_options.add(internship.sector)
        location_options.add(internship.location)
        
        # Split skills and add individually
        for skill in internship.skills.split(','):
            skills_options.add(skill.strip())
    
    return {
        "education_options": sorted(list(education_options)),
        "skills_options": sorted(list(skills_options)),
        "sector_options": sorted(list(sector_options)),
        "location_options": sorted(list(location_options))
    }

def get_recommendations(db: Session, student_form: schemas.StudentForm) -> List[Dict]:
    """
    Get top 5 internship recommendations based on student profile
    """
    # Get all active internships
    internships = get_all_internships(db)
    
    # Convert student form to dict for scoring
    student_data = {
        "education": student_form.education,
        "skills": student_form.skills,
        "sector": student_form.sector,
        "preferred_location": student_form.preferred_location,
        "description": student_form.description
    }
    
    # Calculate scores for each internship
    scored_internships = []
    for internship in internships:
        score = calculate_total_score(internship, student_data)
        
        # Only include internships with score > 0
        if score > 0:
            scored_internships.append({
                "internship": internship,
                "score": score
            })
    
    # Sort by score (descending) and get top 20-30
    scored_internships.sort(key=lambda x: x["score"], reverse=True)
    top_internships = scored_internships[:30]  # Get top 30 for further filtering
    
    # In production, here you would apply ML model for better ranking
    # For now, we'll use the existing scores
    
    # Get top 5
    top_5 = top_internships[:5]
    
    # Format response
    recommendations = []
    for item in top_5:
        internship = item["internship"]
        recommendations.append({
            "id": internship.id,
            "title": internship.title,
            "sector": internship.sector,
            "location": internship.location,
            "skills": internship.skills,
            "duration": internship.duration,
            "description": internship.description,
            "match_score": round(item["score"], 2)
        })
    
    return recommendations