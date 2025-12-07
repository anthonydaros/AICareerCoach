/**
 * Demo data for showcasing the AI Career Coach functionality
 */

export const DEMO_RESUME = `JOHN DOE
Senior Software Engineer

Contact: john.doe@email.com | (555) 123-4567 | San Francisco, CA
LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe

PROFESSIONAL SUMMARY
Experienced Software Engineer with 6+ years of expertise in full-stack development, cloud architecture, and team leadership. Proficient in Python, TypeScript, React, and AWS. Passionate about building scalable applications and mentoring junior developers.

TECHNICAL SKILLS
Languages: Python, TypeScript, JavaScript, Go, SQL
Frontend: React, Next.js, Vue.js, TailwindCSS, HTML5, CSS3
Backend: FastAPI, Node.js, Express, Django, GraphQL
Cloud & DevOps: AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes, CI/CD, Terraform
Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
Tools: Git, GitHub Actions, Jest, PyTest, Agile/Scrum

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021 - Present
- Led development of microservices architecture serving 2M+ daily users
- Reduced API response time by 40% through optimization and caching strategies
- Mentored team of 5 junior developers, improving code quality by 25%
- Implemented CI/CD pipelines reducing deployment time from 2 hours to 15 minutes
- Technologies: Python, FastAPI, React, PostgreSQL, AWS, Docker

Software Engineer | StartupXYZ | 2019 - 2021
- Built real-time collaboration features using WebSockets and Redis
- Developed RESTful APIs consumed by mobile and web applications
- Contributed to open-source projects with 500+ GitHub stars
- Technologies: Node.js, React, MongoDB, AWS Lambda

Junior Developer | WebAgency Co. | 2018 - 2019
- Created responsive web applications for 20+ clients
- Implemented automated testing increasing code coverage to 85%
- Technologies: JavaScript, Vue.js, PHP, MySQL

EDUCATION
B.S. Computer Science | University of California, Berkeley | 2018
- GPA: 3.7/4.0, Dean's List

CERTIFICATIONS
- AWS Solutions Architect Associate (2023)
- Certified Kubernetes Administrator (2022)

PROJECTS
Open Source CLI Tool | github.com/johndoe/cli-tool
- Built developer productivity tool with 2,000+ downloads
- Technologies: Go, Cobra, GitHub Actions`;

export const DEMO_JOBS = [
  {
    id: "demo-1",
    text: `Senior Full Stack Developer - TechVentures Inc.

Location: Remote (US-based)
Salary: $150,000 - $180,000

About Us:
TechVentures is a rapidly growing SaaS company building the next generation of enterprise collaboration tools. We're looking for a Senior Full Stack Developer to join our platform team.

Requirements:
- 5+ years of experience in full-stack development
- Strong proficiency in React, TypeScript, and Node.js
- Experience with cloud platforms (AWS or GCP preferred)
- Knowledge of PostgreSQL and Redis
- Understanding of microservices architecture
- Excellent communication and collaboration skills

Nice to Have:
- Experience with GraphQL
- Familiarity with Kubernetes and Docker
- Open source contributions

Responsibilities:
- Design and implement new features across the full stack
- Collaborate with product and design teams
- Mentor junior developers
- Participate in code reviews and architectural decisions
- Improve system performance and reliability

Benefits:
- Fully remote work
- Unlimited PTO
- 401k matching
- Health, dental, and vision insurance
- Annual learning budget`
  },
  {
    id: "demo-2",
    text: `Python Backend Engineer - DataFlow AI

Location: San Francisco, CA (Hybrid)
Salary: $140,000 - $170,000

About the Role:
DataFlow AI is building cutting-edge machine learning infrastructure. We need a Python Backend Engineer to help scale our data processing pipelines.

Requirements:
- 4+ years of Python development experience
- Experience with FastAPI or Django
- Strong understanding of distributed systems
- PostgreSQL and Redis experience
- AWS or GCP cloud experience
- CI/CD and testing best practices

Nice to Have:
- ML/AI background
- Kubernetes experience
- Experience with Kafka or similar message queues

What You'll Do:
- Build and maintain high-throughput data pipelines
- Design APIs for ML model serving
- Optimize database queries and system performance
- Implement monitoring and alerting
- Collaborate with ML engineers

Perks:
- Competitive equity package
- Premium healthcare
- Catered lunches
- Professional development budget`
  }
];

export const DEMO_ANALYSIS_RESULT = {
  atsScore: {
    overall: 78,
    breakdown: {
      keywords: 85,
      formatting: 72,
      experience: 80,
      skills: 75
    },
    suggestions: [
      "Add more action verbs at the beginning of bullet points",
      "Include specific metrics and achievements in each role",
      "Consider adding a 'Key Achievements' section"
    ]
  },
  jobMatches: [
    {
      jobId: "demo-1",
      matchScore: 82,
      matchedSkills: ["React", "TypeScript", "Node.js", "AWS", "PostgreSQL", "Redis", "Microservices"],
      missingSkills: ["GraphQL"],
      highlights: [
        "Strong match for full-stack development requirements",
        "Cloud experience aligns well with AWS preference",
        "Leadership and mentoring experience is a plus"
      ]
    },
    {
      jobId: "demo-2",
      matchScore: 75,
      matchedSkills: ["Python", "FastAPI", "PostgreSQL", "Redis", "AWS", "CI/CD"],
      missingSkills: ["Kafka", "ML background"],
      highlights: [
        "Python and FastAPI experience directly matches requirements",
        "Cloud and database skills are well aligned",
        "Consider highlighting any ML/AI exposure"
      ]
    }
  ]
};
