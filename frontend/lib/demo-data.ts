/**
 * Demo data for showcasing the AI Career Coach functionality
 * Updated to showcase: AI/LLM skills, Low-code automation, Brazilian market context,
 * Design career track, Stability analysis, and Dynamic role-based scoring
 */

// =============================================================================
// DEMO RESUME - Showcases AI/LLM, Automation, and Brazilian context
// =============================================================================
export const DEMO_RESUME = `JOAO SILVA
Desenvolvedor Pleno / AI Engineer
Portfolio: behance.net/joaosilva | dribbble.com/joaosilva

Contact: joao.silva@email.com | +55 11 99999-9999 | Sao Paulo, SP, Brazil
LinkedIn: linkedin.com/in/joaosilva | GitHub: github.com/joaosilva

RESUMO PROFISSIONAL
Desenvolvedor Pleno com 5+ anos de experiencia em desenvolvimento full-stack e AI/LLM.
Especialista em automacao com n8n, Make e Zapier. Experiencia com LangChain, RAG e vector databases.
Liderou migracao de sistemas legados para arquitetura de microservices.

HABILIDADES TECNICAS
Linguagens: Python, TypeScript, JavaScript, SQL
AI/LLM: LangChain, CrewAI, OpenAI API, RAG, Prompt Engineering, Embeddings
Vector DBs: Pinecone, Chroma, FAISS, Weaviate
Automacao: n8n, Make (Integromat), Zapier, Power Automate
Frontend: React, Next.js, TailwindCSS, Figma
Backend: FastAPI, Node.js, Django
Cloud & DevOps: AWS (EC2, S3, Lambda), Docker, Kubernetes, Terraform
Databases: PostgreSQL, MongoDB, Redis

EXPERIENCIA PROFISSIONAL

AI Engineer PJ | TechStartup (Series A) | 2023 - Presente
- Arquitetei sistema RAG com LangChain e Pinecone para chatbot empresarial
- Implementei pipelines de automacao com n8n integrando 15+ servicos
- Reduzi tempo de processamento de dados em 60% com embeddings otimizados
- Liderei equipe de 4 desenvolvedores em projeto de AI generativa
- Tecnologias: Python, LangChain, FastAPI, Pinecone, n8n, AWS

Desenvolvedor Pleno CLT | Nubank | 2022 - 2023
- Desenvolvi APIs de alta disponibilidade servindo 5M+ usuarios
- Implementei sistema de recomendacao usando machine learning
- Mentored 3 desenvolvedores juniores em boas praticas de codigo
- Participei da migracao para arquitetura de microservices
- Tecnologias: Python, FastAPI, PostgreSQL, Kubernetes, Redis

Software Engineer | Meta | 2021 - 2022
- Contributed to React Native framework improvements
- Built internal tools using GraphQL and TypeScript
- Participated in cross-functional team of 8 engineers
- Laid off during 2022 restructuring
- Technologies: TypeScript, React, GraphQL, Node.js

Desenvolvedor Junior | Startup XYZ (Seed) | 2019 - 2021
- Criou automacoes com Zapier e Make para processos internos
- Desenvolveu features frontend com React e Vue.js
- Assistiu na implementacao de testes automatizados
- Tecnologias: JavaScript, React, Vue.js, Zapier, Make

FORMACAO
Bacharelado em Ciencia da Computacao | USP | 2019
- Trabalho de conclusao: Sistemas de Recomendacao com Deep Learning

CERTIFICACOES
- AWS Solutions Architect Associate (2023)
- LangChain Developer Certificate (2024)
- n8n Expert Certification (2023)

PROJETOS
Chatbot RAG para E-commerce | github.com/joaosilva/ecommerce-rag
- Sistema de atendimento automatizado com LangChain e vector search
- Tecnologias: Python, LangChain, Pinecone, FastAPI`;

// =============================================================================
// DEMO JOBS - Multiple role types to showcase dynamic scoring
// =============================================================================
export const DEMO_JOBS = [
  {
    id: "demo-ai-engineer",
    text: `AI Engineer - LatAm Fintech (Series B)

Location: Remote (Brazil preferred)
Salary: R$ 25,000 - R$ 35,000/month (PJ)

Sobre a Empresa:
Fintech em crescimento acelerado buscando AI Engineer para liderar iniciativas de IA generativa.
Ambiente startup com equity e flexibilidade total.

Requisitos:
- 4+ anos de experiencia em desenvolvimento Python
- Experiencia solida com LangChain, RAG e vector databases
- Conhecimento de Pinecone, Weaviate ou Chroma
- Experiencia com prompt engineering e fine-tuning
- AWS ou GCP para deploy de modelos
- Bonus: Experiencia com CrewAI ou AutoGen

Responsabilidades:
- Arquitetar e implementar solucoes de AI/LLM
- Desenvolver pipelines de RAG para produtos
- Liderar equipe tecnica de 3-5 pessoas
- Definir estrategia tecnica de AI
- Colaborar com times de produto e design

Beneficios:
- Contrato PJ com flexibilidade
- Equity da empresa
- Budget para cursos e conferencias
- Hardware de escolha`
  },
  {
    id: "demo-automation",
    text: `Automation Specialist - Enterprise Corp

Location: Hybrid (Sao Paulo, SP)
Type: CLT
Salary: R$ 12,000 - R$ 18,000

Sobre a Vaga:
Buscamos especialista em automacao para otimizar processos empresariais usando
ferramentas low-code/no-code e integracoes.

Requisitos:
- 3+ anos de experiencia com automacao de processos
- Dominio de n8n, Make (Integromat) ou Zapier
- Experiencia com Power Automate e Microsoft 365
- Conhecimento de APIs REST e webhooks
- SQL basico para consultas e relatorios
- Habilidade de documentar fluxos e processos

Diferenciais:
- Experiencia com Airtable ou Notion como backend
- Conhecimento de Python para scripts customizados
- Certificacoes em ferramentas de automacao

O que voce vai fazer:
- Mapear e automatizar processos de negocio
- Criar integracoes entre sistemas internos e externos
- Treinar equipes em ferramentas de automacao
- Documentar workflows e melhores praticas
- Reduzir trabalho manual em 50%+

Beneficios CLT:
- Vale refeicao e alimentacao
- Plano de saude e odontologico
- PLR anual
- Horario flexivel`
  },
  {
    id: "demo-design",
    text: `Senior Product Designer - Design Studio

Location: Remote (Global)
Salary: $80,000 - $120,000 USD

About the Role:
Award-winning design studio seeking Senior Product Designer to lead design systems
and mentor junior designers.

Requirements:
- 5+ years of product design experience
- Expert-level Figma skills
- Experience with design systems and component libraries
- Strong portfolio with case studies (Behance/Dribbble)
- User research and usability testing experience
- Knowledge of design tokens and accessibility (WCAG)

Nice to Have:
- Experience with Framer or Webflow
- Motion design skills
- Frontend development basics (HTML/CSS)

Responsibilities:
- Lead design system architecture
- Conduct user research and testing
- Mentor team of 3 designers
- Collaborate with engineering on implementation
- Present designs to stakeholders

Benefits:
- Fully remote, async culture
- Unlimited PTO
- Annual design conference budget
- Latest hardware and software`
  },
  {
    id: "demo-product",
    text: `Product Manager - Tech Company

Location: Sao Paulo, SP (Hybrid)
Type: CLT
Salary: R$ 20,000 - R$ 30,000

About Us:
Growing tech company looking for PM to lead our AI product initiatives.

Requirements:
- 4+ years as Product Manager or Product Owner
- Experience with AI/ML products preferred
- Strong stakeholder management skills
- Data-driven decision making
- Agile/Scrum methodology
- Technical background is a plus

Responsibilities:
- Define product roadmap and strategy
- Manage backlog and prioritization
- Work with engineering and design teams
- Present to C-level stakeholders
- Drive product metrics and OKRs

Benefits:
- Competitive CLT package
- Stock options
- Health and dental insurance
- Flexible working hours`
  }
];

// =============================================================================
// DEMO ANALYSIS RESULT - Showcases new scoring features
// =============================================================================
export const DEMO_ANALYSIS_RESULT = {
  // ATS Score with role-type specific weights
  atsScore: {
    overall: 82,
    roleType: "technical", // Detected role type
    breakdown: {
      skillMatch: 88,    // AI/LLM skills matched well
      experience: 75,    // 5 years experience
      education: 70,     // BS in Computer Science
      certifications: 85, // AWS + LangChain certs
      keywords: 80       // Good keyword coverage
    },
    suggestions: [
      "Highlight RAG implementation metrics (latency, accuracy improvements)",
      "Add quantifiable results for n8n automation projects",
      "Consider AWS ML Specialty certification for AI roles"
    ]
  },

  // Seniority Detection with Brazilian context
  seniorityAnalysis: {
    level: "mid", // Pleno level detected
    confidence: 78,
    yearsExperience: 5,
    indicators: [
      "Brazilian 'Pleno' title detected",
      "5 years experience indicates mid-level",
      "Senior-level AI/LLM skills (LangChain, RAG)",
      "Led team of 4 developers",
      "Mix of advanced and intermediate skills"
    ],
    scores: {
      experience: 0.6,
      complexity: 0.75,
      autonomy: 0.7,
      skills: 0.8,
      leadership: 0.65,
      impact: 0.6
    }
  },

  // Stability Analysis with Brazilian employment context
  stabilityAnalysis: {
    score: 72,
    totalCompanies: 4,
    averageTenure: 18, // months
    timeline: [
      {
        company: "TechStartup (Series A)",
        duration: 12,
        contractType: "pj", // PJ detected - reduced penalty
        startupStage: "series_a",
        isLayoffPeriod: false
      },
      {
        company: "Nubank",
        duration: 12,
        contractType: "clt",
        isLayoffPeriod: true, // Brazilian tech layoffs 2022-2024
        startupStage: null
      },
      {
        company: "Meta",
        duration: 12,
        contractType: "unknown",
        isLayoffPeriod: true, // Known layoff company 2022
        startupStage: null
      },
      {
        company: "Startup XYZ (Seed)",
        duration: 24,
        contractType: "unknown",
        startupStage: "early_stage", // Early stage - reduced penalty
        isLayoffPeriod: false
      }
    ],
    indicators: [
      "PJ contract at TechStartup - short tenure expected",
      "Meta departure during 2022 layoffs - no penalty applied",
      "Nubank departure during Brazilian tech layoff period",
      "Early-stage startup tenure adjusted (Seed stage)",
      "Stable 2-year tenure at first position"
    ],
    flags: []
  },

  // Job Matches with expanded skill inference
  jobMatches: [
    {
      jobId: "demo-ai-engineer",
      jobTitle: "AI Engineer - LatAm Fintech",
      matchScore: 88,
      roleType: "data", // AI/Data role detected
      matchedSkills: [
        "Python", "LangChain", "RAG", "Pinecone", "Prompt Engineering",
        "FastAPI", "AWS", "Embeddings", "Vector Databases"
      ],
      inferredSkills: [ // Skills inferred from relationships
        "PyTorch", "Transformers", "Semantic Search", "LLMs"
      ],
      missingSkills: ["CrewAI", "AutoGen", "Fine-tuning"],
      highlights: [
        "Strong LangChain and RAG experience directly matches requirements",
        "Vector database expertise with Pinecone and Chroma",
        "PJ contract type aligns with job offering",
        "Leadership experience with 4-person team"
      ],
      concerns: [
        "No explicit CrewAI experience mentioned"
      ],
      seniorityMatch: "match" // Mid-level matches job requirements
    },
    {
      jobId: "demo-automation",
      jobTitle: "Automation Specialist",
      matchScore: 85,
      roleType: "technical",
      matchedSkills: [
        "n8n", "Make", "Zapier", "APIs", "Webhooks", "Python", "SQL"
      ],
      inferredSkills: [
        "Automation Workflows", "Integrations", "Data Transformation"
      ],
      missingSkills: ["Power Automate", "Airtable"],
      highlights: [
        "Expert-level n8n experience with 15+ integrations",
        "Make (Integromat) and Zapier proficiency",
        "Python skills for custom automations",
        "CLT position matches employment preference"
      ],
      concerns: [
        "Power Automate experience not listed",
        "May be overqualified - consider negotiating seniority"
      ],
      seniorityMatch: "over-qualified"
    },
    {
      jobId: "demo-design",
      jobTitle: "Senior Product Designer",
      matchScore: 45,
      roleType: "design", // Design role - portfolio scoring applied
      matchedSkills: ["Figma"],
      inferredSkills: [],
      missingSkills: [
        "Design Systems", "User Research", "Usability Testing",
        "Design Tokens", "WCAG Accessibility"
      ],
      highlights: [
        "Has portfolio links (Behance, Dribbble)",
        "Figma mentioned in skills"
      ],
      concerns: [
        "Primary background is engineering, not design",
        "Missing core design skills and experience",
        "Portfolio may not have design case studies"
      ],
      seniorityMatch: "under-qualified"
    },
    {
      jobId: "demo-product",
      jobTitle: "Product Manager",
      matchScore: 62,
      roleType: "product", // Product role - leadership scoring applied
      matchedSkills: ["AI/ML Products", "Technical Background", "Agile"],
      inferredSkills: ["Technical Communication"],
      missingSkills: [
        "Product Roadmap", "Stakeholder Management", "OKRs"
      ],
      highlights: [
        "Technical AI/ML background valuable for AI products",
        "Leadership experience from leading dev team",
        "Experience with product features development"
      ],
      concerns: [
        "No direct PM/PO title experience",
        "Missing formal product management skills",
        "Would be career transition"
      ],
      seniorityMatch: "under-qualified"
    }
  ],

  // Summary with new features highlighted
  summary: {
    bestMatch: {
      jobId: "demo-ai-engineer",
      jobTitle: "AI Engineer - LatAm Fintech",
      score: 88,
      reason: "Strong AI/LLM skills match, appropriate seniority level, PJ contract preference"
    },
    keyStrengths: [
      "Expert-level LangChain and RAG skills",
      "Diverse automation toolkit (n8n, Make, Zapier)",
      "Strong Python and FastAPI experience",
      "Vector database expertise",
      "Leadership and mentoring experience"
    ],
    areasToImprove: [
      "Gain CrewAI or AutoGen experience for multi-agent systems",
      "Add fine-tuning experience to LLM skills",
      "Consider PM skills for career growth"
    ],
    marketInsights: [
      "AI/LLM skills are in high demand in Brazilian market",
      "PJ contracts common for senior tech roles in Brazil",
      "n8n/Make expertise valuable for automation roles",
      "Layoff context from Meta/Nubank understood by recruiters"
    ]
  }
};

// =============================================================================
// ADDITIONAL DEMO PROFILES - For showcasing different role types
// =============================================================================

export const DEMO_PROFILES = {
  // Designer profile for design role matching
  designer: {
    resume: `MARIA SANTOS
Senior UX Designer

Portfolio: behance.net/mariasantos | dribbble.com/mariasantos
Contact: maria@design.com | Sao Paulo, SP

EXPERIENCIA

Design Lead | Design Agency | 2021 - Present
- Led design system architecture for enterprise clients
- Managed team of 4 designers
- Conducted user research with 200+ participants
- Implemented accessibility audits (WCAG 2.1 AA)

Product Designer | Startup Inc | 2019 - 2021
- Created wireframes and prototypes in Figma
- Led usability testing sessions
- Developed design tokens system

HABILIDADES
- Design Systems, Figma, User Research, Prototyping
- Accessibility (WCAG), Design Tokens, Usability Testing
- Information Architecture, Interaction Design`,
    expectedRoleType: "design",
    expectedScore: 92
  },

  // Product manager profile
  productManager: {
    resume: `CARLOS OLIVEIRA
Product Manager

EXPERIENCIA

Senior PM | Tech Corp | 2020 - Present
- Defined product roadmap for 3 product lines
- Managed stakeholder relationships with C-level
- Led cross-functional team of 15
- Drove 40% increase in user engagement

Product Owner | Fintech | 2018 - 2020
- Managed backlog and sprint planning
- Conducted user interviews and analysis
- Defined OKRs and tracked metrics

HABILIDADES
- Product Strategy, Roadmap Planning, Stakeholder Management
- Agile/Scrum, User Research, Data Analysis, OKRs`,
    expectedRoleType: "product",
    expectedScore: 85
  }
};
