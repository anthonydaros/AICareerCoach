# Skill Relationships Knowledge Base

## Skill Inference Database

When a candidate lists a skill, they likely also have experience with related technologies:

### Programming Languages

| If They Know | They Likely Know |
|--------------|------------------|
| Python | pip, virtualenv, pytest, type hints |
| Python (Data) | pandas, numpy, jupyter, matplotlib |
| Python (ML) | tensorflow, pytorch, scikit-learn, keras |
| Python (Web) | django, flask, fastapi, sqlalchemy |
| JavaScript | npm, node.js, html, css |
| TypeScript | javascript, node.js, type safety |
| Java | maven, gradle, spring, jvm |
| Go | goroutines, channels, go modules |
| Rust | cargo, ownership, memory safety |
| C++ | pointers, memory management, stl |

### Frontend Frameworks

| If They Know | They Likely Know |
|--------------|------------------|
| React | jsx, hooks, redux, react-router |
| Vue | vuex, vue-router, composition api |
| Angular | rxjs, typescript, dependency injection |
| Next.js | react, ssr, api routes, vercel |
| Svelte | svelte-kit, reactivity |

### Backend & APIs

| If They Know | They Likely Know |
|--------------|------------------|
| Django | python, orm, admin, rest framework |
| Flask | python, jinja2, blueprints |
| FastAPI | python, pydantic, async, openapi |
| Spring Boot | java, maven, hibernate, jpa |
| Node.js | npm, express, javascript |
| GraphQL | apollo, schema design, resolvers |
| REST API | http methods, status codes, json |

### Cloud Platforms

| If They Know | They Likely Know |
|--------------|------------------|
| AWS | ec2, s3, lambda, iam, cloudformation |
| Azure | azure functions, blob storage, ad |
| GCP | compute engine, cloud storage, bigquery |
| Docker | containers, dockerfile, compose |
| Kubernetes | pods, services, deployments, helm |
| Terraform | infrastructure as code, hcl, modules |

### Databases

| If They Know | They Likely Know |
|--------------|------------------|
| PostgreSQL | sql, acid, indexing, constraints |
| MySQL | sql, replication, innodb |
| MongoDB | nosql, document stores, aggregation |
| Redis | caching, pub/sub, data structures |
| Elasticsearch | search, indexing, kibana |
| Kafka | streaming, pub/sub, partitions |

### Data Engineering

| If They Know | They Likely Know |
|--------------|------------------|
| Spark | distributed computing, dataframes, scala/python |
| Airflow | dag, scheduling, operators |
| dbt | sql, data modeling, testing |
| Snowflake | data warehouse, sql, cloud |
| BigQuery | sql, gcp, analytics |

### DevOps & CI/CD

| If They Know | They Likely Know |
|--------------|------------------|
| GitHub Actions | yaml, workflows, ci/cd |
| Jenkins | pipelines, groovy, plugins |
| GitLab CI | yaml, runners, pipelines |
| ArgoCD | kubernetes, gitops, helm |
| Prometheus | metrics, alerting, grafana |

## Skill Aliases

Common abbreviations and alternate names:

| Alias | Canonical Name |
|-------|---------------|
| k8s | kubernetes |
| k8 | kubernetes |
| js | javascript |
| ts | typescript |
| py | python |
| rb | ruby |
| pg | postgresql |
| postgres | postgresql |
| mongo | mongodb |
| es | elasticsearch |
| tf | terraform |
| gh | github |
| gha | github actions |
| rds | aws rds |
| ec2 | aws ec2 |
| s3 | aws s3 |
| gke | google kubernetes engine |
| eks | amazon elastic kubernetes service |
| aks | azure kubernetes service |
| ml | machine learning |
| ai | artificial intelligence |
| nlp | natural language processing |
| cv | computer vision |
| llm | large language model |
| rag | retrieval augmented generation |
| ci | continuous integration |
| cd | continuous deployment |
| tdd | test driven development |
| bdd | behavior driven development |
| oop | object oriented programming |
| fp | functional programming |
| api | application programming interface |
| sdk | software development kit |
| cli | command line interface |
| ui | user interface |
| ux | user experience |

## Skill Categories

### Languages
python, java, javascript, typescript, go, rust, c++, c, ruby, php, swift, kotlin, scala, r, sql, bash, powershell

### Cloud
aws, azure, gcp, digitalocean, heroku, vercel, netlify, cloudflare

### Data
postgresql, mysql, mongodb, redis, elasticsearch, cassandra, dynamodb, snowflake, bigquery, redshift

### DevOps
docker, kubernetes, terraform, ansible, jenkins, github actions, gitlab ci, circleci, argocd

### Design
figma, sketch, adobe xd, invision, photoshop, illustrator, css, tailwind, bootstrap

### Product
jira, confluence, notion, asana, trello, linear, productboard, amplitude, mixpanel

### QA
selenium, cypress, jest, mocha, pytest, junit, postman, k6, locust

## Match Calculation Logic

### Direct Match
```
resume_skill == job_requirement → 100% match
```

### Alias Match
```
resolve_alias(resume_skill) == job_requirement → 100% match
```

### Inferred Match
```
skill ∈ inferred_skills(resume_skill) → 80% match
```

### Category Match
```
same_category(resume_skill, job_requirement) → 50% match
```

## Example: Skill Expansion

**Resume states:** "Python, AWS, PostgreSQL"

**Expanded skill profile:**
```
Python:
  - Core: pip, virtualenv, pytest
  - Possible: django OR flask OR fastapi
  - Possible: pandas, numpy (if data-related)

AWS:
  - Core: ec2, s3, iam
  - Possible: lambda, cloudformation, rds

PostgreSQL:
  - Core: sql, indexing, transactions
  - Related: database design, data modeling
```

## Transferable Skills Matrix

| From Skill | Transferable To | Strength |
|------------|-----------------|----------|
| Java | Kotlin, Scala | High |
| JavaScript | TypeScript | High |
| React | React Native | High |
| Python | Data Science | Medium |
| SQL | NoSQL concepts | Medium |
| AWS | Azure, GCP | Medium |
| Docker | Kubernetes | Medium |
| REST | GraphQL | Medium |
| Agile | Scrum, Kanban | High |
