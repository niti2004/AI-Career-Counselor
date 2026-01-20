from .career_data import CAREER_DB, CAREER_LEVELS
from .fuzzy_matcher import find_best_career_match, find_similar_careers
from .recommender import recommend_careers_by_skills, find_skill_gap
from .llm_guidance import generate_personalized_guidance, get_ai_status

def career_guidance(career, level="fresher"):
    """
    Provides structured career guidance with AI enhancements.
    Uses fuzzy matching and skill-based recommendations.
    
    Args:
        career: Career interest (string)
        level: User level - "student", "fresher", or "professional"
    
    Returns:
        Dictionary with structured career guidance
    """
    
    # Normalize user input
    career = career.lower().strip()
    level = level.lower().strip() if level else "fresher"
    
    # Validate level
    if level not in CAREER_LEVELS:
        level = "fresher"
    
    # Try fuzzy matching first (handles typos)
    best_match, confidence = find_best_career_match(career)
    
    if best_match:
        career_info = CAREER_DB[best_match]
        level_info = CAREER_LEVELS[level]
        
        # Customize roadmap based on level
        roadmap = career_info["roadmap"].copy()
        if level == "student":
            roadmap.insert(0, "Focus on fundamentals and pursue internships")
        elif level == "professional":
            roadmap.insert(0, "Consider specialization and leadership development")
        
        # Try to get AI-powered personalized guidance
        ai_guidance = None
        if confidence < 100:  # Show confidence if fuzzy matched
            ai_guidance = generate_personalized_guidance(best_match, level)
        
        result = {
            "status": "success",
            "career": best_match.title(),
            "match_confidence": confidence,  # Show fuzzy match confidence
            "level": level.title(),
            "focus": level_info["focus"],
            "roadmap": roadmap,
            "skills": career_info["skills"],
            "resources": career_info["resources"],
            "market": career_info["market"],
            "future": career_info["future"],
            "tips": level_info["tips"]
        }
        
        # Add AI-generated guidance if available
        if ai_guidance and ai_guidance.get("status") == "success":
            result["ai_personalized_guidance"] = ai_guidance.get("personalized_guidance")
        
        # Find and include similar careers
        similar = find_similar_careers(best_match, top_n=2)
        if similar:
            result["similar_careers"] = [
                {"career": c.title(), "similarity": f"{round(s*100, 0)}%"} 
                for c, s in similar
            ]
        
        return result
    else:
        # Fallback for unknown careers
        return {
            "status": "unknown",
            "career": career.title(),
            "message": f"'{career.title()}' is an emerging or specialized career path. Let's explore transferable skills instead.",
            "suggestion": "Consider searching for related careers like: Software Engineer, Data Analyst, Product Manager",
            "tips": [
                "Research companies and job postings for this role",
                "Identify key skills mentioned in job descriptions",
                "Build a portfolio demonstrating relevant skills",
                "Network with professionals in this field"
            ]
        }


def recommend_by_skills(skills_list):
    """
    Recommend careers based on user's skills.
    
    Args:
        skills_list: List of user skills
    
    Returns:
        Dictionary with career recommendations
    """
    recommendations = recommend_careers_by_skills(skills_list, top_n=5)
    
    if recommendations:
        result = {
            "status": "success",
            "input_skills": skills_list,
            "recommendations": []
        }
        
        for career, score, matching in recommendations:
            result["recommendations"].append({
                "career": career.title(),
                "match_score": f"{round(score*100, 1)}%",
                "matching_skills": matching,
                "skills_to_learn": len(CAREER_DB[career]["skills"]) - len(matching)
            })
        
        return result
    else:
        return {
            "status": "error",
            "message": "Unable to generate recommendations. Please provide valid skills."
        }


def analyze_skill_gap(career, skills_list):
    """
    Analyze what skills user needs to learn for a career.
    
    Args:
        career: Target career
        skills_list: User's current skills
    
    Returns:
        Dictionary with skill gap analysis
    """
    # Fuzzy match the career first
    best_match, _ = find_best_career_match(career)
    
    if not best_match:
        return {
            "status": "unknown",
            "message": f"Career '{career}' not found in database"
        }
    
    gap = find_skill_gap(best_match, skills_list)
    
    if gap:
        return {
            "status": "success",
            **gap,
            "career": best_match.title(),
            "analysis_summary": f"You have {gap['current_skills']}/{gap['total_skills']} required skills ({gap['skill_match_percentage']}%)"
        }
    
    return {"status": "error", "message": "Unable to analyze skill gap"}


def get_ai_features():
    """Get status of all AI features."""
    return {
        "features": {
            "fuzzy_matching": True,
            "skill_recommendation": True,
            "skill_gap_analysis": True,
            "personalized_guidance": get_ai_status()
        }
    }
