import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_AVAILABLE = bool(OPENAI_API_KEY)

# Google Gemini Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_AVAILABLE = bool(GEMINI_API_KEY)

# Default provider preference
DEFAULT_PROVIDER = os.getenv('DEFAULT_AI_PROVIDER', 'gemini')

if OPENAI_AVAILABLE:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

if GEMINI_AVAILABLE:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')

def generate_personalized_guidance(career_name, level, skills=None):
    """
    Generate personalized career guidance using AI (Gemini by default, falls back to OpenAI).
    Falls back to template-based guidance if API is not available.
    
    Args:
        career_name: Career name
        level: User level (student/fresher/professional)
        skills: User's current skills (optional)
    
    Returns:
        dict: Generated guidance
    """
    
    skills_context = f"\nUser's current skills: {', '.join(skills)}" if skills else ""
    
    prompt = f"""Act as an expert career counselor. Provide personalized guidance for someone interested in {career_name} career.

User Details:
- Career Interest: {career_name}
- Current Level: {level}{skills_context}

Provide:
1. A personalized introduction (2-3 sentences)
2. Why this career is suitable
3. Top 3 immediate action items
4. Potential challenges and how to overcome them
5. Expected timeline to get first job/role

Make it conversational, encouraging, and practical."""

    # Try Gemini first if available
    if GEMINI_AVAILABLE and DEFAULT_PROVIDER == 'gemini':
        try:
            response = gemini_model.generate_content(prompt)
            return {
                "status": "success",
                "personalized_guidance": response.text,
                "model": "gemini-pro",
                "provider": "Google Gemini"
            }
        except Exception as e:
            print(f"Gemini error: {str(e)}")
            # Fall through to OpenAI or return error
    
    # Try OpenAI if available
    if OPENAI_AVAILABLE:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert career counselor providing personalized career guidance."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return {
                "status": "success",
                "personalized_guidance": response.choices[0].message.content,
                "model": "gpt-3.5-turbo",
                "provider": "OpenAI"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating guidance: {str(e)}"
            }
    
    return None


def generate_interview_prep(career_name):
    """
    Generate interview preparation tips using AI.
    
    Args:
        career_name: Target career
    
    Returns:
        dict: Interview preparation guide
    """
    prompt = f"""Generate an interview preparation guide for a {career_name} position.

Include:
1. Top 10 interview questions likely to be asked
2. How to structure your answers
3. Sample answers for 3 key questions
4. Questions to ask the interviewer
5. Common mistakes to avoid

Format as a practical guide."""

    # Try Gemini first
    if GEMINI_AVAILABLE and DEFAULT_PROVIDER == 'gemini':
        try:
            response = gemini_model.generate_content(prompt)
            return {
                "status": "success",
                "interview_guide": response.text,
                "provider": "Google Gemini"
            }
        except Exception as e:
            print(f"Gemini error: {str(e)}")
    
    # Try OpenAI
    if OPENAI_AVAILABLE:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in interview preparation and career development."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            return {
                "status": "success",
                "interview_guide": response.choices[0].message.content,
                "provider": "OpenAI"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating interview guide: {str(e)}"
            }
    
    return None


def analyze_career_fit(career_name, user_profile):
    """
    Analyze how well a career fits the user's profile.
    
    Args:
        career_name: Career to analyze
        user_profile: Dict with user's skills, interests, personality
    
    Returns:
        dict: Career fit analysis
    """
    profile_str = "\n".join([f"- {k}: {v}" for k, v in user_profile.items()])
    
    prompt = f"""Analyze how well the {career_name} career aligns with this profile:

{profile_str}

Provide:
1. Overall fit score (1-10)
2. Strengths that align with this career
3. Potential challenges
4. Recommendations for success
5. Alternative careers to consider

Be honest and constructive."""

    # Try Gemini first
    if GEMINI_AVAILABLE and DEFAULT_PROVIDER == 'gemini':
        try:
            response = gemini_model.generate_content(prompt)
            return {
                "status": "success",
                "analysis": response.text,
                "provider": "Google Gemini"
            }
        except Exception as e:
            print(f"Gemini error: {str(e)}")
    
    # Try OpenAI
    if OPENAI_AVAILABLE:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a career counselor evaluating career fit based on user profiles."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            return {
                "status": "success",
                "analysis": response.choices[0].message.content,
                "provider": "OpenAI"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error analyzing career fit: {str(e)}"
            }
    
    return None


def get_ai_status():
    """Check if AI integration is available."""
    status = {
        "gemini_available": GEMINI_AVAILABLE,
        "openai_available": OPENAI_AVAILABLE,
        "default_provider": DEFAULT_PROVIDER if (GEMINI_AVAILABLE or OPENAI_AVAILABLE) else "none",
        "providers": []
    }
    
    if GEMINI_AVAILABLE:
        status["providers"].append({
            "name": "Google Gemini",
            "model": "gemini-pro",
            "status": "Active"
        })
    
    if OPENAI_AVAILABLE:
        status["providers"].append({
            "name": "OpenAI",
            "model": "gpt-3.5-turbo",
            "status": "Active"
        })
    
    if not GEMINI_AVAILABLE and not OPENAI_AVAILABLE:
        status["message"] = "No AI providers configured. Set GEMINI_API_KEY or OPENAI_API_KEY"
    else:
        status["message"] = f"AI features enabled: {', '.join([p['name'] for p in status['providers']])}"
    
    return status
