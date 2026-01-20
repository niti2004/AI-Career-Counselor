import os
import json
from pathlib import Path

# Try to load a generated O*NET-based CAREER DB if present; otherwise fall back
# to a small built-in sample DB. The importer script `backend/onet_importer.py`
# can create `backend/CAREER_DB_onet.json` from an O*NET occupations CSV.
_ONET_JSON = Path(__file__).parent / 'CAREER_DB_onet.json'

if _ONET_JSON.exists():
    try:
        with open(_ONET_JSON, 'r', encoding='utf-8') as _f:
            CAREER_DB = json.load(_f)
        print(f"Loaded O*NET career DB with {len(CAREER_DB)} entries from {_ONET_JSON}")
    except Exception:
        CAREER_DB = {}
else:
    CAREER_DB = {
    "data analyst": {
        "roadmap": [
            "Learn Excel & SQL",
            "Python for data analysis",
            "Statistics & probability",
            "Build portfolio projects",
            "Pursue internships",
            "Learn visualization tools (Power BI, Tableau)"
        ],
        "skills": ["SQL", "Python", "Excel", "Power BI", "Statistics", "Data Visualization", "Problem Solving"],
        "resources": [{"name": "Kaggle", "url": "https://www.kaggle.com"}, {"name": "Coursera", "url": "https://www.coursera.org"}, {"name": "DataCamp", "url": "https://www.datacamp.com"}, {"name": "YouTube - Alex The Analyst", "url": "https://www.youtube.com/@alextheanalyst"}, {"name": "Mode Analytics SQL Tutorial", "url": "https://mode.com/sql-tutorial/"}],
        "market": "High demand across finance, healthcare, tech, and e-commerce. Average salary: $65k-$85k",
        "future": "Strong growth with AI integration and increasing data-driven decision making",
        "salary": {"entry": 55000, "mid": 75000, "senior": 95000, "lead": 120000},
        "growth": {"fresher": "Junior Data Analyst (0-2 yrs)", "professional": "Senior Data Analyst (2-5 yrs)", "expert": "Analytics Manager/Lead (5+ yrs)"},
        "job_outlook": "22% growth (2021-2031) | Faster than average",
        "description": "Transform raw data into actionable insights. Work with databases, create dashboards, and drive data-informed decisions. Perfect for analytical minds who love problem-solving.",
        "work_environment": "Mostly remote/hybrid. Fast-paced, collaborative teams. High impact on business decisions.",
        "typical_day": "- Analyze data queries and trends\n- Create dashboards for stakeholders\n- Prepare reports and presentations\n- Collaborate with engineers and managers"
    },
    "software engineer": {
        "roadmap": [
            "Master fundamentals (DSA, OOP)",
            "Learn a programming language (Python, JavaScript, Java)",
            "Build projects on GitHub",
            "System design basics",
            "Contribute to open source",
            "Interview prep & apply to companies"
        ],
        "skills": ["Java", "Python", "JavaScript", "DSA", "System Design", "Git", "Database Design", "OOP"],
        "resources": [{"name": "LeetCode", "url": "https://leetcode.com"}, {"name": "GeeksforGeeks", "url": "https://www.geeksforgeeks.org"}, {"name": "Educative", "url": "https://www.educative.io"}, {"name": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer"}, {"name": "GitHub", "url": "https://github.com"}],
        "market": "Very high demand. Average salary: $90k-$150k+. Remote opportunities abundant",
        "future": "Sustainable growth with AI/ML, cloud computing, and quantum computing emerging",
        "salary": {"entry": 80000, "mid": 120000, "senior": 160000, "lead": 200000},
        "growth": {"fresher": "Junior Developer (0-2 yrs)", "professional": "Senior Developer (2-5 yrs)", "expert": "Lead/Architect (5+ yrs)"},
        "job_outlook": "15% growth (2021-2031) | Faster than average",
        "description": "Build the digital world. Write clean, scalable code that powers apps, websites, and systems. Collaborate with teams and impact millions of users. Ideal for logical thinkers who love coding challenges.",
        "work_environment": "Highly remote-friendly. Collaborative, innovative teams. Fast-paced with continuous learning. Competitive perks and benefits.",
        "typical_day": "- Write and review code\n- Debug complex issues\n- Design system architecture\n- Attend team standups and code reviews"
    },
    "web developer": {
        "roadmap": [
            "HTML, CSS, JavaScript fundamentals",
            "Frontend framework (React, Vue, Angular)",
            "Backend basics (Node.js/Python/Java)",
            "Databases & APIs",
            "Build full-stack projects",
            "Learn DevOps basics (Docker, deployment)"
        ],
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js", "MongoDB", "Git", "REST APIs", "Responsive Design"],
        "resources": [{"name": "freeCodeCamp", "url": "https://www.freecodecamp.org"}, {"name": "Udemy", "url": "https://www.udemy.com"}, {"name": "MDN Web Docs", "url": "https://developer.mozilla.org"}, {"name": "Frontend Masters", "url": "https://frontendmasters.com"}, {"name": "Scrimba", "url": "https://scrimba.com"}],
        "market": "High demand across all industries. Average salary: $70k-$100k. Flexible remote work",
        "future": "Continuous evolution with AI-assisted development and no-code platforms emerging",
        "salary": {"entry": 60000, "mid": 85000, "senior": 120000, "lead": 160000},
        "growth": {"fresher": "Junior Web Developer (0-2 yrs)", "professional": "Full-Stack Developer (2-5 yrs)", "expert": "Tech Lead/Architect (5+ yrs)"},
        "job_outlook": "23% growth (2021-2031) | Much faster than average",
        "description": "Create beautiful, interactive websites and applications. Bridge design and backend. See your code live instantly. Perfect for creative problem-solvers who want immediate visual feedback.",
        "work_environment": "Very remote-friendly. Startups to large tech companies. Flexible hours, creative autonomy. Strong community and learning culture.",
        "typical_day": "- Develop frontend components\n- Fix bugs and optimize performance\n- Implement API integrations\n- Collaborate with designers and backend devs"
    },
    "machine learning engineer": {
        "roadmap": [
            "Strong Python and Math fundamentals",
            "Machine Learning algorithms & theory",
            "Deep Learning & Neural Networks",
            "Practical ML projects (Kaggle competitions)",
            "Learn frameworks (TensorFlow, PyTorch)",
            "Big Data & deployment (Docker, Kubernetes)"
        ],
        "skills": ["Python", "TensorFlow", "PyTorch", "Mathematics", "Statistics", "SQL", "Big Data", "Deployment"],
        "resources": [{"name": "Andrew Ng ML Course", "url": "https://www.coursera.org/learn/machine-learning"}, {"name": "Fast.ai", "url": "https://www.fast.ai"}, {"name": "Stanford CS231N", "url": "http://cs231n.stanford.edu"}, {"name": "Kaggle", "url": "https://www.kaggle.com"}, {"name": "Papers With Code", "url": "https://paperswithcode.com"}],
        "market": "Very high demand in tech, finance, healthcare. Average salary: $120k-$160k+",
        "future": "Explosive growth with AI revolution. Emerging fields: LLMs, Transformers, Multimodal AI",
        "salary": {"entry": 100000, "mid": 150000, "senior": 200000, "lead": 250000},
        "growth": {"fresher": "Junior ML Engineer (0-2 yrs)", "professional": "Senior ML Engineer (2-5 yrs)", "expert": "Principal/Research Lead (5+ yrs)"},
        "job_outlook": "36% growth (2021-2031) | Much faster than average",
        "description": "Build intelligent systems that learn and improve. Work on cutting-edge AI, computer vision, NLP. High impact on products and society. Best for mathematically-minded engineers.",
        "work_environment": "Highly competitive, innovative teams. Often in well-funded tech/finance companies. Research-friendly with time for experimentation.",
        "typical_day": "- Develop ML models and algorithms\n- Train and evaluate models\n- Optimize performance and efficiency\n- Publish research and present findings"
    },
    "product manager": {
        "roadmap": [
            "Understand user research & market analysis",
            "Learn product strategy & roadmapping",
            "Develop communication & leadership skills",
            "Build a portfolio of product case studies",
            "Gain technical understanding (not coding required)",
            "Pursue internships or APM programs"
        ],
        "skills": ["Communication", "Analytical Thinking", "Leadership", "User Research", "Data Analysis", "Technical Acumen"],
        "resources": [{"name": "Reforge", "url": "https://www.reforge.com"}, {"name": "Product School", "url": "https://www.productschool.com"}, {"name": "Lenny's Product Podcast", "url": "https://www.lennyspodcast.com"}, {"name": "Inspired by Marty Cagan", "url": "https://www.svpg.com/books/inspired-how-to-create-products-customers-love/"}, {"name": "Figma/Miro", "url": "https://www.figma.com"}],
        "market": "High demand in tech startups & large companies. Average salary: $100k-$150k",
        "future": "Growing importance with AI integration in product development",
        "salary": {"entry": 90000, "mid": 130000, "senior": 180000, "lead": 250000},
        "growth": {"fresher": "Associate PM/APM (0-2 yrs)", "professional": "Senior Product Manager (2-5 yrs)", "expert": "Director/VP Product (5+ yrs)"},
        "job_outlook": "18% growth (2021-2031) | Faster than average",
        "description": "Shape products that millions use. Own strategy, roadmap, and vision. Lead cross-functional teams. Perfect for strategic thinkers who love influencing decisions.",
        "work_environment": "High-visibility roles in startups and tech giants. Collaborative with engineers, designers, marketing. Strategic and fast-paced.",
        "typical_day": "- Conduct user research and analyze metrics\n- Plan product roadmap and features\n- Lead cross-functional meetings\n- Communicate with stakeholders and executives"
    },
    "ux designer": {
        "roadmap": [
            "Learn design fundamentals (color, typography, layout)",
            "Master Figma & design tools",
            "Understand user psychology & research",
            "Build design portfolio (5-8 projects)",
            "Learn interaction & motion design",
            "Develop communication with developers"
        ],
        "skills": ["Figma", "User Research", "Prototyping", "Wireframing", "Visual Design", "Communication", "CSS Knowledge"],
        "resources": [{"name": "Design+Code", "url": "https://www.designcode.io"}, {"name": "Interaction Design Foundation", "url": "https://www.interaction-design.org"}, {"name": "Figma tutorials", "url": "https://www.figma.com"}, {"name": "Dribbble", "url": "https://dribbble.com"}, {"name": "User Testing", "url": "https://www.usertesting.com"}],
        "market": "High demand across tech, healthcare, finance. Average salary: $80k-$120k",
        "future": "Growing focus on accessibility, ethical design, and AI-assisted design tools",
        "salary": {"entry": 65000, "mid": 95000, "senior": 135000, "lead": 180000},
        "growth": {"fresher": "Junior UX Designer (0-2 yrs)", "professional": "Senior UX Designer (2-5 yrs)", "expert": "Design Manager/Lead (5+ yrs)"},
        "job_outlook": "20% growth (2021-2031) | Faster than average",
        "description": "Create beautiful, intuitive experiences. Research users, design solutions, test ideas. Balance aesthetics with functionality. Ideal for creative problem-solvers who empathize with users.",
        "work_environment": "Increasingly remote-friendly. Collaborative with product, engineering, marketing. Emphasis on user feedback and iteration.",
        "typical_day": "- Conduct user interviews and research\n- Create wireframes and prototypes\n- Design visual interfaces\n- Test and iterate based on feedback"
    },
    "cybersecurity analyst": {
        "roadmap": [
            "Network & system fundamentals",
            "Learn ethical hacking (CEH path)",
            "Understand security protocols & encryption",
            "Get certified (Security+, CEH, CISSP)",
            "Hands-on labs & CTF challenges",
            "Stay updated on threat landscapes"
        ],
        "skills": ["Networking", "Linux/Windows", "Encryption", "Penetration Testing", "Risk Analysis", "Python", "Problem Solving"],
        "resources": [{"name": "TryHackMe", "url": "https://tryhackme.com"}, {"name": "HackTheBox", "url": "https://www.hackthebox.com"}, {"name": "Professor Messer", "url": "https://www.professormesser.com"}, {"name": "Cybrary", "url": "https://www.cybrary.it"}, {"name": "PortSwigger Web Security Academy", "url": "https://portswigger.net/web-security"}],
        "market": "Extreme shortage of talent. Average salary: $85k-$130k+. High job security",
        "future": "Critical demand as cyber threats increase. Growth in AI-assisted threat detection",
        "salary": {"entry": 75000, "mid": 110000, "senior": 160000, "lead": 210000},
        "growth": {"fresher": "Security Analyst (0-2 yrs)", "professional": "Senior Security Analyst (2-5 yrs)", "expert": "Security Manager/Director (5+ yrs)"},
        "job_outlook": "35% growth (2021-2031) | Much faster than average",
        "description": "Protect organizations from cyber threats. Hunt for vulnerabilities, respond to incidents. High stakes, always learning. Perfect for detail-oriented, curious minds.",
        "work_environment": "Critical infrastructure focus, 24/7 operations. Startup security teams to Fortune 500 security centers. On-call rotations common.",
        "typical_day": "- Monitor security alerts and logs\n- Conduct vulnerability assessments\n- Investigate security incidents\n- Document threats and recommendations"
    },
    "cloud architect": {
        "roadmap": [
            "Learn cloud platforms (AWS, Azure, GCP)",
            "Understand infrastructure & DevOps",
            "Get cloud certifications (AWS Solutions Architect)",
            "Design scalable & secure systems",
            "Learn Infrastructure as Code (Terraform)",
            "Develop cost optimization skills"
        ],
        "skills": ["AWS", "Azure", "Docker", "Kubernetes", "Terraform", "Linux", "Database Design", "Security"],
        "resources": [{"name": "A Cloud Guru", "url": "https://acloudguru.com"}, {"name": "Linux Academy", "url": "https://linuxacademy.com"}, {"name": "AWS Documentation", "url": "https://docs.aws.amazon.com"}, {"name": "Terraform Registry", "url": "https://registry.terraform.io"}, {"name": "CloudAcademy", "url": "https://cloudacademy.com"}],
        "market": "Very high demand. Average salary: $120k-$170k+. Excellent remote opportunities",
        "future": "Explosive growth with cloud-native adoption and multi-cloud strategies",
        "salary": {"entry": 95000, "mid": 140000, "senior": 190000, "lead": 240000},
        "growth": {"fresher": "Junior Cloud Engineer (0-2 yrs)", "professional": "Senior Cloud Architect (2-5 yrs)", "expert": "Principal Architect (5+ yrs)"},
        "job_outlook": "32% growth (2021-2031) | Much faster than average",
        "description": "Design and manage cloud infrastructure for scale. Build resilient, cost-effective systems. Bridge infrastructure and development. Ideal for systems thinkers who love architecture.",
        "work_environment": "Highly remote-friendly. Strategic influence in tech companies. Focus on efficiency, security, and scalability.",
        "typical_day": "- Design cloud architectures\n- Optimize costs and performance\n- Lead infrastructure initiatives\n- Mentor cloud engineers"
    }

}

CAREER_LEVELS = {
    "student": {
        "focus": "Build foundations and internship opportunities",
        "tips": ["Focus on learning fundamentals", "Pursue internships or co-ops", "Build projects for portfolio"]
    },
    "fresher": {
        "focus": "Land first job and prove capabilities",
        "tips": ["Build strong portfolio", "Apply to entry-level positions", "Network actively", "Consider contract roles"]
    },
    "professional": {
        "focus": "Advance career and develop expertise",
        "tips": ["Seek senior roles", "Develop leadership skills", "Consider specialization", "Build mentor relationships"]
    }
}
