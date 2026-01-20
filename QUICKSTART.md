# 🚀 Quick Start Guide

## Installation (2 minutes)

### 1. Install Python Packages
```bash
cd ai-career-counselor
pip install -r requirements.txt
```

### 2. Run the App
```bash
python backend/app.py
```

### 3. Open Browser
```
http://127.0.0.1:5000
```

**That's it!** The app is now running with all ML/AI features enabled. ✅

---

## Using the App

### 🔍 Tab 1: Career Search
**Find careers and get detailed guidance**

1. Type a career name (typos are OK!)
   - "data analist" → auto-corrects to "data analyst"
   - "sofware engineer" → works fine
   
2. Select your level
   - Student (building foundations)
   - Fresher (first job hunter)
   - Professional (career advancement)

3. Click "Get My Career Roadmap"

You'll see:
- Full roadmap adapted to your level
- All required skills
- Learning resources
- Market insights & salary info
- Future outlook
- Similar careers you might like

---

### 💡 Tab 2: Find by Skills
**Discover careers based on skills you have**

1. Enter your skills (comma-separated)
   ```
   Python, SQL, Excel, Communication
   ```

2. Click "Find Matching Careers"

You'll see:
- Ranked list of matching careers
- Match percentage for each
- Your matching skills (highlighted)
- Skills you still need to learn

**Example output:**
```
1. Data Analyst (87% match)
   ✓ Matching: Python, SQL, Excel
   Need to learn: 4 more skills

2. Business Analyst (72% match)
   ✓ Matching: Excel, Communication
   Need to learn: 6 more skills
```

---

### 📊 Tab 3: Skill Gap Analysis
**Understand what you need to learn for a target career**

1. Enter target career
   ```
   Software Engineer
   ```

2. Enter your current skills (optional)
   ```
   Python, Git
   ```

3. Click "Analyze My Skill Gap"

You'll see:
- Progress bar (% skills you have)
- ✅ Skills you already have (green)
- ❌ Skills to learn (red)
- Total skills needed

**Example:**
```
Software Engineer - 25% Complete

✅ You Have (2/8 skills):
   Python, Git

❌ You Need to Learn:
   Java, DSA, System Design, Databases, ...
```

---

## 🤖 Features Explained

### ✨ Smart Typo Handling
- Type "dta analist" → matches "data analyst"
- Type "macine lerning" → finds "machine learning engineer"
- Shows confidence score

### 🎯 Skill-Based Matching
- Real ML algorithm (TF-IDF + Cosine Similarity)
- Understands skill variations
- Ranks careers by best match

### 📈 Skill Progress Tracking
- Visual progress bar
- Exact skill gaps identified
- Learning path suggested

### 🤖 AI Features (Optional)
- Personalized guidance from GPT (if enabled)
- Interview preparation tips
- Career fit analysis

---

## 🔧 Optional: Enable AI Features

### Get an OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Sign up/login
3. Create new secret key
4. Copy the key (looks like: `sk-...`)

### Configure Your Key
```bash
# Create .env file in project root
cp .env.example .env

# Edit .env and add your key:
# OPENAI_API_KEY=sk-your-key-here
```

### Restart App
```bash
# Press Ctrl+C to stop
# Then run again:
python backend/app.py
```

### Verify AI is Active
- Check the status bar at top of page
- Should show: "✅ AI Features Active (GPT-powered guidance available)"
- Now you'll get personalized guidance from AI!

---

## 📝 Available Careers

Currently supports these 8 careers:

1. **Data Analyst**
   - Skills: SQL, Python, Excel, Power BI, Statistics
   - Market: High demand, $65k-$85k

2. **Software Engineer**
   - Skills: Java, Python, JavaScript, DSA, System Design
   - Market: Very high demand, $90k-$150k+

3. **Web Developer**
   - Skills: HTML, CSS, JavaScript, React, Node.js
   - Market: High demand, $70k-$100k

4. **Machine Learning Engineer**
   - Skills: Python, TensorFlow, PyTorch, Math, Statistics
   - Market: Very high demand, $120k-$160k+

5. **Product Manager**
   - Skills: Communication, Strategy, User Research, Data
   - Market: High demand, $100k-$150k

6. **UX Designer**
   - Skills: Figma, User Research, Design, Communication
   - Market: High demand, $80k-$120k

7. **Cybersecurity Analyst**
   - Skills: Networking, Ethical Hacking, Encryption, Python
   - Market: Extreme shortage, $85k-$130k+

8. **Cloud Architect**
   - Skills: AWS, Azure, Docker, Kubernetes, Terraform
   - Market: Very high demand, $120k-$170k+

---

## 💻 Example Workflows

### Scenario 1: Career Discovery
```
"I'm a student with Python skills. What can I do?"

1. Go to Tab 2: Find by Skills
2. Enter: "Python, Problem Solving"
3. See: Top careers = Data Analyst, Software Engineer, ML Engineer
4. Click "Data Analyst"
5. Get full roadmap and resources
```

### Scenario 2: Career Transition
```
"I want to become a Web Developer. I know Python and Git. What's missing?"

1. Go to Tab 3: Skill Gap Analysis
2. Career: "web developer"
3. Your skills: "Python, Git"
4. See: 25% complete, need: JavaScript, React, Node.js, HTML, CSS
5. Get learning path
```

### Scenario 3: Overcoming Typo
```
"I want to be a 'dta enginer'"

1. Go to Tab 1: Career Search
2. Type: "dta enginer"
3. System auto-corrects to closest match
4. Shows confidence: 78%
5. Get full guidance
```

---

## 🐛 Troubleshooting

### App won't start
```
Error: "Address already in use"
Solution: Kill existing Flask process
  - powershell: Get-Process python | Stop-Process
  - Try different port: python -m flask run --port 5001
```

### "Cannot connect to server"
```
Solution: Make sure Flask is running
  - Check terminal shows: "Running on http://127.0.0.1:5000"
  - Try refreshing browser
```

### No results for my career
```
Solution: Your career might not be in database
  - Check "Available Careers" list
  - Try similar career name
  - Or use Tab 2 to search by skills
```

### AI features not showing
```
Solution: OPENAI_API_KEY not set (this is OK!)
  - App works perfectly without it
  - Set API key to enable AI features
  - See "Optional: Enable AI Features" section above
```

---

## 📚 API Reference

If you want to integrate this API:

### Career Search
```
POST /career
Body: {
  "career": "data analyst",
  "level": "fresher"
}
Returns: Full career guidance with AI features
```

### Recommend by Skills
```
POST /recommend
Body: {
  "skills": ["Python", "SQL", "Excel"]
}
Returns: Ranked list of matching careers
```

### Skill Gap
```
POST /skill-gap
Body: {
  "career": "software engineer",
  "skills": ["Python", "Git"]
}
Returns: Detailed skill gap analysis
```

### AI Status
```
GET /ai-status
Returns: Status of all AI features
```

---

## 🎓 Learning More

**Curious about the technology?** Check out:
- `README.md` - Full feature documentation
- `ARCHITECTURE.md` - Technical architecture & algorithms
- `IMPLEMENTATION.md` - Implementation details

---

## 🎉 You're All Set!

Start exploring careers now! The AI Career Counselor is ready to help you.

**Questions?** Check the README or docs folder.
