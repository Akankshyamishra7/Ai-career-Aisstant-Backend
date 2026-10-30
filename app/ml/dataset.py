import random
import pandas as pd
from typing import List, Tuple
from app.ml.taxonomy import JOB_ROLES_TAXONOMY

ROLE_TEMPLATES = {
    "Data Analyst": [
        "Skilled in SQL queries, creating interactive Power BI and Tableau dashboards. Handled data cleaning and ETL with Python and Pandas. Experienced in statistical analysis, business metrics, and Excel pivot tables.",
        "Data Analyst with 3 years of experience in data visualization using Tableau, writing complex SQL queries, building executive reports, and conducting A/B test analysis in Excel and Python.",
        "Experienced in SQL database querying, Snowflake data warehouse, creating automated reporting dashboards with Power BI, data warehousing, and business intelligence KPIs.",
        "Data Analyst proficient in Python data wrangling, Pandas, NumPy, statistical hypothesis testing, SQL joins, Tableau reports, and presenting data insights to stakeholders.",
        "Built financial dashboards in Excel and Power BI, optimized SQL database queries, performed regression analysis in R and Python, and streamlined monthly reporting workflows."
    ],
    "Machine Learning Engineer": [
        "Designed and deployed machine learning pipelines using Python, Scikit-learn, PyTorch, and Docker. Implemented automated model retraining and monitoring with MLflow and FastAPI.",
        "Machine Learning Engineer specializing in predictive modeling, deep learning architectures, feature engineering with Pandas and NumPy, model containerization using Docker, and cloud deployment.",
        "Built recommendation systems and gradient boosting models using Scikit-learn, XGBoost, and PyTorch. Deployed inference REST APIs using FastAPI and Kubernetes.",
        "Expert in Python, Scikit-learn algorithms (Random Forest, SVM, Gradient Boosting), model validation, hyperparameter tuning, MLOps, Docker, and AWS SageMaker.",
        "Applied ML Engineer with strong skills in Python, PyTorch, TensorFlow, data structures, algorithm optimization, distributed training, and production inference deployment."
    ],
    "Data Scientist": [
        "Data Scientist with deep expertise in statistical modeling, Python, R, machine learning algorithms, hypothesis testing, and exploratory data analysis using Pandas and Seaborn.",
        "Passionate about leveraging data science to solve customer churn. Built predictive models using Scikit-learn, conducted A/B testing, and communicated findings via interactive notebooks.",
        "Strong foundation in mathematics, probability, statistics, Python, SQL, NLP, and machine learning. Designed causal inference experiments and customer segmentation clusters.",
        "Analyzed large datasets using Python, PySpark, and SQL. Developed classification and regression models, performed feature selection, and built predictive analytics pipelines.",
        "Data Scientist skilled in experimental design, statistical inference, Bayesian modeling, Python, Scikit-learn, and synthesizing complex findings for executive leadership."
    ],
    "Frontend Developer": [
        "Frontend Engineer proficient in React, Next.js, TypeScript, and modern CSS with Tailwind CSS. Experienced in building responsive web applications with state management using Redux.",
        "UI Developer with a passion for sleek user experiences. Expert in JavaScript ES6+, TypeScript, React hooks, HTML5 semantics, Tailwind CSS, and web accessibility standards.",
        "Developed responsive Single Page Applications (SPAs) using React, Next.js, TypeScript, REST APIs, and Jest for unit testing. Optimized Core Web Vitals and load performance.",
        "Frontend Developer skilled in HTML5, CSS3, JavaScript, React components, Tailwind CSS styling, responsive design across mobile/desktop, and integrating GraphQL endpoints.",
        "Specialized in client-side architecture using TypeScript, Next.js, Redux Toolkit, component libraries, CSS Grid/Flexbox, and building modular interactive dashboards."
    ],
    "Backend Developer": [
        "Backend Developer experienced in building scalable RESTful APIs with Python, FastAPI, and Node.js. Designed relational schemas in PostgreSQL and managed caching with Redis.",
        "Server-side engineer with expertise in microservices architecture, Python, Django, FastAPI, Docker containerization, SQL query optimization, and secure JWT authentication.",
        "Built high-throughput backend services using Node.js, Express, PostgreSQL, and Redis. Implemented async message queues and integrated third-party payment gateways.",
        "Backend Engineer with focus on system design, database indexing, REST APIs, Python, FastAPI, Docker, automated CI/CD pipelines, and cloud database migrations.",
        "Experienced in Java, Spring Boot, PostgreSQL, building reliable distributed microservices, message brokers, and implementing robust error handling and API documentation."
    ],
    "Full Stack Developer": [
        "Full Stack Developer building end-to-end web applications with React, Next.js, Node.js, Express, and PostgreSQL. Experienced in Docker, Tailwind CSS, and REST APIs.",
        "Versatile engineer skilled in TypeScript across the stack. Developed modern UI in React/Next.js and scalable server endpoints in Node.js with MongoDB and PostgreSQL databases.",
        "Full Stack Engineer proficient in JavaScript, TypeScript, React, Python FastAPI, PostgreSQL, HTML5, Tailwind CSS, Git workflows, and cloud deployments.",
        "Built responsive SaaS platforms from scratch using Next.js frontend, Node.js backend, RESTful APIs, Tailwind CSS, SQL databases, and automated testing.",
        "Experienced Full Stack Web Developer knowledgeable in frontend UI components, backend business logic, database migrations, CI/CD, and Dockerized deployments."
    ],
    "DevOps / Cloud Engineer": [
        "DevOps Engineer with extensive background in AWS cloud infrastructure, Kubernetes cluster orchestration, Docker containerization, and Terraform Infrastructure as Code (IaC).",
        "Cloud Engineer automating deployment pipelines using GitHub Actions, CI/CD, Docker, Kubernetes, Linux system administration, Bash scripting, and Prometheus monitoring.",
        "Designed resilient multi-region infrastructure on AWS and GCP using Terraform. Managed container deployments with Docker, Helm, Kubernetes, and monitored SLAs using Grafana.",
        "Site Reliability Engineer (SRE) specializing in Linux environments, CI/CD pipeline automation, Docker containers, Kubernetes, cloud security compliance, and log analysis.",
        "Automated provisioning and configuration management with Ansible and Terraform. Managed Kubernetes microservice clusters and implemented zero-downtime rolling updates."
    ],
    "Mobile App Developer": [
        "Mobile App Developer with strong skills in React Native and Flutter. Published multi-platform mobile apps to Google Play Store and Apple App Store.",
        "Developed cross-platform mobile user interfaces using Flutter, Dart, TypeScript, React Native, Firebase authentication, and offline data synchronization.",
        "Mobile Engineer proficient in React Native, Redux, mobile navigation, native modules integration, REST APIs, and optimizing app performance for iOS and Android.",
        "Created responsive, animated mobile apps with React Native, TypeScript, Tailwind/StyleSheet, local caching, push notifications, and Firebase backend integration.",
        "Experienced in iOS and Android app development using Flutter and React Native. Focused on smooth mobile 60fps UI animations, responsive layouts, and API integrations."
    ],
    "Cybersecurity Analyst": [
        "Cybersecurity Analyst skilled in network vulnerability scanning, Wireshark packet analysis, SIEM log monitoring, and implementing OWASP security standards.",
        "Information Security specialist with experience in penetration testing, Linux security hardening, incident response, firewalls, and vulnerability assessments.",
        "Conducted ethical hacking assessments, configured SIEM alerts, evaluated network security postures, and mitigated security risks across enterprise systems.",
        "Security Analyst knowledgeable in Python scripting for security automation, network protocols, Wireshark, intrusion detection systems, and regulatory compliance.",
        "Performed threat modeling, penetration testing against web applications, vulnerability management, and remediation of OWASP Top 10 security flaws."
    ],
    "AI / NLP Engineer": [
        "AI Engineer specializing in Large Language Models (LLMs), LangChain, Retrieval-Augmented Generation (RAG), vector databases, PyTorch, and Python prompt engineering.",
        "Built production generative AI applications using Hugging Face Transformers, fine-tuning open-source models, LangChain workflows, and ChromaDB vector search.",
        "NLP Engineer experienced in text classification, semantic search, embeddings, PyTorch, Python, FastAPI, and building conversational AI agents with RAG pipelines.",
        "Developed enterprise search solutions using OpenAI APIs, open-source LLMs, LangChain, vector similarity indexing, Python, and PyTorch deep learning models.",
        "Applied Generative AI researcher and engineer with expertise in prompt engineering, token optimization, model fine-tuning, Transformers, and deploying LLM microservices."
    ],
    "Cloud Solutions Architect": [
        "Cloud Solutions Architect with proven track record in AWS enterprise cloud migrations, multi-region high availability architectures, Terraform IaC, and Kubernetes orchestration.",
        "Enterprise Architect designing scalable microservice systems, serverless infrastructure on AWS and Azure, cost governance, security compliance, and event-driven architectures with Kafka.",
        "Architected fault-tolerant distributed cloud platforms, disaster recovery protocols, zero-trust cloud security, Docker container ecosystems, and automated CI/CD release strategies.",
        "Experienced Cloud Architect specializing in hybrid cloud connectivity, Kubernetes cluster design, microservice governance, API gateways, database partitioning, and cloud networking.",
        "Led cloud modernization programs, migrated legacy monolithic systems to AWS and GCP microservices, optimized cloud compute costs, and established robust SRE observability."
    ],
    "QA & Test Automation Engineer": [
        "QA Automation Engineer skilled in building end-to-end test automation frameworks using Selenium, Cypress, Playwright, Python, and JavaScript.",
        "Software Development Engineer in Test (SDET) experienced in API test automation with Postman and REST Assured, performance testing using JMeter, and CI/CD test gates.",
        "Designed comprehensive regression suites with Cypress and Selenium WebDriver. Integrated automated test executions into GitHub Actions and Jenkins pipelines.",
        "Test Automation Specialist proficient in Python, PyTest, Selenium, cross-browser validation, defect tracking in Jira, and behavioral-driven development (BDD) with Cucumber.",
        "Experienced in load and performance testing, automated contract testing for microservices, Jest unit testing, and ensuring 99%+ automated regression coverage."
    ]
}

def generate_training_data(samples_per_role: int = 65) -> pd.DataFrame:
    """
    Generates an augmented training dataset pairing diverse skill subsets and role descriptions
    with corresponding target job roles for classification model training across all 12 roles.
    """
    data: List[Tuple[str, str]] = []
    
    for role, info in JOB_ROLES_TAXONOMY.items():
        core_skills = info["core_skills"]
        rec_skills = info["recommended_skills"]
        templates = ROLE_TEMPLATES.get(role, [])
        all_role_skills = core_skills + rec_skills

        # 1. Add base templates
        for tmpl in templates:
            data.append((tmpl, role))

        # 2. Generate augmented variations with random skill subsets and phrasing
        for _ in range(samples_per_role):
            sampled_core = random.sample(core_skills, min(len(core_skills), random.randint(3, len(core_skills))))
            sampled_rec = random.sample(rec_skills, min(len(rec_skills), random.randint(1, len(rec_skills))))
            selected_skills = sampled_core + sampled_rec
            random.shuffle(selected_skills)

            phrasings = [
                f"Candidate experienced in {', '.join(selected_skills)}. Strong background in {selected_skills[0]} and {selected_skills[1]}. Looking for opportunities in tech.",
                f"Technical profile: {', '.join(selected_skills)}. Developed several applications and projects utilizing {selected_skills[0]} and {selected_skills[-1]}.",
                f"Summary: Dedicated professional with hands-on expertise in {', '.join(selected_skills[:4])}. Proven ability to deliver production solutions with {', '.join(selected_skills[2:])}.",
                f"Skills: {' | '.join(selected_skills)}. Experienced in collaborative engineering environments, version control, and continuous improvement.",
                f"Experience: Architected and implemented features leveraging {selected_skills[0]}, {selected_skills[1]}, and {selected_skills[2]}. Proficient with {', '.join(selected_skills)}."
            ]

            data.append((random.choice(phrasings), role))

    df = pd.DataFrame(data, columns=["text", "role"])
    return df
