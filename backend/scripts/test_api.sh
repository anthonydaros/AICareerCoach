#!/bin/bash
# AI Career Coach - Automated API Test Script
# Tests the /analyze endpoint with knowledge bases integration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
API_URL="${API_URL:-https://api-career.anthonymax.com}"
LOCAL_URL="${LOCAL_URL:-http://localhost:8000}"
TEST_OUTPUT_DIR="/tmp/career-coach-tests"
TIMEOUT=120

# Create test output directory
mkdir -p "$TEST_OUTPUT_DIR"

echo -e "${BLUE}=== AI Career Coach API Test ===${NC}"
echo -e "API URL: $API_URL"
echo -e "Test Output: $TEST_OUTPUT_DIR"
echo ""

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}[PASS]${NC} $2"
    else
        echo -e "${RED}[FAIL]${NC} $2"
    fi
}

# Test 1: Health Check
echo -e "${YELLOW}[TEST 1] Health Check${NC}"
HTTP_CODE=$(curl -s -o "$TEST_OUTPUT_DIR/health.json" -w "%{http_code}" "$API_URL/health")
if [ "$HTTP_CODE" = "200" ]; then
    print_status 0 "Health endpoint returned 200"
    cat "$TEST_OUTPUT_DIR/health.json" | python3 -m json.tool 2>/dev/null || cat "$TEST_OUTPUT_DIR/health.json"
else
    print_status 1 "Health endpoint returned $HTTP_CODE"
fi
echo ""

# Create test payload
echo -e "${YELLOW}[TEST 2] Creating test payload${NC}"
cat > "$TEST_OUTPUT_DIR/test-payload.json" << 'EOF'
{
  "resume_text": "John Doe - Senior Software Engineer\n\nSUMMARY:\n8 years of experience in backend development. Expert in Python, FastAPI, PostgreSQL. Led teams of 5+ engineers at Google and Meta. Architected microservices handling 10M+ requests/day. Strong background in system design, distributed systems, and cloud architecture (AWS, GCP). Previously worked at Meta (2022-2024), Google (2019-2022), Amazon (2016-2019).\n\nSKILLS:\nPython, FastAPI, Django, PostgreSQL, Redis, Docker, Kubernetes, AWS, GCP, System Design, Microservices, CI/CD, GitHub Actions\n\nEXPERIENCE:\n\nSenior Software Engineer - Meta (2022-2024)\n- Led backend team of 5 engineers\n- Architected messaging service handling 10M requests/day\n- Reduced latency by 40% through optimization\n\nSoftware Engineer - Google (2019-2022)\n- Developed internal tools used by 5000+ engineers\n- Implemented CI/CD pipelines reducing deployment time by 60%\n\nSoftware Engineer - Amazon (2016-2019)\n- Built RESTful APIs for e-commerce platform\n- Improved database query performance by 50%\n\nEDUCATION:\nBS Computer Science - MIT (2016)\n\nCERTIFICATIONS:\n- AWS Solutions Architect\n- Google Cloud Professional",
  "job_postings": [
    {
      "raw_text": "Senior Backend Engineer - TechStartup\n\nWe're looking for a Senior Backend Engineer to join our growing team!\n\nRequirements:\n- 5+ years of Python experience\n- Experience with FastAPI or Django\n- Strong SQL skills (PostgreSQL preferred)\n- Docker and Kubernetes experience\n- AWS or GCP cloud experience\n- System design skills\n\nNice to have:\n- Experience with Redis\n- CI/CD pipeline experience\n- Leadership experience\n\nAbout us: Fast-growing Series B startup building next-gen developer tools."
    },
    {
      "raw_text": "Staff Engineer - BigCorp\n\nJoin our platform team as a Staff Engineer!\n\nRequirements:\n- 10+ years software development experience\n- Expert in distributed systems\n- Strong in Python, Go, or Java\n- Experience with Kubernetes at scale\n- Track record of technical leadership\n\nResponsibilities:\n- Define technical strategy\n- Mentor senior engineers\n- Drive architectural decisions"
    }
  ]
}
EOF
print_status 0 "Test payload created"
echo ""

# Test 3: Analyze Endpoint
echo -e "${YELLOW}[TEST 3] Analyze Endpoint (may take up to 2 minutes)${NC}"
START_TIME=$(date +%s)
HTTP_CODE=$(curl -s -X POST "$API_URL/analyze" \
    -H "Content-Type: application/json" \
    -d @"$TEST_OUTPUT_DIR/test-payload.json" \
    -o "$TEST_OUTPUT_DIR/analyze-result.json" \
    -w "%{http_code}" \
    --max-time $TIMEOUT)
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ "$HTTP_CODE" = "200" ]; then
    print_status 0 "Analyze endpoint returned 200 (${DURATION}s)"

    # Parse and display results
    echo -e "\n${BLUE}--- Analysis Results ---${NC}"

    # Extract key metrics using Python
    python3 << PYTHON
import json
import sys

try:
    with open('$TEST_OUTPUT_DIR/analyze-result.json', 'r') as f:
        data = json.load(f)

    print(f"\nResume Parsed:")
    if 'resume' in data:
        r = data['resume']
        print(f"  Name: {r.get('name', 'N/A')}")
        print(f"  Total Experience: {r.get('total_experience_years', 0)} years")
        skills = r.get('skills', [])
        if skills:
            skill_names = [s.get('name', s) if isinstance(s, dict) else s for s in skills[:10]]
            print(f"  Top Skills: {', '.join(skill_names)}")

    print(f"\nJob Matches:")
    if 'job_matches' in data:
        for i, match in enumerate(data['job_matches'], 1):
            print(f"  {i}. {match.get('job_title', 'Unknown')} - {match.get('match_percentage', 0):.1f}% match")
            if match.get('is_best_fit'):
                print(f"     [BEST FIT]")

    print(f"\nATS Scores:")
    if 'ats_results' in data:
        for i, ats in enumerate(data['ats_results'], 1):
            print(f"  Job {i}: {ats.get('total_score', 0):.1f}/100")
            print(f"    Skills: {ats.get('skill_score', 0):.1f}, Experience: {ats.get('experience_score', 0):.1f}")

    print(f"\nSeniority Analysis:")
    if 'seniority_analysis' in data:
        sen = data['seniority_analysis']
        print(f"  Level: {sen.get('level', 'N/A')}")
        print(f"  Confidence: {sen.get('confidence', 0):.1f}%")

    print(f"\nStability Analysis:")
    if 'stability_analysis' in data:
        stab = data['stability_analysis']
        print(f"  Score: {stab.get('score', 0)}/100")
        print(f"  Avg Tenure: {stab.get('avg_tenure_months', 0):.1f} months")

    print(f"\n{'-'*40}")
    print("Full response saved to: $TEST_OUTPUT_DIR/analyze-result.json")

except Exception as e:
    print(f"Error parsing response: {e}")
    sys.exit(1)
PYTHON

else
    print_status 1 "Analyze endpoint returned $HTTP_CODE"
    echo "Response:"
    cat "$TEST_OUTPUT_DIR/analyze-result.json" 2>/dev/null || echo "(no response body)"
fi
echo ""

# Test 4: Knowledge Base Integration Check
echo -e "${YELLOW}[TEST 4] Knowledge Base Integration Check${NC}"
cd /Users/anthonymax/Documents/GIT/AI\ Career\ Coach\ MVP/backend
python3 << 'PYTHON'
import sys
sys.path.insert(0, '.')

try:
    # Test imports
    from src.domain.knowledge.job_titles import ROLE_CATEGORIES, detect_seniority_from_title
    from src.domain.knowledge.seniority_detection import SENIORITY_THRESHOLDS
    from src.domain.knowledge.career_stability import TECH_LAYOFF_COMPANIES
    from src.domain.knowledge.ats_scoring import ATS_WEIGHTS
    from src.domain.services.skill_relationships import SKILL_RELATIONSHIPS, TRANSFERABLE_SKILLS

    print("  Knowledge bases loaded successfully!")
    print(f"    - Role categories: {len(ROLE_CATEGORIES)}")
    print(f"    - Seniority levels (US): {len(SENIORITY_THRESHOLDS['us'])}")
    print(f"    - Seniority levels (BR): {len(SENIORITY_THRESHOLDS['br'])}")
    print(f"    - Layoff companies: {len(TECH_LAYOFF_COMPANIES)}")
    print(f"    - Skill relationships: {len(SKILL_RELATIONSHIPS)}")
    print(f"    - Transferable skills: {len(TRANSFERABLE_SKILLS)}")

    # Test seniority detection
    level, name = detect_seniority_from_title("Senior Software Engineer")
    print(f"\n  Title detection test: 'Senior Software Engineer' -> Level {level} ({name})")

    sys.exit(0)
except Exception as e:
    print(f"  Error: {e}")
    sys.exit(1)
PYTHON
KB_STATUS=$?
print_status $KB_STATUS "Knowledge base integration"
echo ""

# Summary
echo -e "${BLUE}=== Test Summary ===${NC}"
echo -e "API URL: $API_URL"
echo -e "Response time: ${DURATION}s"
echo -e "Output directory: $TEST_OUTPUT_DIR"

if [ "$HTTP_CODE" = "200" ] && [ "$KB_STATUS" -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed.${NC}"
    exit 1
fi
