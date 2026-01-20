from .career_data import CAREER_DB as CAREER_DATA
from .utils import normalize_text, find_best_match


def get_career_guidance(user_career):
    user_career = normalize_text(user_career)

    matched_career = find_best_match(user_career, CAREER_DATA)

    if matched_career:
        career_info = CAREER_DATA[matched_career]

        return {
            "career": matched_career.title(),
            "roadmap": career_info["roadmap"],
            "skills": career_info["skills"],
            "resources": career_info["resources"],
            "market": career_info["market"],
            "future": career_info["future"]
        }

    # Fallback if career not found
    return {
        "career": user_career.title(),
        "roadmap": [
            "Explore fundamentals",
            "Identify transferable skills",
            "Research similar roles",
            "Build beginner projects"
        ],
        "skills": [
            "Problem-solving", "Communication", "Adaptability"
        ],
        "resources": [
            "Google",
            "LinkedIn Learning",
            "YouTube"
        ],
        "market": "Emerging or niche career – research required",
        "future": "Depends on skill development and industry trends"
    }
