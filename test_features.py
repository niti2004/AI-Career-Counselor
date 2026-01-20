#!/usr/bin/env python
"""
Quick test script for all AI Career Counselor features
Run: python test_features.py
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_feature(name, endpoint, method="GET", data=None):
    """Test a single endpoint"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {name}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        else:
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS")
            print(f"Response: {json.dumps(result, indent=2)[:500]}")
            return True
        else:
            print(f"❌ FAILED (Status: {response.status_code})")
            print(f"Response: {response.text[:300]}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    print("\n🚀 AI Career Counselor - Feature Test Suite")
    print("=" * 60)
    
    tests = [
        # Original features
        ("Career Search", "/career", "POST", {"career": "Data Analyst", "level": "fresher"}),
        ("Skill Recommendations", "/recommend", "POST", {"skills": ["Python", "SQL", "Excel"]}),
        ("Skill Gap Analysis", "/skill-gap", "POST", {"career": "Software Engineer", "skills": ["Python"]}),
        ("AI Status", "/ai-status", "GET", None),
        
        # New comparison features
        ("Compare Careers", "/compare", "POST", {"careers": ["Data Analyst", "Software Engineer"]}),
        ("Salary Comparison", "/salary-comparison", "POST", {"careers": ["Data Analyst", "Web Developer"]}),
        ("Career Details", "/career-details/data%20analyst", "GET", None),
        
        # Interview features
        ("Start Interview", "/interview/start", "POST", {"career": "Software Engineer", "level": "fresher"}),
        ("Interview Tips", "/interview/tips/software%20engineer", "GET", None),
        
        # O*NET features
        ("O*NET Data", "/onet/data", "GET", None),
        ("Search Careers", "/onet/search", "POST", {"keyword": "engineer"}),
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test_feature(*test):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"📊 Test Results: {passed} Passed, {failed} Failed")
    print(f"{'='*60}\n")
    
    return passed, failed

if __name__ == "__main__":
    main()
