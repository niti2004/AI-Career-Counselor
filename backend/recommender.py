from .career_data import CAREER_DB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend_careers_by_skills(user_skills, top_n=5):
    """
    Recommend careers based on user's skills using TF-IDF and cosine similarity.
    
    Args:
        user_skills: List of user skills (strings)
        top_n: Number of recommendations to return
    
    Returns:
        list: List of (career_name, match_score, matching_skills) tuples
    """
    if not user_skills or len(user_skills) == 0:
        return []
    
    # Create skill profiles
    career_skill_profiles = {}
    for career, info in CAREER_DB.items():
        career_skill_profiles[career] = " ".join(info["skills"])
    
    user_profile = " ".join(user_skills).lower()
    
    # Vectorize skills using TF-IDF
    all_profiles = [user_profile] + list(career_skill_profiles.values())
    
    try:
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 2))
        vectors = vectorizer.fit_transform(all_profiles)
        
        # Calculate similarity between user skills and each career
        similarities = cosine_similarity(vectors[0:1], vectors[1:])[0]
        
        # Get results with scores
        results = []
        for idx, (career, score) in enumerate(zip(career_skill_profiles.keys(), similarities)):
            career_skills = set(CAREER_DB[career]["skills"])
            user_skills_set = set(skill.lower() for skill in user_skills)
            
            # Find matching skills
            matching = [s for s in career_skills if any(
                user_skill.lower() in s.lower() or s.lower() in user_skill.lower() 
                for user_skill in user_skills
            )]
            
            results.append((career, float(score), matching))
        
        # Sort by score and return top N
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]
    except:
        return []


def get_career_by_skills_match(skills_list):
    """
    Find the best matching career for a list of skills.
    
    Args:
        skills_list: List of skills user has
    
    Returns:
        dict: Career recommendation with details
    """
    if not skills_list:
        return None
    
    recommendations = recommend_careers_by_skills(skills_list, top_n=1)
    
    if recommendations:
        career_name, score, matching_skills = recommendations[0]
        return {
            "career": career_name,
            "match_percentage": round(score * 100, 2),
            "matching_skills": matching_skills,
            "skills_to_learn": [s for s in CAREER_DB[career_name]["skills"] if s not in matching_skills]
        }
    
    return None


def find_skill_gap(desired_career, user_skills):
    """
    Analyze skill gap between user's current skills and desired career.
    
    Args:
        desired_career: Target career name
        user_skills: List of user's current skills
    
    Returns:
        dict: Analysis of skill gap
    """
    if desired_career not in CAREER_DB:
        return None
    
    career_skills = set(CAREER_DB[desired_career]["skills"])
    user_skills_set = set(skill.lower() for skill in user_skills)
    
    career_skills_lower = set(s.lower() for s in career_skills)
    
    # Find matching and missing skills
    matching_skills = [s for s in career_skills if s.lower() in user_skills_set]
    missing_skills = [s for s in career_skills if s.lower() not in user_skills_set]
    
    return {
        "career": desired_career,
        "current_skills": len(matching_skills),
        "total_skills": len(career_skills),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": round((len(matching_skills) / len(career_skills)) * 100, 2) if career_skills else 0
    }
