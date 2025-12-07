#!/usr/bin/env python3
"""
Test script for CareerAI model validation.
Tests all API endpoints and validates model responses.
"""

import requests
import json
import time
from datetime import datetime

API_BASE = "http://localhost:8000"

# Sample test data
SAMPLE_RESUME = """
JOHN DOE
Senior Software Engineer
john.doe@email.com | (555) 123-4567 | San Francisco, CA

SUMMARY
Senior Software Engineer with 7+ years of experience in full-stack development,
specializing in Python, React, and cloud technologies. Led teams of 5+ engineers
and delivered critical systems handling 10M+ daily requests.

EXPERIENCE

Senior Software Engineer | TechCorp Inc. | Jan 2020 - Present
- Led development of microservices architecture using Python, FastAPI, and Kubernetes
- Reduced system latency by 40% through optimization of database queries and caching
- Mentored 4 junior developers and conducted code reviews for team of 8
- Implemented CI/CD pipelines using GitHub Actions, reducing deployment time by 60%

Software Engineer | StartupXYZ | Jun 2017 - Dec 2019
- Built real-time data processing pipeline handling 1M+ events/day using Python and Kafka
- Developed React frontend with TypeScript for internal analytics dashboard
- Integrated AWS services (S3, Lambda, DynamoDB) for scalable data storage
- Collaborated with product team to define technical requirements

Junior Developer | WebAgency | Mar 2015 - May 2017
- Developed responsive web applications using JavaScript, HTML5, CSS3
- Maintained and enhanced legacy PHP applications
- Participated in agile ceremonies and sprint planning

EDUCATION
Bachelor of Science in Computer Science | UC Berkeley | 2014
GPA: 3.7/4.0

SKILLS
Programming: Python, JavaScript, TypeScript, SQL, Go
Frameworks: FastAPI, Django, React, Node.js
Cloud: AWS (S3, Lambda, EC2, RDS), GCP, Kubernetes, Docker
Databases: PostgreSQL, MongoDB, Redis
Tools: Git, GitHub Actions, Jenkins, Terraform

CERTIFICATIONS
- AWS Solutions Architect Associate (2022)
- Kubernetes Administrator (CKA) (2021)
"""

SAMPLE_JOB = """
Senior Backend Engineer - TechGiant Corp

Location: San Francisco, CA (Hybrid)
Salary: $180,000 - $220,000

About Us:
TechGiant Corp is a leading technology company building next-generation cloud platforms.

Requirements:
- 5+ years of software engineering experience
- Strong proficiency in Python and/or Go
- Experience with microservices architecture and Kubernetes
- Solid understanding of database design (SQL and NoSQL)
- Experience with AWS or GCP cloud services
- Strong communication and teamwork skills

Nice to Have:
- Experience with real-time data processing
- Knowledge of machine learning/AI
- Open source contributions
- Leadership or mentoring experience

Responsibilities:
- Design and implement scalable backend services
- Collaborate with cross-functional teams
- Mentor junior engineers
- Participate in architecture decisions
- Write clean, maintainable code with comprehensive tests
"""

def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def print_result(test_name: str, passed: bool, details: str = ""):
    """Print test result."""
    status = "PASS" if passed else "FAIL"
    symbol = "[OK]" if passed else "[X]"
    print(f"{symbol} {test_name}: {status}")
    if details:
        print(f"    {details}")

def test_health():
    """Test health endpoint."""
    print_section("TEST 1: Health Check")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        data = response.json()

        passed = response.status_code == 200 and data.get("status") == "healthy"
        print_result("Health endpoint", passed, f"Status: {data.get('status', 'unknown')}")
        return passed
    except Exception as e:
        print_result("Health endpoint", False, str(e))
        return False

def test_analyze():
    """Test full analysis endpoint."""
    print_section("TEST 2: Full Analysis (/analyze)")

    payload = {
        "resume_text": SAMPLE_RESUME,
        "job_postings": [
            {"id": "job1", "text": SAMPLE_JOB}
        ]
    }

    try:
        print("Sending request... (this may take a while)")
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/analyze",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=180
        )
        elapsed = time.time() - start_time

        if response.status_code != 200:
            print_result("Analysis endpoint", False, f"Status: {response.status_code}, Error: {response.text[:200]}")
            return False, None

        data = response.json()
        print(f"Response received in {elapsed:.1f}s")

        # Validate response structure
        checks = {
            "has_ats_result": "ats_result" in data,
            "has_job_matches": "job_matches" in data and len(data["job_matches"]) > 0,
            "has_seniority": "seniority" in data,
            "has_stability": "stability" in data,
            "has_best_fit": "best_fit" in data,
        }

        for check_name, passed in checks.items():
            print_result(check_name, passed)

        # Detailed ATS result validation
        if checks["has_ats_result"]:
            ats = data["ats_result"]
            print("\n  ATS Score Details:")
            print(f"    Total Score: {ats.get('total_score', 'N/A')}/100")
            print(f"    Skill Score: {ats.get('skill_score', 'N/A')}/40")
            print(f"    Experience Score: {ats.get('experience_score', 'N/A')}/30")
            print(f"    Keyword Analysis Count: {len(ats.get('keyword_analysis', []))}")

            # Check if scores are reasonable
            total = ats.get('total_score', 0)
            ats_valid = 0 <= total <= 100
            print_result("ATS score in valid range", ats_valid, f"Score: {total}")

        # Job match validation
        if checks["has_job_matches"]:
            match = data["job_matches"][0]
            print("\n  Job Match Details:")
            print(f"    Job Title: {match.get('job_title', 'N/A')}")
            print(f"    Match %: {match.get('match_percentage', 'N/A')}%")
            print(f"    Match Level: {match.get('match_level', 'N/A')}")
            print(f"    Matched Skills: {len(match.get('matched_skills', []))}")
            print(f"    Missing Skills: {len(match.get('missing_skills', []))}")
            print(f"    Strengths: {len(match.get('strengths', []))}")

            match_pct = match.get('match_percentage', 0)
            match_valid = 0 <= match_pct <= 100
            print_result("Match percentage in valid range", match_valid, f"Match: {match_pct}%")

        # Seniority validation
        if checks["has_seniority"]:
            sen = data["seniority"]
            print("\n  Seniority Details:")
            print(f"    Level: {sen.get('level', 'N/A')}")
            print(f"    Confidence: {sen.get('confidence', 'N/A')}%")
            print(f"    Years Experience: {sen.get('years_experience', 'N/A')}")

            level = sen.get('level', '').lower()
            level_valid = level in ['junior', 'mid', 'senior', 'lead', 'principal', 'staff']
            print_result("Seniority level valid", level_valid, f"Level: {level}")

        all_passed = all(checks.values())
        print_result("\nOverall Analysis Test", all_passed)

        return all_passed, data

    except requests.exceptions.Timeout:
        print_result("Analysis endpoint", False, "Request timed out (180s)")
        return False, None
    except Exception as e:
        print_result("Analysis endpoint", False, str(e))
        return False, None

def test_ats_score():
    """Test ATS score endpoint."""
    print_section("TEST 3: ATS Score Only (/ats-score)")

    payload = {
        "resume_text": SAMPLE_RESUME,
        "job_text": SAMPLE_JOB
    }

    try:
        print("Sending request...")
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/ats-score",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        elapsed = time.time() - start_time

        if response.status_code != 200:
            print_result("ATS Score endpoint", False, f"Status: {response.status_code}")
            return False

        data = response.json()
        print(f"Response received in {elapsed:.1f}s")

        # Validate
        has_score = "total_score" in data
        score = data.get("total_score", 0)
        score_valid = 0 <= score <= 100

        print(f"  Total Score: {score}/100")
        print(f"  Skill Score: {data.get('skill_score', 'N/A')}/40")
        print(f"  Keywords Found: {len([k for k in data.get('keyword_analysis', []) if k.get('found_in_resume')])}")

        print_result("ATS Score endpoint", has_score and score_valid)
        return has_score and score_valid

    except Exception as e:
        print_result("ATS Score endpoint", False, str(e))
        return False

def test_interview_prep():
    """Test interview prep endpoint."""
    print_section("TEST 4: Interview Prep (/interview-prep)")

    payload = {
        "resume_text": SAMPLE_RESUME,
        "job_text": SAMPLE_JOB,
        "skill_gaps": ["Go", "machine learning"]
    }

    try:
        print("Sending request...")
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/interview-prep",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        elapsed = time.time() - start_time

        if response.status_code != 200:
            print_result("Interview Prep endpoint", False, f"Status: {response.status_code}, Error: {response.text[:200]}")
            return False

        data = response.json()
        print(f"Response received in {elapsed:.1f}s")

        # Validate
        has_questions = "questions" in data and len(data["questions"]) > 0
        has_job_title = "job_title" in data

        print(f"  Job Title: {data.get('job_title', 'N/A')}")
        print(f"  Questions Generated: {len(data.get('questions', []))}")

        if has_questions:
            print("\n  Sample Questions:")
            for i, q in enumerate(data["questions"][:3], 1):
                category = q.get("category", "unknown")
                question = q.get("question", "")[:80]
                print(f"    {i}. [{category}] {question}...")

        passed = has_questions and has_job_title
        print_result("Interview Prep endpoint", passed)
        return passed

    except Exception as e:
        print_result("Interview Prep endpoint", False, str(e))
        return False

def test_coaching_tips():
    """Test coaching tips endpoint."""
    print_section("TEST 5: Coaching Tips (/coaching-tips)")

    payload = {
        "resume_text": SAMPLE_RESUME,
        "job_postings": [
            {"id": "job1", "text": SAMPLE_JOB}
        ],
        "match_results": []
    }

    try:
        print("Sending request...")
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/coaching-tips",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        elapsed = time.time() - start_time

        if response.status_code != 200:
            print_result("Coaching Tips endpoint", False, f"Status: {response.status_code}, Error: {response.text[:200]}")
            return False

        data = response.json()
        print(f"Response received in {elapsed:.1f}s")

        # Validate
        has_tips = "tips" in data and len(data["tips"]) > 0

        print(f"  Tips Generated: {len(data.get('tips', []))}")

        if has_tips:
            print("\n  Sample Tips:")
            for i, tip in enumerate(data["tips"][:3], 1):
                category = tip.get("category", "unknown")
                title = tip.get("title", "")[:50]
                print(f"    {i}. [{category}] {title}")

        print_result("Coaching Tips endpoint", has_tips)
        return has_tips

    except Exception as e:
        print_result("Coaching Tips endpoint", False, str(e))
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print(" CAREERAI MODEL VALIDATION TESTS")
    print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results = {}

    # Test 1: Health
    results["health"] = test_health()

    if not results["health"]:
        print("\n[!] Health check failed. Is the backend running?")
        print("    Run: cd backend && uvicorn src.presentation.api.main:app --reload")
        return

    # Test 2: Full Analysis
    results["analyze"], analyze_data = test_analyze()

    # Test 3: ATS Score
    results["ats_score"] = test_ats_score()

    # Test 4: Interview Prep
    results["interview_prep"] = test_interview_prep()

    # Test 5: Coaching Tips
    results["coaching_tips"] = test_coaching_tips()

    # Summary
    print_section("TEST SUMMARY")

    total = len(results)
    passed = sum(1 for r in results.values() if r)

    print(f"\nResults: {passed}/{total} tests passed")
    print("-" * 40)

    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        symbol = "[OK]" if result else "[X]"
        print(f"  {symbol} {test_name}: {status}")

    print("-" * 40)

    if passed == total:
        print("\n[SUCCESS] All tests passed! CareerAI model is working correctly.")
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed. Review the output above.")

    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
