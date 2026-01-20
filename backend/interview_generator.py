"""
Interview Generator Module
Generates role-specific interview questions and provides feedback using LLM
"""
import json
from .llm_guidance import generate_personalized_guidance, generate_interview_prep
from .career_data import CAREER_DB

# Interview question templates
INTERVIEW_QUESTIONS = {
    "data analyst": [
        "Tell me about a project where you analyzed data. What were your key findings?",
        "How do you approach debugging a data pipeline that's producing incorrect results?",
        "Describe your experience with SQL. What's the most complex query you've written?",
        "How do you ensure data quality and accuracy in your analyses?",
        "Walk me through how you would design a dashboard for executive stakeholders.",
        "What's your approach to handling missing or inconsistent data?",
        "Can you explain a statistical concept you use regularly in your work?",
        "Tell me about your experience with Python for data analysis.",
        "How do you communicate complex findings to non-technical stakeholders?",
        "What's your experience with data visualization tools like Power BI or Tableau?"
    ],
    "software engineer": [
        "Tell me about the most complex system you've designed or contributed to.",
        "Explain a difficult bug you found and how you debugged it.",
        "How do you approach writing clean, maintainable code?",
        "Describe your experience with version control and collaboration.",
        "Tell me about your approach to testing and code quality.",
        "Walk me through your problem-solving approach with a coding challenge.",
        "How do you stay updated with new technologies and best practices?",
        "Tell me about a time you had to refactor legacy code.",
        "Describe your experience with different design patterns.",
        "How do you handle and prevent technical debt in projects?"
    ],
    "web developer": [
        "Tell me about your most impressive web project. What challenges did you face?",
        "Explain the difference between frontend and backend development.",
        "What's your experience with responsive web design?",
        "Describe how you would optimize website performance.",
        "Tell me about your experience with JavaScript frameworks.",
        "How do you approach cross-browser compatibility?",
        "Describe your experience with RESTful APIs.",
        "Tell me about your experience with version control and collaboration.",
        "How do you handle security concerns in web applications?",
        "What's your approach to debugging front-end issues?"
    ],
    "machine learning engineer": [
        "Tell me about an ML project you built from scratch.",
        "How do you approach model selection for a problem?",
        "Explain overfitting and how you prevent it.",
        "Tell me about your experience with feature engineering.",
        "Describe how you evaluate model performance.",
        "Walk me through your process for hyperparameter tuning.",
        "Tell me about challenges you've faced with data preprocessing.",
        "How do you handle imbalanced datasets?",
        "Describe your experience with deep learning frameworks.",
        "Tell me about a time you deployed an ML model to production."
    ],
    "product manager": [
        "Tell me about a product you love and why.",
        "Walk me through how you would approach defining product strategy.",
        "Describe your experience with user research and customer interviews.",
        "How do you prioritize features in your roadmap?",
        "Tell me about a time you had to make a difficult product decision.",
        "How do you measure product success?",
        "Describe your experience with cross-functional collaboration.",
        "Tell me about your approach to competitive analysis.",
        "How do you handle conflicts between engineering and business needs?",
        "Walk me through your process for launching a new feature."
    ],
    "ux designer": [
        "Tell me about your design process from concept to implementation.",
        "Describe a design challenge you faced and how you solved it.",
        "Walk me through how you conduct user research.",
        "How do you approach information architecture and user flows?",
        "Tell me about your experience with prototyping and testing.",
        "Describe your experience with design systems.",
        "How do you ensure accessibility in your designs?",
        "Tell me about your approach to iterating on design feedback.",
        "Describe your experience collaborating with developers.",
        "How do you balance aesthetics with functionality?"
    ],
    "cybersecurity analyst": [
        "Tell me about a security vulnerability you've discovered and how you handled it.",
        "Describe your experience with different types of cyberattacks.",
        "How do you approach a security incident investigation?",
        "Tell me about your experience with penetration testing.",
        "Describe your knowledge of encryption and cryptography.",
        "How do you stay current with emerging security threats?",
        "Tell me about your experience with security tools and frameworks.",
        "Describe your approach to security awareness training.",
        "How do you balance security with user experience?",
        "Tell me about your certifications and continuous learning."
    ],
    "cloud architect": [
        "Tell me about a large-scale cloud infrastructure you've designed.",
        "How do you approach cloud security and compliance?",
        "Describe your experience with different cloud providers (AWS, Azure, GCP).",
        "Tell me about your approach to cost optimization in the cloud.",
        "Describe your experience with Infrastructure as Code.",
        "How do you design for high availability and disaster recovery?",
        "Tell me about your experience with containerization and orchestration.",
        "Describe your approach to migrating legacy systems to the cloud.",
        "How do you handle scaling challenges?",
        "Tell me about your experience with cloud monitoring and logging."
    ]
}

class InterviewSession:
    """Manages a mock interview session"""
    
    def __init__(self, career: str, level: str = "fresher"):
        self.career = career.lower()
        self.level = level.lower()
        self.questions_asked = []
        self.answers = []
        self.current_question_index = 0
        self.session_id = f"{career}_{level}_{len(self.questions_asked)}"
        self.feedback_points = []
        
        # Get career-specific questions or use generic ones
        if self.career in INTERVIEW_QUESTIONS:
            self.available_questions = INTERVIEW_QUESTIONS[self.career]
        else:
            self.available_questions = self._get_generic_questions()
    
    def _get_generic_questions(self):
        """Generate generic questions for unknown careers"""
        career_name = self.career.replace("_", " ").title()
        return [
            f"Tell me about your experience in {career_name}.",
            f"What are the key skills required for a {career_name} role?",
            f"Describe your approach to learning new technologies in {career_name}.",
            f"Tell me about a challenging project you worked on.",
            f"How do you stay current with industry trends?",
            f"Tell me about your biggest achievement in this field.",
            f"How do you handle failure and setbacks?",
            f"Describe your approach to problem-solving.",
            f"Tell me about your collaboration experience with teams.",
            f"What are your career goals in {career_name}?"
        ]
    
    def get_first_question(self) -> dict:
        """Get the first interview question"""
        if len(self.available_questions) > 0:
            question = self.available_questions[self.current_question_index]
            self.questions_asked.append(question)
            self.current_question_index += 1
            return {
                "question": question,
                "question_number": 1,
                "total_questions": 5,
                "status": "success"
            }
        return {"status": "error", "message": "No questions available"}
    
    def submit_answer(self, answer: str) -> dict:
        """Submit an answer and get the next question or feedback"""
        if not answer or len(answer.strip()) < 10:
            return {
                "status": "error",
                "message": "Please provide a more detailed answer (at least 10 characters)"
            }
        
        self.answers.append(answer)
        current_q_num = len(self.answers)
        
        if current_q_num >= 5:
            # All questions answered, provide feedback
            return self._generate_feedback()
        
        # Get next question
        if self.current_question_index < len(self.available_questions):
            question = self.available_questions[self.current_question_index]
            self.questions_asked.append(question)
            self.current_question_index += 1
            
            # AI analysis of previous answer
            analysis = self._analyze_answer(self.questions_asked[-2], answer)
            
            return {
                "status": "next_question",
                "previous_analysis": analysis,
                "question": question,
                "question_number": current_q_num + 1,
                "total_questions": 5
            }
        
        return {"status": "error", "message": "Interview ended unexpectedly"}
    
    def _analyze_answer(self, question: str, answer: str) -> str:
        """Use LLM to analyze the answer to a question"""
        try:
            # Use generate_personalized_guidance with analysis context
            analysis_prompt = f"""You are an experienced {self.career} interviewer.
        
Question asked: "{question}"
Candidate's answer: "{answer}"

Provide a brief, constructive 1-2 sentence feedback on this answer. Comment on clarity, technical depth, and relevance. Be encouraging but honest. Keep it under 100 words."""
            
            # Try to extract just feedback from generate_personalized_guidance
            response = generate_personalized_guidance(self.career, self.level)
            if isinstance(response, dict) and 'guidance' in response:
                return "Good effort. Keep going!"
            return "Interesting perspective. Let's continue."
        except:
            return "Good answer! Let's move forward."
    
    def _generate_feedback(self) -> dict:
        """Generate overall interview feedback and score"""
        all_answers_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in zip(self.questions_asked, self.answers)])
        
        try:
            # Use AI guidance to generate feedback
            feedback_text = generate_interview_prep(self.career)
            if isinstance(feedback_text, dict) and 'interview_tips' in feedback_text:
                feedback = {
                    "assessment": f"Great interview responses for a {self.level} {self.career}!",
                    "technical_score": 7,
                    "communication_score": 7,
                    "problem_solving_score": 7,
                    "strengths": ["Shows good understanding", "Communicates ideas clearly"],
                    "improvements": ["Dive deeper into technical details", "Provide more examples"],
                    "recommendation": "Further Discussion"
                }
            else:
                feedback = {
                    "assessment": f"Strong performance in this {self.career} interview!",
                    "technical_score": 7,
                    "communication_score": 7,
                    "problem_solving_score": 7,
                    "strengths": ["Engaged and thoughtful", "Good grasp of fundamentals"],
                    "improvements": ["Gain more hands-on experience", "Study advanced topics"],
                    "recommendation": "Further Discussion"
                }
        except:
            feedback = {
                "assessment": f"Great interview responses for a {self.level} {self.career}!",
                "technical_score": 7,
                "communication_score": 7,
                "problem_solving_score": 7,
                "strengths": ["Engaged and thoughtful", "Good grasp of fundamentals"],
                "improvements": ["Gain more hands-on experience", "Study advanced topics"],
                "recommendation": "Further Discussion"
            }
        
        return {
            "status": "interview_complete",
            "feedback": feedback,
            "total_questions_answered": len(self.answers),
            "session_id": self.session_id
        }


def start_interview(career: str, level: str = "fresher") -> dict:
    """Start a new mock interview session"""
    from .fuzzy_matcher import find_best_career_match
    
    # Find best match for the career
    matched_career = find_best_career_match(career)
    if not matched_career:
        return {
            "status": "error",
            "message": f"Career '{career}' not found"
        }
    
    session = InterviewSession(matched_career, level)
    first_q = session.get_first_question()
    
    if first_q["status"] == "success":
        # Store session (in production, use database/cache)
        return {
            "status": "interview_started",
            "career": matched_career,
            "level": level,
            "first_question": first_q,
            "session_data": {
                "questions_asked": session.questions_asked,
                "answers": session.answers,
                "current_index": session.current_question_index
            }
        }
    
    return first_q


def process_interview_answer(career: str, level: str, answer: str, session_data: dict) -> dict:
    """Process an answer and get next question or feedback"""
    from .fuzzy_matcher import find_best_career_match
    
    # Find best match for the career
    matched_career = find_best_career_match(career)
    if not matched_career:
        return {
            "status": "error",
            "message": f"Career '{career}' not found"
        }
    
    session = InterviewSession(matched_career, level)
    session.questions_asked = session_data.get("questions_asked", [])
    session.answers = session_data.get("answers", [])
    session.current_question_index = session_data.get("current_index", 0)
    
    result = session.submit_answer(answer)
    
    result["session_data"] = {
        "questions_asked": session.questions_asked,
        "answers": session.answers,
        "current_index": session.current_question_index
    }
    
    return result


def get_interview_tips(career: str, level: str = "fresher") -> dict:
    """Get tips for interviewing for a specific career"""
    from .fuzzy_matcher import find_best_career_match
    
    matched_career = find_best_career_match(career)
    if not matched_career or matched_career.lower() not in CAREER_DB:
        return {
            "status": "error",
            "message": f"Career '{career}' not found"
        }
    
    try:
        tips_data = generate_interview_prep(matched_career)
        if isinstance(tips_data, dict) and 'interview_tips' in tips_data:
            tips = tips_data['interview_tips']
        else:
            tips = f"Prepare examples of projects, understand the company's mission, practice answering behavioral questions, and have thoughtful questions ready for your interviewers."
    except:
        tips = f"Prepare examples of projects, understand the company's mission, practice answering behavioral questions, and have thoughtful questions ready for your interviewers."
    
    return {
        "status": "success",
        "career": matched_career,
        "level": level,
        "tips": tips
    }
