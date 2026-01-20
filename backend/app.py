from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

from backend.career_ai import career_guidance, recommend_by_skills, analyze_skill_gap, get_ai_features
from backend.career_comparison import compare_careers, get_salary_comparison, get_skill_comparison, get_growth_comparison, get_career_fit_score, get_career_details
from backend.onet_integration import get_onet_data, search_onet_careers, download_onet_data, get_career_statistics

@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, '..', 'frontend'), 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(os.path.join(app.root_path, '..', 'frontend'), path)

@app.route('/career', methods=['POST'])
def career():
    """Get career guidance with fuzzy matching and AI enhancements."""
    data = request.json
    career = data.get("career")
    level = data.get("level", "fresher")

    response = career_guidance(career, level)
    return jsonify(response)

@app.route('/recommend', methods=['POST'])
def recommend():
    """Recommend careers based on user's skills."""
    data = request.json
    skills = data.get("skills", [])
    
    if not skills or len(skills) == 0:
        return jsonify({
            "status": "error",
            "message": "Please provide at least one skill"
        }), 400
    
    response = recommend_by_skills(skills)
    return jsonify(response)

@app.route('/skill-gap', methods=['POST'])
def skill_gap():
    """Analyze skill gap for a target career."""
    data = request.json
    career = data.get("career")
    skills = data.get("skills", [])
    
    if not career:
        return jsonify({
            "status": "error",
            "message": "Career name is required"
        }), 400
    
    response = analyze_skill_gap(career, skills)
    return jsonify(response)

@app.route('/ai-status', methods=['GET'])
def ai_status():
    """Check AI features status."""
    response = get_ai_features()
    return jsonify(response)

# ============ CAREER COMPARISON ENDPOINTS ============

@app.route('/compare', methods=['POST'])
def compare():
    """Compare 2-3 careers side by side."""
    data = request.json
    careers = data.get("careers", [])
    
    if not careers or len(careers) == 0:
        return jsonify({
            "status": "error",
            "message": "Please provide at least 2 careers to compare"
        }), 400
    
    response = compare_careers(careers)
    return jsonify(response)

@app.route('/salary-comparison', methods=['POST'])
def salary_comparison():
    """Compare salary across careers."""
    data = request.json
    careers = data.get("careers", [])
    
    response = get_salary_comparison(careers)
    return jsonify(response)

@app.route('/skill-comparison', methods=['POST'])
def skill_comparison():
    """Compare skills required across careers."""
    data = request.json
    careers = data.get("careers", [])
    
    response = get_skill_comparison(careers)
    return jsonify(response)

@app.route('/growth-comparison', methods=['POST'])
def growth_comparison():
    """Compare career growth paths."""
    data = request.json
    careers = data.get("careers", [])
    
    response = get_growth_comparison(careers)
    return jsonify(response)

@app.route('/career-fit', methods=['POST'])
def career_fit():
    """Get career fit scores based on user skills."""
    data = request.json
    careers = data.get("careers", [])
    user_skills = data.get("skills", [])
    
    response = get_career_fit_score(careers, user_skills)
    return jsonify(response)

@app.route('/career-details/<career_name>', methods=['GET'])
def career_details(career_name):
    """Get comprehensive career details."""
    response = get_career_details(career_name)
    return jsonify(response)

# ============ O*NET INTEGRATION ENDPOINTS ============

@app.route('/onet/search', methods=['POST'])
def onet_search():
    """Search O*NET careers by keyword."""
    data = request.json
    keyword = data.get("keyword", "")
    
    response = search_onet_careers(keyword)
    return jsonify(response)

@app.route('/onet/data', methods=['GET'])
def onet_data():
    """Get O*NET career data."""
    response = get_onet_data()
    return jsonify(response)

@app.route('/onet/statistics/<career_name>', methods=['GET'])
def onet_statistics(career_name):
    """Get labor statistics for a career."""
    response = get_career_statistics(career_name)
    return jsonify(response)

@app.route('/onet/download-info', methods=['GET'])
def onet_download_info():
    """Get O*NET download and integration information."""
    response = download_onet_data()
    return jsonify(response)

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=port, debug=debug)
