"""
O*NET Integration Module with NLP-powered Search
Provides O*NET data handling and intelligent semantic career search using TF-IDF
"""
import json
from .career_data import CAREER_DB
from .fuzzy_matcher import find_best_career_match
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# O*NET Sample Data with detailed descriptions
ONET_SAMPLE_DATA = {
    "data_scientist": {
        "name": "Data Scientist",
        "description": "Extract insights from complex datasets using machine learning and statistical analysis. Build ML models that drive business decisions. Blend mathematics, programming, and domain expertise to solve real-world problems.",
        "salary": {"entry": 85000, "mid": 130000, "senior": 180000, "lead": 240000},
        "job_outlook": "36% growth (2021-2031) | Much faster than average",
        "skills": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization", "Deep Learning", "Big Data", "Tableau"],
        "keywords": ["data analysis", "predictive modeling", "neural networks", "analytics", "big data"]
    },
    "devops_engineer": {
        "name": "DevOps Engineer",
        "description": "Bridge development and operations. Automate deployment pipelines, manage infrastructure, and improve system reliability. Use containerization and cloud technologies to scale applications efficiently.",
        "salary": {"entry": 85000, "mid": 125000, "senior": 170000, "lead": 220000},
        "job_outlook": "28% growth (2021-2031) | Much faster than average",
        "skills": ["Linux", "AWS", "Docker", "Kubernetes", "Jenkins", "Terraform", "CI/CD", "Bash/Python", "Monitoring"],
        "keywords": ["deployment", "infrastructure", "automation", "cloud", "containers"]
    },
    "business_analyst": {
        "name": "Business Analyst",
        "description": "Bridge business and technology. Analyze requirements, improve business processes, and drive business value from IT projects. Communicate between technical teams and stakeholders.",
        "salary": {"entry": 55000, "mid": 75000, "senior": 100000, "lead": 130000},
        "job_outlook": "14% growth (2021-2031) | Faster than average",
        "skills": ["SQL", "Excel", "Data Analysis", "Communication", "Process Mapping", "Power BI", "Requirements Analysis", "Business Acumen"],
        "keywords": ["requirements", "process improvement", "business logic", "analysis", "reporting"]
    },
    "solutions_architect": {
        "name": "Solutions Architect",
        "description": "Design enterprise-scale solutions that balance business needs with technical constraints. Lead high-impact initiatives and present technical solutions to stakeholders.",
        "salary": {"entry": 110000, "mid": 160000, "senior": 220000, "lead": 280000},
        "job_outlook": "13% growth | Steady and growing",
        "skills": ["System Design", "Cloud Architecture", "AWS", "Azure", "Communication", "Problem Solving", "Security", "Leadership"],
        "keywords": ["architecture", "enterprise", "scaling", "design patterns", "infrastructure planning"]
    },
    "mobile_developer": {
        "name": "Mobile Developer",
        "description": "Build engaging mobile applications for iOS, Android, or cross-platform environments. Create user experiences that millions use daily. Work with modern mobile frameworks and tools.",
        "salary": {"entry": 75000, "mid": 110000, "senior": 150000, "lead": 200000},
        "job_outlook": "22% growth | Faster than average",
        "skills": ["Swift", "Kotlin", "React Native", "Flutter", "Mobile UI/UX", "APIs", "Git", "Firebase", "Testing"],
        "keywords": ["mobile apps", "ios", "android", "user interface", "mobile experience"]
    }
}


def _create_career_search_corpus():
    """Create searchable text corpus for all careers using NLP"""
    corpus = {}
    all_careers = {**CAREER_DB, **ONET_SAMPLE_DATA}
    
    for career_name, career_data in all_careers.items():
        # Combine all relevant text fields
        text_parts = [
            career_name.replace("_", " "),
            career_data.get('description', ''),
            ' '.join(career_data.get('skills', [])),
            career_data.get('market', ''),
            career_data.get('future', ''),
            ' '.join(career_data.get('keywords', [])) if 'keywords' in career_data else '',
        ]
        corpus[career_name] = ' '.join(text_parts).lower()
    
    return corpus, all_careers


def search_onet_careers(keyword: str) -> dict:
    """Search careers using NLP-powered TF-IDF semantic search"""
    if not keyword or len(keyword.strip()) == 0:
        return {
            "status": "error",
            "message": "Please enter a search keyword",
            "total": 0,
            "results": []
        }
    
    corpus, all_careers = _create_career_search_corpus()
    
    if not corpus:
        return {
            "status": "error",
            "message": "No careers available",
            "total": 0,
            "results": []
        }
    
    try:
        # TF-IDF Vectorizer for semantic search
        vectorizer = TfidfVectorizer(
            analyzer='char',
            ngram_range=(2, 3),
            lowercase=True,
            stop_words='english'
        )
        
        career_names = list(corpus.keys())
        career_vectors = list(corpus.values())
        
        # Fit vectorizer on all career texts
        X = vectorizer.fit_transform(career_vectors)
        
        # Transform the search query
        query_vector = vectorizer.transform([keyword.lower()])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, X)[0]
        
        # Get indices of matches sorted by similarity
        top_indices = np.argsort(similarities)[::-1]
        
        results = []
        seen = set()
        
        for idx in top_indices:
            similarity = float(similarities[idx])
            if similarity > 0.05:  # Threshold for relevance
                career_name = career_names[idx]
                if career_name not in seen:
                    career_data = all_careers[career_name]
                    results.append({
                        "name": career_data.get("name", career_name.replace("_", " ").title()),
                        "description": career_data.get("description", "")[:200],
                        "skills": career_data.get("skills", [])[:4],
                        "salary_entry": career_data.get("salary", {}).get("entry", 0),
                        "job_outlook": career_data.get("job_outlook", ""),
                        "match_score": f"{similarity*100:.1f}%",
                        "similarity": similarity
                    })
                    seen.add(career_name)
        
        # Sort by similarity descending
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return {
            "status": "success",
            "keyword": keyword,
            "total": len(results),
            "results": results[:15]  # Limit to 15 results
        }
        
    except Exception as e:
        # Fallback to keyword-based search
        keyword_lower = keyword.lower()
        results = []
        seen = set()
        
        for career_name, career_data in all_careers.items():
            if career_name not in seen:
                # Check if keyword appears in name, description, or skills
                match_score = 0
                if keyword_lower in career_name.lower():
                    match_score = 100
                elif keyword_lower in career_data.get('description', '').lower():
                    match_score = 70
                else:
                    for skill in career_data.get('skills', []):
                        if keyword_lower in skill.lower():
                            match_score = 60
                            break
                
                if match_score > 0:
                    results.append({
                        "name": career_data.get("name", career_name.replace("_", " ").title()),
                        "description": career_data.get("description", "")[:200],
                        "skills": career_data.get("skills", [])[:4],
                        "salary_entry": career_data.get("salary", {}).get("entry", 0),
                        "match_score": f"{match_score}%"
                    })
                    seen.add(career_name)
        
        return {
            "status": "success",
            "keyword": keyword,
            "total": len(results),
            "results": results
        }


def get_onet_data() -> dict:
    """Get all O*NET sample data"""
    return {
        "status": "success",
        "total_careers": len(ONET_SAMPLE_DATA) + len(CAREER_DB),
        "sample_careers": list(ONET_SAMPLE_DATA.keys()),
        "data": ONET_SAMPLE_DATA
    }


def get_career_statistics(career_name: str) -> dict:
    """Get labor statistics for a specific career"""
    all_careers = {**CAREER_DB, **ONET_SAMPLE_DATA}
    
    # Find best match using fuzzy matching
    matched_career = find_best_career_match(career_name)
    
    if matched_career and matched_career in all_careers:
        career_data = all_careers[matched_career]
        return {
            "status": "success",
            "career": matched_career.replace("_", " ").title(),
            "job_outlook": career_data.get("job_outlook", "Data not available"),
            "salary": career_data.get("salary", {}),
            "skills": career_data.get("skills", []),
            "description": career_data.get("description", ""),
            "keywords": career_data.get("keywords", [])
        }
    
    return {
        "status": "error",
        "message": f"Career '{career_name}' not found"
    }


def download_onet_data() -> dict:
    """Get information about downloading full O*NET data"""
    return {
        "status": "success",
        "message": "O*NET data integration information",
        "currently_available": len(ONET_SAMPLE_DATA) + len(CAREER_DB),
        "total_onet_careers": 900,
        "download_instructions": [
            "Visit https://www.onetcenter.org/database.html",
            "Download the O*NET database in JSON or CSV format",
            "Extract the data files",
            "Use onet_importer.py to integrate into career database"
        ],
        "features": [
            "Complete job descriptions and tasks",
            "Detailed skill requirements and proficiencies",
            "Work activities and work context",
            "Required education and training",
            "Wage and employment statistics",
            "Industry and occupation codes"
        ]
    }
