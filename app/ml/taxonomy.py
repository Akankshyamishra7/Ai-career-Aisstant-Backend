from typing import Dict, List, Any

# Standardized 12 authoritative technology job roles with core & recommended skills
JOB_ROLES_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "Data Analyst": {
        "description": "Analyzes raw data, builds executive dashboards, extracts business intelligence, and communicates data insights to stakeholders.",
        "core_skills": ["SQL", "Python", "Excel", "Power BI", "Tableau", "Statistics", "Data Visualization", "Pandas"],
        "recommended_skills": ["R", "NumPy", "Data Warehousing", "ETL", "A/B Testing", "Snowflake", "BigQuery"],
        "salary_range": "$70k - $105k",
        "market_demand": "Very High"
    },
    "Machine Learning Engineer": {
        "description": "Designs, trains, tests, and deploys scalable machine learning pipelines and models into production systems.",
        "core_skills": ["Python", "Scikit-learn", "Machine Learning", "PyTorch", "TensorFlow", "Pandas", "NumPy", "Docker", "Git"],
        "recommended_skills": ["MLOps", "Deep Learning", "FastAPI", "Kubernetes", "AWS", "MLflow", "Data Structures", "SQL"],
        "salary_range": "$120k - $180k",
        "market_demand": "High Growth"
    },
    "Data Scientist": {
        "description": "Applies statistical modeling, experimental design, hypothesis testing, and machine learning to solve strategic business challenges.",
        "core_skills": ["Python", "R", "SQL", "Statistics", "Machine Learning", "Data Analysis", "Pandas", "Scikit-learn", "Data Visualization"],
        "recommended_skills": ["Hypothesis Testing", "Deep Learning", "Spark", "NLP", "Feature Engineering", "Storytelling", "Tableau"],
        "salary_range": "$115k - $165k",
        "market_demand": "High"
    },
    "Frontend Developer": {
        "description": "Develops responsive, accessible, high-performance web user interfaces using modern client-side frameworks.",
        "core_skills": ["JavaScript", "TypeScript", "React", "HTML5", "CSS3", "Tailwind CSS", "Git", "Responsive Design"],
        "recommended_skills": ["Next.js", "Redux", "REST APIs", "GraphQL", "Jest", "Webpack", "UI/UX Design", "Performance Optimization"],
        "salary_range": "$80k - $130k",
        "market_demand": "Very High"
    },
    "Backend Developer": {
        "description": "Architects server-side logic, high-throughput APIs, database schemas, message queues, and microservices.",
        "core_skills": ["Python", "FastAPI", "Node.js", "Express", "PostgreSQL", "SQL", "REST APIs", "Docker", "Git"],
        "recommended_skills": ["MongoDB", "Redis", "Microservices", "System Design", "AWS", "CI/CD", "GraphQL", "Linux", "Kafka"],
        "salary_range": "$90k - $145k",
        "market_demand": "High"
    },
    "Full Stack Developer": {
        "description": "Bridges client-side and server-side engineering to deliver end-to-end scalable web applications.",
        "core_skills": ["JavaScript", "TypeScript", "React", "Node.js", "SQL", "HTML5", "CSS3", "Git", "REST APIs"],
        "recommended_skills": ["Next.js", "PostgreSQL", "MongoDB", "Docker", "Tailwind CSS", "CI/CD", "System Design", "Redis"],
        "salary_range": "$95k - $155k",
        "market_demand": "Very High"
    },
    "DevOps / Cloud Engineer": {
        "description": "Automates cloud infrastructure, build/deploy pipelines, container orchestration, monitoring, and system reliability.",
        "core_skills": ["Docker", "Kubernetes", "Linux", "AWS", "CI/CD", "Terraform", "Git", "Bash", "Python"],
        "recommended_skills": ["GitHub Actions", "Azure", "GCP", "Prometheus", "Grafana", "Ansible", "Helm", "Security"],
        "salary_range": "$110k - $170k",
        "market_demand": "High Growth"
    },
    "Mobile App Developer": {
        "description": "Constructs cross-platform or native mobile applications for iOS and Android ecosystems with smooth user experiences.",
        "core_skills": ["React Native", "Flutter", "JavaScript", "TypeScript", "Mobile UI", "Git", "REST APIs"],
        "recommended_skills": ["Swift", "Kotlin", "iOS", "Android", "Firebase", "App Store Deployment", "Redux", "Dart"],
        "salary_range": "$85k - $140k",
        "market_demand": "High"
    },
    "Cybersecurity Analyst": {
        "description": "Protects enterprise systems, conducts vulnerability assessments, investigates security incidents, and enforces protocols.",
        "core_skills": ["Network Security", "Linux", "SIEM", "Penetration Testing", "Python", "Vulnerability Assessment", "Wireshark"],
        "recommended_skills": ["Incident Response", "Ethical Hacking", "OWASP", "Cryptography", "Firewalls", "Cloud Security", "SOC"],
        "salary_range": "$88k - $140k",
        "market_demand": "High"
    },
    "AI / NLP Engineer": {
        "description": "Specializes in Large Language Models (LLMs), Generative AI, natural language processing, vector retrieval, and RAG pipelines.",
        "core_skills": ["Python", "NLP", "Machine Learning", "PyTorch", "Transformers", "Deep Learning", "LangChain", "Vector Databases"],
        "recommended_skills": ["Hugging Face", "RAG", "FastAPI", "Prompt Engineering", "Fine-Tuning", "Docker", "LLMs"],
        "salary_range": "$130k - $195k",
        "market_demand": "Explosive"
    },
    "Cloud Solutions Architect": {
        "description": "Defines enterprise cloud migration roadmaps, multi-region architecture, high availability, cost optimization, and microservice governance.",
        "core_skills": ["AWS", "Cloud Architecture", "System Design", "Kubernetes", "Docker", "Terraform", "Microservices", "Linux"],
        "recommended_skills": ["Azure", "GCP", "Networking", "Security", "Cost Optimization", "CI/CD", "Disaster Recovery", "Kafka"],
        "salary_range": "$140k - $210k",
        "market_demand": "Very High"
    },
    "QA & Test Automation Engineer": {
        "description": "Guarantees software quality through automated end-to-end test suites, performance benchmarking, and continuous testing pipelines.",
        "core_skills": ["Selenium", "Python", "Test Automation", "Jest", "Git", "API Testing", "Postman", "Cypress"],
        "recommended_skills": ["Playwright", "CI/CD", "Docker", "Performance Testing", "JMeter", "SQL", "Jira", "Cucumber"],
        "salary_range": "$75k - $125k",
        "market_demand": "High"
    }
}

# 180+ unique canonical technical skills mapped from aliases and common names
SKILL_ALIASES: Dict[str, str] = {
    # Programming Languages
    "py": "Python", "python": "Python", "python3": "Python",
    "js": "JavaScript", "javascript": "JavaScript", "es6": "JavaScript", "ecmascript": "JavaScript",
    "ts": "TypeScript", "typescript": "TypeScript",
    "java": "Java", "java8": "Java", "java17": "Java",
    "c++": "C++", "cpp": "C++",
    "c#": "C#", "csharp": "C#",
    ".net": ".NET", "dotnet": ".NET", "asp.net": ".NET",
    "go": "Go", "golang": "Go",
    "rust": "Rust",
    "r": "R", "r-lang": "R",
    "ruby": "Ruby", "rails": "Ruby on Rails", "ruby on rails": "Ruby on Rails",
    "php": "PHP", "laravel": "Laravel",
    "swift": "Swift", "swiftui": "Swift",
    "kotlin": "Kotlin",
    "dart": "Dart",
    "scala": "Scala",
    "bash": "Bash", "shell": "Bash", "powershell": "PowerShell",
    "sql": "SQL", "plsql": "PL/SQL", "t-sql": "T-SQL",

    # Data Science & Machine Learning
    "scikit-learn": "Scikit-learn", "scikit learn": "Scikit-learn", "scikit": "Scikit-learn", "sklearn": "Scikit-learn",
    "tensorflow": "TensorFlow", "tf": "TensorFlow", "keras": "Keras",
    "pytorch": "PyTorch", "torch": "PyTorch",
    "pandas": "Pandas", "numpy": "NumPy", "scipy": "SciPy",
    "matplotlib": "Matplotlib", "seaborn": "Seaborn", "plotly": "Plotly",
    "machine learning": "Machine Learning", "ml": "Machine Learning", "machine-learning": "Machine Learning",
    "deep learning": "Deep Learning", "dl": "Deep Learning",
    "statistics": "Statistics", "statistical analysis": "Statistics", "stats": "Statistics",
    "data analysis": "Data Analysis", "data analytics": "Data Analysis",
    "data science": "Data Science",
    "data visualization": "Data Visualization", "dataviz": "Data Visualization",
    "feature engineering": "Feature Engineering", "hypothesis testing": "Hypothesis Testing", "a/b testing": "A/B Testing",
    "xgboost": "XGBoost", "lightgbm": "LightGBM", "catboost": "CatBoost",
    "mlops": "MLOps", "mlflow": "MLflow", "kubeflow": "Kubeflow", "dvc": "DVC", "weights & biases": "WandB",

    # Generative AI & NLP
    "nlp": "NLP", "natural language processing": "NLP",
    "artificial intelligence": "Artificial Intelligence", "ai": "Artificial Intelligence",
    "generative ai": "Generative AI", "genai": "Generative AI",
    "llm": "LLMs", "llms": "LLMs", "large language models": "LLMs",
    "rag": "RAG", "retrieval augmented generation": "RAG",
    "langchain": "LangChain", "llamaindex": "LlamaIndex",
    "transformers": "Transformers", "hugging face": "Hugging Face", "huggingface": "Hugging Face",
    "prompt engineering": "Prompt Engineering", "fine-tuning": "Fine-Tuning",
    "vector databases": "Vector Databases", "vector database": "Vector Databases", "chromadb": "ChromaDB", "pinecone": "Pinecone", "weaviate": "Weaviate", "qdrant": "Qdrant",
    "openai": "OpenAI API", "gemini": "Google Gemini",

    # Business Intelligence & Big Data
    "power bi": "Power BI", "powerbi": "Power BI", "power-bi": "Power BI",
    "tableau": "Tableau",
    "excel": "Excel", "advanced excel": "Excel", "pivot tables": "Excel",
    "etl": "ETL", "data pipeline": "ETL", "data pipelines": "ETL",
    "spark": "Spark", "pyspark": "PySpark", "apache spark": "Spark",
    "hadoop": "Hadoop", "hive": "Hive", "kafka": "Kafka", "apache kafka": "Kafka",
    "airflow": "Apache Airflow", "apache airflow": "Apache Airflow",
    "snowflake": "Snowflake", "bigquery": "BigQuery", "google bigquery": "BigQuery", "redshift": "AWS Redshift",
    "data warehousing": "Data Warehousing", "data lake": "Data Lake", "dbt": "dbt",

    # Frontend Development
    "react": "React", "react.js": "React", "reactjs": "React",
    "next.js": "Next.js", "nextjs": "Next.js", "next": "Next.js",
    "vue": "Vue.js", "vue.js": "Vue.js", "vuejs": "Vue.js", "nuxt": "Nuxt.js",
    "angular": "Angular", "angularjs": "Angular",
    "svelte": "Svelte", "sveltekit": "SvelteKit",
    "html": "HTML5", "html5": "HTML5",
    "css": "CSS3", "css3": "CSS3",
    "tailwind": "Tailwind CSS", "tailwindcss": "Tailwind CSS",
    "bootstrap": "Bootstrap", "material ui": "Material UI", "mui": "Material UI", "shadcn": "Shadcn UI",
    "redux": "Redux", "redux toolkit": "Redux", "zustand": "Zustand", "mobx": "MobX",
    "webpack": "Webpack", "vite": "Vite",
    "responsive design": "Responsive Design", "mobile responsive": "Responsive Design",
    "ui/ux design": "UI/UX Design", "figma": "Figma",

    # Backend Development
    "node": "Node.js", "nodejs": "Node.js", "node.js": "Node.js",
    "express": "Express", "expressjs": "Express", "express.js": "Express",
    "nestjs": "NestJS", "nest.js": "NestJS",
    "fastapi": "FastAPI",
    "django": "Django", "django rest framework": "Django", "drf": "Django",
    "flask": "Flask",
    "spring": "Spring Boot", "springboot": "Spring Boot", "spring framework": "Spring Boot",
    "rest": "REST APIs", "rest api": "REST APIs", "rest apis": "REST APIs", "restful": "REST APIs", "restful apis": "REST APIs",
    "graphql": "GraphQL", "apollo": "Apollo GraphQL", "grpc": "gRPC", "websockets": "WebSockets", "socket.io": "WebSockets",
    "microservices": "Microservices", "microservice": "Microservices",
    "system design": "System Design", "system architecture": "System Design", "high availability": "System Design", "scalability": "System Design",

    # Databases & Caching
    "postgresql": "PostgreSQL", "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "sqlite": "SQLite",
    "mongodb": "MongoDB", "mongo": "MongoDB",
    "redis": "Redis",
    "elasticsearch": "Elasticsearch",
    "cassandra": "Cassandra", "dynamodb": "DynamoDB",
    "prisma": "Prisma", "sqlalchemy": "SQLAlchemy", "typeorm": "TypeORM", "hibernate": "Hibernate",
    "supabase": "Supabase", "firebase": "Firebase",

    # Cloud & DevOps
    "docker": "Docker", "containerization": "Docker", "containers": "Docker",
    "kubernetes": "Kubernetes", "k8s": "Kubernetes", "helm": "Helm",
    "aws": "AWS", "amazon web services": "AWS",
    "azure": "Azure", "microsoft azure": "Azure",
    "gcp": "GCP", "google cloud": "GCP", "google cloud platform": "GCP",
    "cloud computing": "Cloud Computing", "cloud architecture": "Cloud Architecture",
    "terraform": "Terraform", "infrastructure as code": "Terraform", "iac": "Terraform",
    "ansible": "Ansible",
    "ci/cd": "CI/CD", "cicd": "CI/CD", "continuous integration": "CI/CD",
    "github actions": "GitHub Actions", "jenkins": "Jenkins", "gitlab ci": "GitLab CI",
    "linux": "Linux", "ubuntu": "Linux", "unix": "Linux",
    "prometheus": "Prometheus", "grafana": "Grafana", "datadog": "Datadog", "elk stack": "ELK Stack",
    "git": "Git", "github": "Git", "gitlab": "GitLab", "bitbucket": "Bitbucket",

    # Testing & QA
    "selenium": "Selenium", "selenium webdriver": "Selenium",
    "cypress": "Cypress",
    "playwright": "Playwright",
    "jest": "Jest", "mocha": "Mocha", "pytest": "PyTest", "junit": "JUnit",
    "postman": "Postman", "api testing": "API Testing",
    "test automation": "Test Automation", "qa": "Quality Assurance", "quality assurance": "Quality Assurance",
    "performance testing": "Performance Testing", "jmeter": "JMeter", "locust": "Locust",
    "cucumber": "Cucumber", "bdd": "Cucumber",

    # Cybersecurity
    "cybersecurity": "Cybersecurity", "infosec": "Cybersecurity", "information security": "Cybersecurity",
    "network security": "Network Security",
    "penetration testing": "Penetration Testing", "pentesting": "Penetration Testing",
    "ethical hacking": "Ethical Hacking",
    "siem": "SIEM", "splunk": "Splunk",
    "wireshark": "Wireshark",
    "owasp": "OWASP", "owasp top 10": "OWASP",
    "vulnerability assessment": "Vulnerability Assessment",
    "cryptography": "Cryptography", "ssl/tls": "Cryptography",
    "firewalls": "Firewalls", "incident response": "Incident Response", "soc": "SOC",

    # Mobile Development
    "react native": "React Native", "react-native": "React Native",
    "flutter": "Flutter",
    "android": "Android", "android development": "Android",
    "ios": "iOS", "ios development": "iOS",
    "mobile ui": "Mobile UI", "app store deployment": "App Store Deployment",

    # Agile & Methodologies
    "agile": "Agile", "scrum": "Scrum", "kanban": "Kanban",
    "jira": "Jira", "confluence": "Confluence",
    "leadership": "Leadership", "teamwork": "Teamwork",
    "communication": "Communication", "problem solving": "Problem Solving",
    "storytelling": "Storytelling"
}

# Categorization lookup for clean visual badges
SKILL_CATEGORIES: Dict[str, str] = {
    # Programming Languages
    "Python": "Programming Languages", "JavaScript": "Programming Languages", "TypeScript": "Programming Languages",
    "Java": "Programming Languages", "C++": "Programming Languages", "C#": "Programming Languages",
    ".NET": "Programming Languages", "Go": "Programming Languages", "Rust": "Programming Languages",
    "R": "Programming Languages", "Ruby": "Programming Languages", "Ruby on Rails": "Frameworks",
    "PHP": "Programming Languages", "Laravel": "Frameworks", "Swift": "Programming Languages",
    "Kotlin": "Programming Languages", "Dart": "Programming Languages", "Scala": "Programming Languages",
    "Bash": "System & Scripting", "PowerShell": "System & Scripting", "SQL": "Database & Query",
    "PL/SQL": "Database & Query", "T-SQL": "Database & Query",

    # Data & ML
    "Pandas": "Data Science & Analytics", "NumPy": "Data Science & Analytics", "SciPy": "Data Science & Analytics",
    "Matplotlib": "Data Visualization", "Seaborn": "Data Visualization", "Plotly": "Data Visualization",
    "Scikit-learn": "Machine Learning", "TensorFlow": "Deep Learning", "Keras": "Deep Learning",
    "PyTorch": "Deep Learning", "Machine Learning": "Machine Learning", "Deep Learning": "Machine Learning",
    "Statistics": "Mathematics & Statistics", "Data Analysis": "Data Science & Analytics",
    "Data Science": "Data Science & Analytics", "Data Visualization": "Data Visualization",
    "Feature Engineering": "Machine Learning", "Hypothesis Testing": "Mathematics & Statistics",
    "A/B Testing": "Data Science & Analytics", "XGBoost": "Machine Learning", "LightGBM": "Machine Learning",
    "CatBoost": "Machine Learning", "MLOps": "Machine Learning", "MLflow": "Machine Learning",
    "Kubeflow": "Machine Learning", "DVC": "Machine Learning", "WandB": "Machine Learning",

    # Generative AI & NLP
    "NLP": "AI & Language Models", "Artificial Intelligence": "AI & Language Models",
    "Generative AI": "AI & Language Models", "LLMs": "AI & Language Models", "RAG": "AI & Language Models",
    "LangChain": "AI & Language Models", "LlamaIndex": "AI & Language Models", "Transformers": "AI & Language Models",
    "Hugging Face": "AI & Language Models", "Prompt Engineering": "AI & Language Models", "Fine-Tuning": "AI & Language Models",
    "Vector Databases": "AI & Language Models", "ChromaDB": "AI & Language Models", "Pinecone": "AI & Language Models",
    "Weaviate": "AI & Language Models", "Qdrant": "AI & Language Models", "OpenAI API": "AI & Language Models",
    "Google Gemini": "AI & Language Models",

    # BI & Big Data
    "Power BI": "Business Intelligence", "Tableau": "Business Intelligence", "Excel": "Business Intelligence",
    "ETL": "Data Engineering", "Spark": "Big Data & Distributed", "PySpark": "Big Data & Distributed",
    "Hadoop": "Big Data & Distributed", "Hive": "Big Data & Distributed", "Kafka": "Event Streaming",
    "Apache Airflow": "Data Engineering", "Snowflake": "Data Warehousing", "BigQuery": "Data Warehousing",
    "AWS Redshift": "Data Warehousing", "Data Warehousing": "Data Warehousing", "Data Lake": "Data Warehousing",
    "dbt": "Data Engineering",

    # Frontend
    "React": "Frontend Frameworks", "Next.js": "Frontend Frameworks", "Vue.js": "Frontend Frameworks",
    "Nuxt.js": "Frontend Frameworks", "Angular": "Frontend Frameworks", "Svelte": "Frontend Frameworks",
    "SvelteKit": "Frontend Frameworks", "HTML5": "Frontend Core", "CSS3": "Frontend Core",
    "Tailwind CSS": "Frontend Styling", "Bootstrap": "Frontend Styling", "Material UI": "Frontend Styling",
    "Shadcn UI": "Frontend Styling", "Redux": "State Management", "Zustand": "State Management",
    "MobX": "State Management", "Webpack": "Frontend Tooling", "Vite": "Frontend Tooling",
    "Responsive Design": "UI & Styling", "UI/UX Design": "Design & UI", "Figma": "Design & UI",

    # Backend
    "Node.js": "Backend Runtime", "Express": "Backend Frameworks", "NestJS": "Backend Frameworks",
    "FastAPI": "Backend Frameworks", "Django": "Backend Frameworks", "Flask": "Backend Frameworks",
    "Spring Boot": "Backend Frameworks", "REST APIs": "API & Networking", "GraphQL": "API & Networking",
    "Apollo GraphQL": "API & Networking", "gRPC": "API & Networking", "WebSockets": "API & Networking",
    "Microservices": "Architecture & Systems", "System Design": "Architecture & Systems",

    # Databases
    "PostgreSQL": "Databases (SQL)", "MySQL": "Databases (SQL)", "SQLite": "Databases (SQL)",
    "MongoDB": "Databases (NoSQL)", "Redis": "In-Memory & Cache", "Elasticsearch": "Search & Analytics",
    "Cassandra": "Databases (NoSQL)", "DynamoDB": "Databases (NoSQL)", "Prisma": "ORM & Database Tools",
    "SQLAlchemy": "ORM & Database Tools", "TypeORM": "ORM & Database Tools", "Hibernate": "ORM & Database Tools",
    "Supabase": "Backend-as-a-Service", "Firebase": "Backend-as-a-Service",

    # DevOps & Cloud
    "Docker": "Containers & Virtualization", "Kubernetes": "Containers & Orchestration", "Helm": "Containers & Orchestration",
    "AWS": "Cloud Platforms", "Azure": "Cloud Platforms", "GCP": "Cloud Platforms",
    "Cloud Computing": "Cloud Platforms", "Cloud Architecture": "Architecture & Systems",
    "Terraform": "Infrastructure as Code", "Ansible": "Configuration Management",
    "CI/CD": "DevOps & Automation", "GitHub Actions": "DevOps & Automation", "Jenkins": "DevOps & Automation",
    "GitLab CI": "DevOps & Automation", "Linux": "Operating Systems", "Prometheus": "Monitoring & Observability",
    "Grafana": "Monitoring & Observability", "Datadog": "Monitoring & Observability", "ELK Stack": "Monitoring & Observability",
    "Git": "Version Control", "GitLab": "Version Control", "Bitbucket": "Version Control",

    # Testing & QA
    "Selenium": "Test Automation", "Cypress": "Test Automation", "Playwright": "Test Automation",
    "Jest": "Unit Testing", "Mocha": "Unit Testing", "PyTest": "Unit Testing", "JUnit": "Unit Testing",
    "Postman": "API Testing", "API Testing": "Testing & QA", "Test Automation": "Testing & QA",
    "Quality Assurance": "Testing & QA", "Performance Testing": "Testing & QA", "JMeter": "Testing & QA",
    "Locust": "Testing & QA", "Cucumber": "BDD & Testing",

    # Cybersecurity
    "Cybersecurity": "Security", "Network Security": "Security", "Penetration Testing": "Security",
    "Ethical Hacking": "Security", "SIEM": "Security", "Splunk": "Security", "Wireshark": "Security",
    "OWASP": "Security", "Vulnerability Assessment": "Security", "Cryptography": "Security",
    "Firewalls": "Security", "Incident Response": "Security", "SOC": "Security",

    # Mobile
    "React Native": "Mobile Development", "Flutter": "Mobile Development", "Android": "Mobile Development",
    "iOS": "Mobile Development", "Mobile UI": "Mobile Development", "App Store Deployment": "Mobile Development",

    # Methodology & Soft Skills
    "Agile": "Methodology", "Scrum": "Methodology", "Kanban": "Methodology", "Jira": "Project Management",
    "Confluence": "Project Management", "Leadership": "Soft Skills", "Teamwork": "Soft Skills",
    "Communication": "Soft Skills", "Problem Solving": "Soft Skills", "Storytelling": "Soft Skills"
}
