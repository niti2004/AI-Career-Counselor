"""
Career Comparison Module
Provides side-by-side comparison of careers
"""
from .career_data import CAREER_DB
from .fuzzy_matcher import find_best_career_match

def compare_careers(career_names: list) -> dict:
    """Compare 2-3 careers side by side"""
    if not career_names or len(career_names) == 0:
        return {"status": "error", "message": "No careers provided for comparison"}
    
    if len(career_names) > 3:
        career_names = career_names[:3]  # Limit to 3 careers
    
    # Find best matches for the requested careers
    careers_to_compare = []
    for career_input in career_names:
        match = find_best_career_match(career_input)
        if match and match in CAREER_DB:
            careers_to_compare.append(match)
        else:
            # Try direct lookup
            for db_career in CAREER_DB.keys():
                if db_career.lower() == career_input.lower():
                    careers_to_compare.append(db_career)
                    break
            else:
                return {
                    "status": "error",
                    "message": f"Career '{career_input}' not found. Available: " + ", ".join(list(CAREER_DB.keys())[:5])
                }
    
    if len(set(careers_to_compare)) < len(careers_to_compare):
        return {
            "status": "error",
            "message": "Please provide different careers for comparison"
        }
    
    # Build comparison data
    comparison = {
        "status": "success",
        "careers": [],
        "comparison_categories": [
            "salary",
            "job_outlook",
            "description",
            "skills",
            "growth",
            "work_environment",
            "typical_day"
        ]
    }
    
    for career_name in careers_to_compare:
        career_data = CAREER_DB[career_name]
        
        career_info = {
            "name": career_name.title(),
            "salary": career_data.get("salary", {}),
            "job_outlook": career_data.get("job_outlook", "Data not available"),
            "description": career_data.get("description", ""),
            "skills": career_data.get("skills", []),
            "growth": career_data.get("growth", {}),
            "market": career_data.get("market", ""),
            "future": career_data.get("future", ""),
            "work_environment": career_data.get("work_environment", ""),
            "typical_day": career_data.get("typical_day", ""),
            "resources": career_data.get("resources", []),
            "roadmap": career_data.get("roadmap", [])
        }
        
        comparison["careers"].append(career_info)
    
    return comparison


def get_salary_comparison(career_names: list) -> dict:
    """Get salary comparison across careers"""
    comparison = compare_careers(career_names)
    
    if comparison["status"] != "success":
        return comparison
    
    salary_data = {
        "status": "success",
        "careers": []
    }
    
    for career in comparison["careers"]:
        salary_data["careers"].append({
            "name": career["name"],
            "salary": career["salary"],
            "market": career["market"]
        })
    
    return salary_data


def get_skill_comparison(career_names: list) -> dict:
    """Get skill comparison across careers"""
    comparison = compare_careers(career_names)
    
    if comparison["status"] != "success":
        return comparison
    
    # Find common and unique skills
    all_careers_data = comparison["careers"]
    all_skills = set()
    for career in all_careers_data:
        all_skills.update(career["skills"])
    
    skill_comparison = {
        "status": "success",
        "careers": []
    }
    
    for career in all_careers_data:
        common_skills = set(career["skills"]) & all_skills
        
        skill_comparison["careers"].append({
            "name": career["name"],
            "required_skills": career["skills"],
            "common_with_others": list(common_skills),
            "unique_skills": list(set(career["skills"]) - all_skills.intersection(*[set(c["skills"]) for c in all_careers_data if c["name"] != career["name"]]))
        })
    
    return skill_comparison


def get_growth_comparison(career_names: list) -> dict:
    """Get career growth path comparison"""
    comparison = compare_careers(career_names)
    
    if comparison["status"] != "success":
        return comparison
    
    growth_data = {
        "status": "success",
        "careers": []
    }
    
    for career in comparison["careers"]:
        growth_data["careers"].append({
            "name": career["name"],
            "growth_path": career["growth"],
            "market": career["market"],
            "future": career["future"],
            "job_outlook": career["job_outlook"]
        })
    
    return growth_data


def get_career_fit_score(career_names: list, user_skills: list = None) -> dict:
    """Get fit score for careers based on user skills"""
    if not user_skills or len(user_skills) == 0:
        user_skills = []
    
    comparison = compare_careers(career_names)
    
    if comparison["status"] != "success":
        return comparison
    
    fit_data = {
        "status": "success",
        "careers": [],
        "user_skills": user_skills
    }
    
    user_skills_set = set(skill.lower() for skill in user_skills)
    
    for career in comparison["careers"]:
        career_skills = set(skill.lower() for skill in career["skills"])
        
        if len(career_skills) > 0:
            matching_skills = user_skills_set & career_skills
            missing_skills = career_skills - user_skills_set
            
            fit_percentage = int((len(matching_skills) / len(career_skills)) * 100) if career_skills else 0
        else:
            fit_percentage = 0
            matching_skills = set()
            missing_skills = set()
        
        fit_data["careers"].append({
            "name": career["name"],
            "fit_score": fit_percentage,
            "matching_skills": list(matching_skills),
            "missing_skills": list(missing_skills),
            "salary_range": career["salary"],
            "description": career["description"]
        })
    
    # Sort by fit score
    fit_data["careers"].sort(key=lambda x: x["fit_score"], reverse=True)
    
    return fit_data


def get_career_details(career_name: str) -> dict:
    """Get comprehensive details for a single career"""
    career = find_best_career_match(career_name)
    
    if not career or career not in CAREER_DB:
        return {
            "status": "error",
            "message": f"Career '{career_name}' not found"
        }
    
    career_data = CAREER_DB[career]
    
    return {
        "status": "success",
        "name": career.title(),
        "data": {
            "description": career_data.get("description", ""),
            "salary": career_data.get("salary", {}),
            "job_outlook": career_data.get("job_outlook", ""),
            "market": career_data.get("market", ""),
            "future": career_data.get("future", ""),
            "work_environment": career_data.get("work_environment", ""),
            "typical_day": career_data.get("typical_day", ""),
            "skills": career_data.get("skills", []),
            "growth": career_data.get("growth", {}),
            "roadmap": career_data.get("roadmap", []),
            "resources": career_data.get("resources", [])
        }
    }
