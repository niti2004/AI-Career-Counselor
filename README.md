# 🚀 AI Career Counselor - Advanced ML/AI Version

An intelligent career guidance system powered by **real machine learning and AI features**. This is not just a lookup tool—it actually analyzes, recommends, and adapts to user input.

## 🎯 What's New: Real AI Features

### 1. **Fuzzy String Matching** 🔍
- **What it does**: Handles typos and variations in career names
- **Example**: Type "data analist" → automatically matches "data analyst"
- **Technology**: Uses Levenshtein distance algorithm
- **Confidence score**: Shows how confident the match is

### 2. **Skill-Based Career Recommendation** 💡
- **What it does**: Analyzes your skills and recommends matching careers
- **Example**: "Python, SQL, Excel" → Recommends Data Analyst (87% match)
- **Technology**: TF-IDF vectorization + cosine similarity
- **How it works**:
  - Vectorizes each skill
  - Compares user skills to career requirements
  - Ranks careers by match percentage

### 3. **Skill Gap Analysis** 📊
- **What it does**: Identifies exactly which skills you need to learn
- **Shows**:
  - Progress bar (% of skills you already have)
  - Skills you have (green tags)
  - Skills to learn (red tags)
  - Detailed analysis

### 4. **Career Similarity Detection** 🔗
- **What it does**: Finds similar careers based on skill overlap
- **Example**: For "Data Analyst", suggests "Business Analyst" and "Data Scientist"
- **Technology**: Jaccard similarity on skill sets

### 5. **OpenAI GPT Integration** 🤖 (Optional)
- **What it does**: Generates personalized guidance using GPT
- **Features**:
  - Personalized roadmap based on your level
  - Interview preparation guides
  - Career fit analysis
- **How to enable**: Set `OPENAI_API_KEY` environment variable

## 📋 Features Breakdown

| Feature | Type | Status |
|---------|------|--------|
| Career Search with fuzzy matching | ML (Levenshtein) | ✅ Active |
| Skill-based recommendations | ML (TF-IDF + Similarity) | ✅ Active |
| Skill gap analysis | ML (Vector matching) | ✅ Active |
| Similar career detection | ML (Jaccard similarity) | ✅ Active |
| Personalized guidance (GPT) | AI/LLM | ⚠️ Optional |
| Input normalization | NLP | ✅ Active |

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
# Start Flask development server
python backend/app.py

# Open browser to http://127.0.0.1:5000
```

### Optional: Enable AI Features (GPT)

```bash
# Create .env file
cp .env.example .env

# Add your OpenAI API key
# OPENAI_API_KEY=sk-...

# Restart the app
```

## 💻 API Endpoints

### 1. Career Guidance (with AI)
**POST** `/career`
```json
{
  "career": "data analyst",
  "level": "fresher"
}
```

**Response includes**:
- Basic career info
- Fuzzy match confidence
- Similar careers
- AI-generated guidance (if API enabled)

### 2. Recommend Careers by Skills
**POST** `/recommend`
```json
{
  "skills": ["Python", "SQL", "Excel", "Communication"]
}
```

**Response**:
```json
{
  "recommendations": [
    {
      "career": "Data Analyst",
      "match_score": "87.5%",
      "matching_skills": ["Python", "SQL", "Excel"],
      "skills_to_learn": 4
    }
  ]
}
```

### 3. Skill Gap Analysis
**POST** `/skill-gap`
```json
{
  "career": "software engineer",
  "skills": ["Python", "Git"]
}
```

**Response**:
```json
{
  "career": "Software Engineer",
  "current_skills": 2,
  "total_skills": 8,
  "skill_match_percentage": 25,
  "matching_skills": ["Python", "Git"],
  "missing_skills": ["Java", "DSA", "System Design", ...]
}
```

### 4. AI Status
**GET** `/ai-status`

**Response**:
```json
{
  "features": {
    "fuzzy_matching": true,
    "skill_recommendation": true,
    "skill_gap_analysis": true,
    "personalized_guidance": {
      "ai_available": false,
      "model": "gpt-3.5-turbo",
      "message": "AI features disabled (set OPENAI_API_KEY environment variable)"
    }
  }
}
```

## 🎯 Three Main Tabs

### Tab 1: 🔍 Career Search
- Traditional career lookup
- Fuzzy matching for typos
- Level-based personalization
- Shows similar careers

### Tab 2: 💡 Find by Skills
- Enter your skills
- Get ranked career recommendations
- See match percentages
- Learn what else you need

### Tab 3: 📊 Skill Gap Analysis
- Target a career
- Enter your current skills
- Get visual progress
- See exact skills to learn

## 🤖 ML/AI Technologies Used

### Machine Learning
- **Fuzzy Matching**: `fuzzywuzzy` (Levenshtein distance)
- **Text Vectorization**: `sklearn.TfidfVectorizer`
- **Similarity Metrics**: Cosine similarity, Jaccard similarity
- **Recommendation Engine**: Content-based filtering

### AI/LLM
- **OpenAI GPT**: Optional integration for personalized guidance
- **Prompt Engineering**: Specialized prompts for career counseling

### NLP
- Text normalization
- Tokenization
- Similarity scoring

## 📊 Example Workflows

### Scenario 1: User with typo
```
User types: "dta analist"
↓
Fuzzy matcher finds: "data analyst" (78% confidence)
↓
Returns full career guidance with note: "Did you mean 'Data Analyst'? (78% match)"
```

### Scenario 2: User unsure about career
```
User enters skills: Python, SQL, Excel, Statistics
↓
Skill recommender analyzes
↓
Returns top careers:
  1. Data Analyst (89%)
  2. Business Analyst (72%)
  3. Data Scientist (68%)
↓
User clicks on "Data Analyst"
↓
Jumps to Career Search tab with pre-filled career name
```

### Scenario 3: Career transition
```
User wants: Software Engineer
User has: Python, Communication, Leadership
↓
Skill gap analysis shows:
  ✅ Matching: Python
  ❌ Missing: Java, DSA, System Design, Git, etc.
↓
Shows specific learning path with 37% completion
```

## 🔧 Configuration

### Environment Variables

```bash
# .env file
OPENAI_API_KEY=sk-your-key-here    # Optional: Enable AI features
OPENAI_MODEL=gpt-3.5-turbo          # Optional: Change model
```

### Adding More Careers

Edit `backend/career_data.py`:

```python
CAREER_DB = {
    "your_career": {
        "roadmap": [...],
        "skills": [...],
        "resources": [...],
        "market": "...",
        "future": "..."
    }
}
```

## 📦 Requirements

```
flask
flask-cors
fuzzywuzzy
python-Levenshtein
scikit-learn
openai (optional)
python-dotenv
```

## 🎓 What You Can Learn

This project demonstrates:

1. **ML Fundamentals**
   - String similarity algorithms
   - Vector-based similarity
   - Content-based recommendations

2. **Backend Development**
   - Flask REST APIs
   - API design with multiple endpoints
   - Error handling

3. **Frontend Development**
   - Tab-based UI
   - Real-time form validation
   - Responsive design

4. **AI Integration**
   - LLM API integration
   - Prompt engineering
   - Graceful fallbacks

5. **Full-Stack Architecture**
   - Client-server communication
   - Data processing pipeline
   - UI/UX for AI features

## 🚀 Future Enhancements

- [ ] User authentication and profiles
- [ ] Save favorite careers
- [ ] Career comparison tool
- [ ] Progress tracking
- [ ] Community reviews
- [ ] Job market data integration
- [ ] Resume builder
- [ ] Interview simulator with AI feedback

## 📝 License

MIT License - Feel free to fork and modify!

## 🎯 Use This For

- **Resume Projects**: Show real ML/AI implementation
- **Portfolio**: Demonstrate full-stack skills
- **Learning**: Understand ML algorithms
- **Helping Others**: Actual career guidance tool
- **Interviews**: Great talking point about AI projects

---

**Made with ❤️ using Python, ML, and AI**
