# test_api.py
import requests
import json

# Base URL of your API
BASE_URL = "http://localhost:8000"

def test_populate_dummy_data():
    """Populate database with dummy data"""
    print("Populating dummy data...")
    response = requests.post(f"{BASE_URL}/api/populate-dummy-data")
    print(response.json())
    print("-" * 50)

def test_get_form_options():
    """Test getting form options"""
    print("Getting form options...")
    response = requests.get(f"{BASE_URL}/api/form-options")
    if response.status_code == 200:
        options = response.json()
        print("Education Options:", options["education_options"])
        print("Sector Options:", options["sector_options"])
        print("Location Options:", options["location_options"])
        print("Skills Options (first 5):", options["skills_options"][:5])
    print("-" * 50)

def test_get_recommendations():
    """Test getting recommendations"""
    print("Getting recommendations for a student...")
    
    # Sample student data
    student_data = {
        "education": "Bachelor's",
        "skills": ["Python", "Machine Learning", "SQL"],
        "sector": "IT",
        "preferred_location": "Mumbai",
        "description": "I am passionate about data science and machine learning. I have experience with Python programming and want to work on real-world AI projects."
    }
    
    response = requests.post(
        f"{BASE_URL}/api/recommendations",
        json=student_data
    )
    
    if response.status_code == 200:
        recommendations = response.json()
        print(f"Found {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['title']}")
            print(f"   Score: {rec['match_score']}/100")
            print(f"   Location: {rec['location']}")
            print(f"   Sector: {rec['sector']}")
            print(f"   Skills: {rec['skills']}")
    else:
        print("Error:", response.json())
    print("-" * 50)

def test_different_profile():
    """Test with a different student profile"""
    print("Testing with Marketing student profile...")
    
    student_data = {
        "education": "12th Pass",
        "skills": ["Content Writing", "Social Media Marketing", "SEO"],
        "sector": "Marketing",
        "preferred_location": "Remote",
        "description": "I love creating content and managing social media. Looking for opportunities in digital marketing."
    }
    
    response = requests.post(
        f"{BASE_URL}/api/recommendations",
        json=student_data
    )
    
    if response.status_code == 200:
        recommendations = response.json()
        print(f"Found {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['title']}")
            print(f"   Score: {rec['match_score']}/100")
            print(f"   Location: {rec['location']}")

if __name__ == "__main__":
    print("Testing Internship Recommendation API")
    print("=" * 50)
    
    # First populate dummy data
    test_populate_dummy_data()
    
    # Test getting form options
    test_get_form_options()
    
    # Test getting recommendations
    test_get_recommendations()
    
    # Test with different profile
    test_different_profile()