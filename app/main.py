# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Internship Recommendation System",
    description="Backend API for PM Internship Scheme Platform",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Internship Recommendation System API"}

@app.get("/api/form-options", response_model=schemas.FormOptions)
def get_form_options(db: Session = Depends(get_db)):
    """
    Get dropdown options for the student form
    """
    options = crud.get_form_options(db)
    return schemas.FormOptions(**options)

@app.post("/api/recommendations", response_model=List[schemas.RecommendationResponse])
def get_recommendations(
    student_form: schemas.StudentForm,
    db: Session = Depends(get_db)
):
    """
    Get top 5 internship recommendations based on student profile
    """
    recommendations = crud.get_recommendations(db, student_form)
    
    if not recommendations:
        raise HTTPException(
            status_code=404, 
            detail="No matching internships found for your profile"
        )
    
    return recommendations

@app.get("/api/internships", response_model=List[schemas.InternshipResponse])
def get_all_internships(db: Session = Depends(get_db)):
    """
    Get all active internships (for admin/testing purposes)
    """
    internships = crud.get_all_internships(db)
    return internships

@app.post("/api/internships", response_model=schemas.InternshipResponse)
def create_internship(
    internship: schemas.InternshipCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new internship (for populating database)
    """
    return crud.create_internship(db, internship)

# Optional: Add endpoint to populate dummy data
@app.post("/api/populate-dummy-data")
def populate_dummy_data(db: Session = Depends(get_db)):
    """
    Populate database with dummy internship data
    """
    dummy_internships = [
        {
            "title": "Web Development Intern",
            "min_education": "Bachelor's",
            "skills": "HTML, CSS, JavaScript, React, Node.js",
            "sector": "IT",
            "location": "Delhi",
            "duration": "3 months",
            "no_of_posts": 5,
            "is_active": True,
            "description": "Looking for enthusiastic web development interns to work on modern web applications. You will be working with React and Node.js to build scalable solutions."
        },
        {
            "title": "Data Science Intern",
            "min_education": "Bachelor's",
            "skills": "Python, Machine Learning, SQL, Pandas, NumPy",
            "sector": "IT",
            "location": "Mumbai",
            "duration": "6 months",
            "no_of_posts": 3,
            "is_active": True,
            "description": "Join our data science team to work on real-world ML projects. Experience with Python and data analysis libraries required."
        },
        {
            "title": "Digital Marketing Intern",
            "min_education": "12th Pass",
            "skills": "Social Media Marketing, Content Writing, SEO, Google Analytics",
            "sector": "Marketing",
            "location": "Remote",
            "duration": "3 months",
            "no_of_posts": 10,
            "is_active": True,
            "description": "Help us grow our digital presence through social media campaigns and content marketing strategies."
        },
        {
            "title": "Finance Analyst Intern",
            "min_education": "Bachelor's",
            "skills": "Excel, Financial Analysis, Accounting, Tally",
            "sector": "Finance",
            "location": "Bangalore",
            "duration": "4 months",
            "no_of_posts": 2,
            "is_active": True,
            "description": "Assist in financial planning, budgeting, and analysis. Strong Excel skills and understanding of financial concepts required."
        },
        {
            "title": "Mobile App Development Intern",
            "min_education": "Bachelor's",
            "skills": "Flutter, React Native, Mobile Development, JavaScript",
            "sector": "IT",
            "location": "Hyderabad",
            "duration": "6 months",
            "no_of_posts": 4,
            "is_active": True,
            "description": "Develop cross-platform mobile applications using Flutter or React Native. Work on innovative mobile solutions."
        },
        {
            "title": "Content Writing Intern",
            "min_education": "12th Pass",
            "skills": "Content Writing, Research, SEO Writing, Blogging",
            "sector": "Marketing",
            "location": "Remote",
            "duration": "2 months",
            "no_of_posts": 8,
            "is_active": True,
            "description": "Create engaging content for blogs, websites, and social media. Strong writing and research skills needed."
        },
        {
            "title": "HR Management Intern",
            "min_education": "Bachelor's",
            "skills": "Recruitment, Communication, MS Office, HR Policies",
            "sector": "HR",
            "location": "Delhi",
            "duration": "3 months",
            "no_of_posts": 2,
            "is_active": True,
            "description": "Support HR team in recruitment, onboarding, and employee engagement activities."
        },
        {
            "title": "Graphic Design Intern",
            "min_education": "Diploma",
            "skills": "Photoshop, Illustrator, Canva, UI/UX Design",
            "sector": "Design",
            "location": "Mumbai",
            "duration": "3 months",
            "no_of_posts": 3,
            "is_active": True,
            "description": "Create visual content for digital and print media. Experience with design software required."
        },
        {
            "title": "Backend Development Intern",
            "min_education": "Bachelor's",
            "skills": "Python, Django, FastAPI, PostgreSQL, REST APIs",
            "sector": "IT",
            "location": "Pune",
            "duration": "4 months",
            "no_of_posts": 3,
            "is_active": True,
            "description": "Build robust backend systems and APIs using Python frameworks. Database knowledge essential."
        },
        {
            "title": "Sales & Marketing Intern",
            "min_education": "12th Pass",
            "skills": "Sales, Communication, Customer Service, MS Office",
            "sector": "Sales",
            "location": "Chennai",
            "duration": "3 months",
            "no_of_posts": 6,
            "is_active": True,
            "description": "Support sales team in lead generation and customer relationship management."
        }
    ]
    
    created_count = 0
    for internship_data in dummy_internships:
        try:
            internship = schemas.InternshipCreate(**internship_data)
            crud.create_internship(db, internship)
            created_count += 1
        except Exception as e:
            continue
    
    return {"message": f"Successfully created {created_count} dummy internships"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)