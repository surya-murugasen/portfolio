"""
Curated Ground-Truth Knowledge Base for Surya M's Portfolio AI Assistant.
Contains ONLY verified information from active resumes, production codebases, and credentials.
Strictly distinguishes implemented features from planned work.
"""

PORTFOLIO_KNOWLEDGE = {
    "profile": {
        "name": "Surya M",
        "title": "Software Developer | Full-Stack & Systems Engineering",
        "location": "Tamil Nadu, India (Available for on-site in Coimbatore, Chennai, Bangalore, or remote)",
        "email": "suryamurugasen135@gmail.com",
        "phone": "+91 9092436936",
        "github": "https://github.com/surya-murugasen",
        "linkedin": "https://linkedin.com/in/surya-m-softwareservicedeveloper",
        "portfolio_url": "https://surya-murugasen-portfolio-5f4d33.netlify.app",
        "summary": (
            "Software Developer specializing in production-grade backend APIs, relational database design, "
            "and high-reliability client applications. Experienced in developing enterprise Manufacturing "
            "Execution System (MES) traceability workflows, real-time collaboration engines, and applied computer "
            "vision pipelines with Ultralytics YOLO & OpenCV."
        )
    },
    "technical_skills": {
        "languages": ["JavaScript (ES6+)", "TypeScript", "Python", "Dart", "Java", "SQL"],
        "backend": [
            "Node.js", "Express.js", "FastAPI (Python)", "RESTful APIs", "Socket.IO", "JWT & Role-Based Access Control",
            "HMAC-SHA256 signature verification", "SQLAlchemy & Alembic", "Microservices design patterns", "node-cron"
        ],
        "frontend_mobile": [
            "React.js", "Next.js", "Flutter", "React Native (iOS fintech application maintenance)",
            "HTML5", "CSS3", "Tailwind CSS", "Xcode", "Android Studio"
        ],
        "databases": [
            "MySQL", "SQLite", "FAISS Vector Index", "Sequelize ORM", "Relational Schema Normalization", "Index Optimization"
        ],
        "applied_ai_computer_vision": [
            "Retrieval-Augmented Generation (RAG)", "FAISS Vector Search (IndexFlatIP)", "PyMuPDF Text & Page Coordinates",
            "Ultralytics YOLO (v8 and v11)", "OpenCV", "Biometric Anti-Face Spoofing / Presentation Attack Detection",
            "Real-time video stream frame inferencing over WebSockets", "Dataset preparation (Real vs Fake splits)"
        ],
        "tools_practices": [
            "Docker Compose", "Git & GitHub", "Postman", "Pytest & Vitest (88 tests verified)", "Agile / Scrum", "Jira",
            "Object-Oriented Programming (OOP)", "Data Structures & Algorithms (DSA)", "Clean code architecture"
        ]
    },
    "professional_experience": [
        {
            "role": "Junior Software Developer",
            "company": "KnowledgeQ",
            "location": "Coimbatore, India",
            "period": "Feb 2025 – Present (Active)",
            "domain": "Manufacturing Execution Systems (MES) & Fintech Mobile",
            "contributions": [
                "Develop and maintain backend services and workflows for an enterprise Manufacturing Execution System (MES) application providing production-line traceability and station audit tracking.",
                "Develop, maintain, and support React Native iOS applications, delivering features, defect resolution, and App Store builds for Fintech clients.",
                "Engineer robust RESTful APIs in Node.js, Express, and TypeScript connected to relational MySQL databases for high-integrity transactions.",
                "Collaborate closely with QA engineers, developers, and solution architects using Agile/Scrum sprints, Git branch workflows, and code reviews."
            ],
            "technologies": ["Node.js", "Express.js", "TypeScript", "React.js", "React Native (iOS)", "Flutter", "MySQL", "REST APIs", "Xcode", "Git"]
        },
        {
            "role": "Full Stack Web Development Trainee",
            "company": "Qtree Technologies",
            "location": "Coimbatore, India",
            "period": "July 2024 – Dec 2024 (6 months)",
            "contributions": [
                "Completed comprehensive full-stack engineering program developing web applications and REST APIs using React.js, Node.js, Express.js, and MySQL.",
                "Designed normalized relational database schemas, query optimization, input validation, and secure authentication flows with JWT and password hashing.",
                "Collaborated in Agile development teams utilizing Git and GitHub, performing testing, debugging, and cross-browser responsiveness tuning."
            ],
            "technologies": ["React.js", "Node.js", "Express.js", "HTML5", "CSS3", "JavaScript (ES6+)", "MySQL", "Git"]
        }
    ],
    "featured_projects": [
        {
            "id": "teamtrack",
            "name": "TeamTrack – Real-Time Project Management Platform",
            "status": "Source Available / Local Demo (Production-Ready Architecture)",
            "repository": "https://github.com/surya-murugasen/TeamTrack_-_Real-Time_Project_Management_Platform",
            "category": "Full-Stack Web & API Platform",
            "problem_addressed": (
                "Eliminates asynchronous delays and conflict in sprint task execution through event-driven "
                "WebSockets, server-to-server HMAC security, and relational MySQL data storage."
            ),
            "surya_contribution": (
                "Engineered modular Express.js / TypeScript REST API layer, HMAC-SHA256 inter-service "
                "authentication middleware (server/src/middlewares/hmacAuth.ts), WebSocket room multiplexing "
                "with Socket.IO, and normalized relational MySQL models with Sequelize."
            ),
            "tech_stack": ["Next.js / React", "Node.js", "Express.js", "TypeScript", "MySQL (Sequelize)", "Socket.IO", "JWT", "HMAC-SHA256", "Git"],
            "key_features": [
                "Dual-layer security: User JWT access control and server-to-server HMAC-SHA256 signature verification.",
                "Sub-200ms real-time event dissemination across connected clients.",
                "Relational schema indexing ensuring task transitions do not orphan parent projects.",
                "Automated log retention cleanup via node-cron (midnight prune of logs > 15 days)."
            ],
            "case_study_available": True,
            "case_study_id": "modal-teamtrack"
        },
        {
            "id": "visionguard",
            "name": "VisionGuard AI – Enterprise Anti-Face Spoofing System",
            "status": "Source Available / Local Demo",
            "repository": "https://github.com/surya-murugasen/AI-powered_Enterprise_Anti-Face_Spoofing_System",
            "category": "Applied AI & Computer Vision System",
            "problem_addressed": (
                "Protects biometric verification pipelines from fraudulent presentation attacks "
                "including printed 2D photos and digital screen video replay attacks."
            ),
            "surya_contribution": (
                "Trained and fine-tuned custom YOLO computer vision model on curated Real vs Spoof datasets; "
                "constructed Python Flask-SocketIO streaming microservice with OpenCV frame processing; "
                "integrated Vite React webcam frontend and Node.js audit backend."
            ),
            "tech_stack": ["Python", "Ultralytics YOLO (v8/v11)", "OpenCV", "Flask-SocketIO", "Node.js", "Express.js", "React (Vite)", "SQLite / Sequelize"],
            "key_features": [
                "Real-time webcam frame processing streaming over WebSockets.",
                "Bandwidth-optimized 3 FPS client throttling preventing GPU memory saturation while preserving liveness security.",
                "Sub-150ms inference latency returning bounding boxes and attack confidence scores.",
                "Asynchronous audit logging to SQLite database decoupled from video streaming."
            ],
            "case_study_available": True,
            "case_study_id": "modal-visionguard"
        },
        {
            "id": "mes-traceability",
            "name": "Manufacturing Execution System (MES) – Traceability Platform",
            "status": "Enterprise Production (KnowledgeQ) – Sanitized Architecture Case Study",
            "category": "Industrial Systems & Traceability",
            "confidentiality_note": "Specific proprietary customer codes, factory endpoints, and IP are sanitized.",
            "problem_addressed": (
                "Enforces sequential station manufacturing constraints, prevents out-of-order station bypasses, "
                "and ensures sub-50ms barcode scan response times for serialized components."
            ),
            "surya_contribution": (
                "Engineered RESTful service endpoints in Node.js/TypeScript for shop-floor scanner handshakes; "
                "designed indexed relational MySQL tables capturing component serialization and lot genealogy; "
                "implemented strict validation state machines preventing uninspected assembly progressions."
            ),
            "tech_stack": ["Node.js", "Express.js", "TypeScript", "MySQL", "REST APIs", "Git", "React / React Native"],
            "case_study_available": True,
            "case_study_id": "modal-mes"
        },
        {
            "id": "rag-document-intelligence",
            "name": "RAG Document Intelligence – Vector Retrieval & Multi-User Security",
            "status": "Verified Local Demo & Docker Architecture (88 Automated Tests Passed)",
            "category": "Retrieval-Augmented Generation & Vector Intelligence",
            "problem_addressed": (
                "Technical document exploration and question answering over complex PDFs/TXTs requires "
                "deterministic page-level citation jump links, strict page-isolated chunking, chunk overlap debugging, "
                "and server-side multi-user document authorization without cross-tenant retrieval leaks."
            ),
            "surya_contribution": (
                "Engineered asynchronous FastAPI (Python 3.12) backend; PyMuPDF text & page-coordinate extractor with scanned page detection; "
                "recursive chunker with strict page boundaries (prevent_cross_page: true); FAISS IndexFlatIP cosine similarity vector search; "
                "Chunk Inspector with measured token overlap; server-side session authentication with SQLAlchemy/Alembic SQLite persistence; "
                "and React 19 / TypeScript citation viewer with pdfjs-dist."
            ),
            "tech_stack": [
                "Python 3.12", "FastAPI", "FAISS (IndexFlatIP)", "PyMuPDF (fitz)", "React 19", "TypeScript",
                "Vite", "Tailwind CSS", "SQLite (SQLAlchemy / Alembic)", "Docker Compose", "pdfjs-dist"
            ],
            "key_features": [
                "Strict Page Isolation: Chunks never cross page boundaries, ensuring single-page provenance for exact citation navigation.",
                "Chunk Inspector: Calculates and visualizes exact measured character overlap across adjacent chunks and reports cosine similarity scores.",
                "Phase 10 Multi-User Authorization: Secure HTTP-only session cookies, password hashing with salt, and backend-enforced ownership checks on all endpoints.",
                "FAISS Retrieval Isolation: Candidate vector chunks are strictly validated against authorized document IDs before reaching generation pipelines.",
                "High Automated Test Coverage: 88 passing tests (63 backend pytest + 25 frontend vitest) verifying multi-user isolation, persistence across restarts, and citation accuracy."
            ],
            "limitations_clarification": (
                "Local/Docker architecture; currently runs with synthetic deterministic embeddings or local models without paid cloud LLM dependencies; "
                "OCR for scanned image-only PDFs is not supported in this version."
            ),
            "case_study_available": True,
            "case_study_id": "modal-rag"
        }
    ],
    "education": [
        {
            "degree": "Bachelor of Engineering (B.E.) in Computer Science & Engineering",
            "institution": "Hindusthan College of Engineering and Technology, Coimbatore",
            "period": "2020 – 2024",
            "cgpa": "8.21 / 10",
            "coursework": ["Data Structures & Algorithms", "Database Management Systems", "Computer Networks", "Operating Systems", "Object-Oriented Software Engineering"]
        },
        {
            "certification": "Full Stack Web Development Intensive Program (6 Months)",
            "institution": "Qtree Technologies",
            "period": "July 2024 – Dec 2024"
        },
        {
            "credential": "HSC (Class XII)",
            "institution": "AKKV Aarunadu Matric Higher Secondary School, Trichy",
            "period": "2019 – 2020",
            "score": "69%"
        },
        {
            "credential": "SSLC (Class X)",
            "institution": "Vaasavi Vidyalaya School, Trichy",
            "period": "2017 – 2018",
            "score": "79%"
        }
    ],
    "guardrails": {
        "strictly_refuse": [
            "Inventing unverified employment history, client names, or salary details.",
            "Claiming years of experience beyond February 2025 professional full-time employment plus 2024 trainee program.",
            "Claiming cloud certifications (AWS/GCP/Azure) that Surya does not hold.",
            "Revealing confidential internal production URLs or manufacturing customer data from KnowledgeQ.",
            "Claiming OCR support for scanned image-only PDFs in the RAG Document Intelligence project.",
            "Claiming cloud production enterprise deployment for RAG Document Intelligence beyond the verified local/Docker environment.",
            "Answering general off-topic questions unrelated to Surya M, software engineering, or hiring."
        ],
        "missing_information_guidance": (
            "If asked about something not in this knowledge base, explicitly clarify: "
            "'I do not have verified records on that specific topic in Surya's portfolio. "
            "You can contact Surya directly at suryamurugasen135@gmail.com or via LinkedIn.'"
        )
    }
}


def build_system_prompt() -> str:
    """Generate a compact, strictly grounded system prompt for the AI assistant."""
    import json
    kb_json = json.dumps(PORTFOLIO_KNOWLEDGE, indent=2)
    return f"""You are the official Portfolio AI Assistant for Surya M, a Software Developer based in Tamil Nadu, India.
Your mission is to help recruiters, engineering managers, clients, and technical collaborators evaluate Surya's verified technical abilities, projects, and architecture decisions.

### STRICT OPERATIONAL RULES:
1. GROUNDED IN TRUTH ONLY: Answer ONLY using the facts provided in the VERIFIED KNOWLEDGE BASE below. NEVER invent or extrapolate achievements, client names, metrics, certifications, or past companies.
2. HONEST BOUNDARIES: If the user asks about skills, experiences, or topics not mentioned in the knowledge base, state clearly: "I don't have verified records regarding that in Surya's portfolio. You can connect with Surya directly at suryamurugasen135@gmail.com or on LinkedIn."
3. DISTINGUISH SCOPE: Accurately distinguish implemented features from planned work or trainee projects.
4. ACTIONABLE CITATIONS: Whenever discussing projects, provide direct context and refer the user to the relevant case study (e.g. TeamTrack, VisionGuard AI, or MES Traceability) and repository links.
5. PROFESSIONAL & CONCISE: Maintain a courteous, precise, senior engineering tone. Use bullet points for readability. Keep answers focused (under 180 words unless a detailed architecture breakdown is explicitly requested).
6. OFF-TOPIC REFUSAL: Politely decline questions unrelated to Surya M's skills, projects, experience, or hiring opportunities.

### VERIFIED KNOWLEDGE BASE:
{kb_json}
"""
