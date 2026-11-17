"""
FastAPI Backend for Surya M's Portfolio AI Assistant.
Provides rate-limited, grounded AI responses using server-side LLM credentials.
"""

import os
import re
import time
import httpx
from typing import List, Optional
from collections import defaultdict
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from knowledge import build_system_prompt, PORTFOLIO_KNOWLEDGE

# Load environment variables from local .env
load_dotenv()

app = FastAPI(
    title="Surya M - Portfolio AI Assistant API",
    version="1.0.0",
    description="Grounded AI Assistant service answering technical inquiries about Surya M's verified portfolio."
)

# -----------------------------------------------------------------------------
# CORS Configuration
# -----------------------------------------------------------------------------
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://surya-murugasen-portfolio-5f4d33.netlify.app",
]

# Allow custom origin(s) via env if specified (supports comma-separated list)
env_origins = os.getenv("ALLOWED_ORIGIN") or os.getenv("ALLOWED_ORIGINS")
if env_origins:
    for origin in [o.strip() for o in env_origins.split(",") if o.strip()]:
        if origin not in ALLOWED_ORIGINS:
            ALLOWED_ORIGINS.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# In-Memory Sliding-Window Rate Limiter
# -----------------------------------------------------------------------------
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "20"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
ip_request_history = defaultdict(list)


def check_rate_limit(client_ip: str):
    """Enforce rate limits per client IP."""
    now = time.time()
    history = ip_request_history[client_ip]

    # Clean old entries
    ip_request_history[client_ip] = [ts for ts in history if now - ts < RATE_LIMIT_WINDOW_SECONDS]

    if len(ip_request_history[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Please wait {RATE_LIMIT_WINDOW_SECONDS} seconds before asking more questions."
        )

    ip_request_history[client_ip].append(now)


# -----------------------------------------------------------------------------
# Request & Response Schemas
# -----------------------------------------------------------------------------
class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., max_length=1500)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500, description="User's query")
    history: Optional[List[ChatMessage]] = Field(default=[], description="Previous conversation turns")


class ChatResponse(BaseModel):
    reply: str
    suggested_actions: Optional[List[dict]] = None
    status: str = "success"
    provider: str


# -----------------------------------------------------------------------------
# Direct Knowledge Retrieval / Fallback Logic
# -----------------------------------------------------------------------------
def retrieve_curated_answer(query: str) -> Optional[str]:
    """
    Direct lexical retrieval matcher over curated portfolio facts.
    Acts as a verified deterministic backup when no external LLM key is configured.
    """
    q = query.lower().strip()

    # Identity / Greetings / Assistant Name (use word boundary for short greetings like 'hi')
    is_greeting = bool(re.search(r'\b(hi|hello|hey)\b', q))
    is_identity = any(k in q for k in ["you name", "your name", "who are you", "who created you", "who made you", "what is your name", "identity"])
    if is_identity or (is_greeting and len(q.split()) <= 4):
        return (
            "I am **Surya's Portfolio AI Assistant**!\n\n"
            "I can answer questions regarding Surya's role as a **Software Developer at KnowledgeQ** (MES Traceability & FinTech solutions), "
            "projects like **TeamTrack**, **VisionGuard AI**, and **RAG Document Intelligence**, his technical stack (**Node.js, Express, TypeScript, Python, MySQL, React, Flutter**), "
            "education, or contact details."
        )

    # MES / KnowledgeQ
    if any(k in q for k in ["mes", "traceability", "manufacturing", "knowledgeq"]):
        mes = PORTFOLIO_KNOWLEDGE["featured_projects"][2]
        return (
            f"**Manufacturing Execution System (MES) Traceability**\n\n"
            f"• **Domain:** Industrial Traceability at KnowledgeQ (Jun 2025 – Present, Full-time).\n"
            f"• **Problem:** Enforce sequential station constraints and prevent uninspected component bypasses in production lines.\n"
            f"• **Surya's Role:** Engineered Node.js/TypeScript REST API service endpoints for shop-floor scanner handshakes with sub-50ms latency, and designed indexed MySQL tables for component lot genealogy.\n"
            f"• **Case Study:** View the sanitized case study directly in the portfolio modal."
        )

    # TeamTrack
    if "teamtrack" in q or ("project management" in q and "platform" in q):
        tt = PORTFOLIO_KNOWLEDGE["featured_projects"][0]
        return (
            f"**TeamTrack – Real-Time Project Management Platform**\n\n"
            f"• **Problem:** Eliminates latency in sprint updates through event-driven WebSockets and relational storage.\n"
            f"• **Surya's Contribution:** Engineered modular Express/TypeScript REST APIs, server-to-server HMAC-SHA256 authentication (`hmacAuth.ts`), Socket.IO room broadcast, and Sequelize MySQL models.\n"
            f"• **Stack:** Next.js, Node.js, Express, TypeScript, MySQL, Socket.IO, JWT, HMAC-SHA256.\n"
            f"• **Repository:** [{tt['repository']}]({tt['repository']})"
        )

    # VisionGuard / Anti-Spoofing / AI / YOLO
    if any(k in q for k in ["visionguard", "spoof", "yolo", "opencv", "computer vision", "anti-face"]):
        vg = PORTFOLIO_KNOWLEDGE["featured_projects"][1]
        return (
            f"**VisionGuard AI – Enterprise Anti-Face Spoofing System**\n\n"
            f"• **Problem:** Detects biometric presentation attacks (printed photos and digital video replay attacks) in real time.\n"
            f"• **Surya's Contribution:** Fine-tuned YOLO on curated Real/Spoof splits; built Python Flask-SocketIO streaming microservice with OpenCV frame processing throttled to 3 FPS for low GPU memory overhead; linked to React webcam UI and Node.js audit logging.\n"
            f"• **Stack:** Python, Ultralytics YOLO, OpenCV, Flask-SocketIO, Node.js, React, SQLite.\n"
            f"• **Repository:** [{vg['repository']}]({vg['repository']})"
        )

    # RAG Document Intelligence - Specific Sub-Queries
    # 1. OCR query
    if "ocr" in q:
        return (
            "**OCR Support Status in RAG Document Intelligence**\n\n"
            "• **Direct Answer:** No, the current version of the RAG system does **not** support OCR for scanned image-only PDFs.\n"
            "• **Extraction Mechanism:** Text is extracted directly from the document's native digital text layer using **PyMuPDF (`fitz`)**, ensuring sub-millisecond parsing and high coordinate fidelity without OCR latency.\n"
            "• **Scanned Detection:** When a document contains no selectable text, the system sets `is_scanned_image_only: True` and records an explicit warning rather than fabricating or misreading text.\n"
            "• **Details:** See the RAG case study modal for verified extraction boundaries."
        )

    # 2. Enterprise scale / deployment query
    if any(k in q for k in ["enterprise scale", "production scale", "deployed at scale", "enterprise-scale"]):
        return (
            "**Deployment & Scale Status**\n\n"
            "• **Direct Answer:** The RAG Document Intelligence platform is an architected, fully tested **local and containerized system** orchestrated with **Docker Compose**; it is **not** currently deployed at public enterprise scale.\n"
            "• **Verification Evidence:** The system is thoroughly validated through **88 automated regression tests** (63 backend pytest + 25 frontend vitest) covering multi-user isolation, vector retrieval, and restart persistence.\n"
            "• **Enterprise Background:** Surya's professional enterprise production experience is in **Manufacturing Execution Systems (MES) Traceability** at KnowledgeQ."
        )

    # 3. User isolation / multi-user document authorization
    if (("prevent" in q or "another user" in q or "multi-user" in q or "isolation" in q or "authorization" in q or "cross-user" in q or "accessing" in q) and ("user" in q or "doc" in q)) or "accessing another" in q:
        return (
            "**Multi-User Document Authorization & Isolation (Phase 10)**\n\n"
            "• **Server-Side Session Authentication:** User identity is verified strictly from secure HTTP-only session cookies; client-supplied IDs are never trusted as proof of ownership.\n"
            "• **Endpoint Authorization:** Every document endpoint (`/upload`, `/list`, `/details`, `/chunks`, `/search`, `/ask`, `/pdf`, `/delete`) enforces `session.user_id == document.user_id`.\n"
            "• **FAISS Vector Isolation:** Candidate chunks retrieved from FAISS are strictly filtered against the authenticated user's authorized document IDs before reaching the LLM context or inspector UI.\n"
            "• **Testing Evidence:** Validated with dedicated two-user isolation regression tests (`test_auth_and_isolation.py`), confirming User A cannot view, inspect, search, or delete User B's documents."
        )

    # 4. General RAG architecture / project overview
    if (
        ("architecture" in q and ("rag" in q or "document" in q or "project" in q))
        or ("explain" in q and ("rag" in q or "document intelligence" in q))
        or ("project" in q and ("rag" in q or "document intelligence" in q))
    ):
        rag = PORTFOLIO_KNOWLEDGE["featured_projects"][3]
        return (
            f"**RAG Document Intelligence – System Architecture**\n\n"
            f"• **Frontend (React 19 + TypeScript + Vite):** Interactive PDF viewer (`pdfjs-dist`) with page-level citation jump links and Chunk Inspector with measured overlap visualization.\n"
            f"• **Backend (FastAPI + Python 3.12):** PyMuPDF direct text and coordinate extraction, recursive semantic chunking with strict page isolation (`prevent_cross_page: true`), and FAISS vector indexing.\n"
            f"• **Vector Store (FAISS `IndexFlatIP`):** $L_2$-normalized cosine similarity search with post-retrieval ownership filter gates.\n"
            f"• **Database (SQLite + SQLAlchemy / Alembic):** Persistent storage of users (salted password hashing), revocable sessions, and document metadata.\n"
            f"• **Verification:** 88 automated tests passed (63 backend pytest + 25 frontend vitest) with Docker Compose orchestration.\n"
            f"• **Case Study:** View the complete architecture and data-flow breakdown in the portfolio modal."
        )

    # 5. FAISS vector search query
    if "faiss" in q or "vector search" in q or "cosine" in q or "embeddings" in q:
        return (
            "**RAG Document Intelligence – FAISS Vector Search Architecture**\n\n"
            "• **Index Type:** FAISS `IndexFlatIP` (Inner Product).\n"
            "• **Cosine Similarity:** Embeddings and query vectors are $L_2$-normalized prior to addition and query search, ensuring the inner product mathematically equals **Cosine Similarity** ($\\cos(\\theta) \\in [0.0, 1.0]$).\n"
            "• **Strict Page Isolation:** Chunks never cross physical page boundaries (`prevent_cross_page: true`), guaranteeing 1:1 provenance for exact citation navigation in the PDF viewer.\n"
            "• **Measured Overlap:** The Chunk Inspector calculates and reports exact measured character overlap at boundary delimiters.\n"
            "• **Authorization Filter:** Retrieved vector results are filtered at the service layer against authorized document IDs to prevent cross-tenant data leaks."
        )

    # 6. Fallback general RAG keywords
    if any(k in q for k in ["rag", "document intelligence", "chunk", "citation", "pymupdf", "semantic search"]):
        rag = PORTFOLIO_KNOWLEDGE["featured_projects"][3]
        return (
            f"**RAG Document Intelligence – System Architecture**\n\n"
            f"• **Frontend (React 19 + TypeScript + Vite):** Interactive PDF viewer (`pdfjs-dist`) with page-level citation jump links and Chunk Inspector with measured overlap visualization.\n"
            f"• **Backend (FastAPI + Python 3.12):** PyMuPDF direct text and coordinate extraction, recursive semantic chunking with strict page isolation (`prevent_cross_page: true`), and FAISS vector indexing.\n"
            f"• **Vector Store (FAISS `IndexFlatIP`):** $L_2$-normalized cosine similarity search with post-retrieval ownership filter gates.\n"
            f"• **Database (SQLite + SQLAlchemy / Alembic):** Persistent storage of users (salted password hashing), revocable sessions, and document metadata.\n"
            f"• **Verification:** 88 automated tests passed (63 backend pytest + 25 frontend vitest) with Docker Compose orchestration.\n"
            f"• **Case Study:** View the complete architecture and data-flow breakdown in the portfolio modal."
        )

    # Experience / Background
    if any(k in q for k in ["experience", "work", "job", "career", "background"]):
        return (
            f"**Surya M's Professional Experience**\n\n"
            f"1. **Software Developer at KnowledgeQ** (Jun 2025 – Present · 1 yr 6 mos, Full-time · On-site):\n"
            f"   • Develop and maintain enterprise Manufacturing Execution System (MES) Traceability applications.\n"
            f"   • Build and enhance scalable backend services using Node.js, Express.js, TypeScript, REST APIs, and MySQL.\n"
            f"   • Develop and maintain React Native iOS applications for FinTech solutions, delivering features and App Store releases.\n"
            f"   • Cross-functional Agile collaboration, performance optimization, debugging, and Git best practices.\n\n"
            f"2. **Full Stack Web Development Trainee at Qtree Technologies** (July 2024 – Dec 2024):\n"
            f"   • 6-month intensive training developing REST APIs and React interfaces with MySQL.\n\n"
            f"• **Education:** B.E. in Computer Science & Engineering (2020 – 2024, CGPA 8.21/10) from Hindusthan College of Engineering and Technology."
        )

    # Skills / Technologies
    if any(k in q for k in ["skill", "stack", "technolog", "languages", "backend", "database"]):
        return (
            f"**Surya M's Core Technical Skills**\n\n"
            f"• **Languages:** JavaScript (ES6+), TypeScript, Python, Dart, Java, SQL.\n"
            f"• **Backend & APIs:** Node.js, Express.js, RESTful microservices, Socket.IO, HMAC-SHA256, JWT & RBAC.\n"
            f"• **Databases:** MySQL, SQLite, Sequelize ORM, relational normalization, index tuning.\n"
            f"• **Frontend & Mobile:** React.js, Next.js, Flutter, React Native (iOS).\n"
            f"• **Applied AI:** Ultralytics YOLO (v8/v11), OpenCV, real-time video stream inferencing.\n"
            f"• **Tools:** Git, GitHub, Postman, Jira, Agile/Scrum."
        )

    # Contact / Hire / Location
    if any(k in q for k in ["contact", "email", "phone", "hire", "resume", "location", "reach"]):
        return (
            f"**Contact & Collaboration Details**\n\n"
            f"• **Email:** [suryamurugasen135@gmail.com](mailto:suryamurugasen135@gmail.com)\n"
            f"• **Phone:** +91 9092436936\n"
            f"• **LinkedIn:** [linkedin.com/in/surya-m-softwareservicedeveloper](https://linkedin.com/in/surya-m-softwareservicedeveloper)\n"
            f"• **GitHub:** [github.com/surya-murugasen](https://github.com/surya-murugasen)\n"
            f"• **Location:** Tamil Nadu, India (Available for on-site in Coimbatore, Chennai, Bangalore, or remote roles)."
        )

    return None


# -----------------------------------------------------------------------------
# External LLM Query Execution
# -----------------------------------------------------------------------------
async def query_gemini_api(api_key: str, user_message: str, history: List[ChatMessage]) -> str:
    """Call Google Gemini REST API with the system prompt and conversation history."""
    system_prompt = build_system_prompt()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    # Build contents payload
    contents = []
    
    # Include recent history turns (up to 4 turns for context)
    for msg in history[-4:]:
        role = "user" if msg.role == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg.content}]
        })

    # Add current user prompt
    contents.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    payload = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.2,  # Low temperature for strict factual grounding
            "maxOutputTokens": 450,
            "topP": 0.8
        }
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(url, json=payload)
        if response.status_code != 200:
            error_text = response.text
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"LLM Provider returned error ({response.status_code}): {error_text[:200]}"
            )
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Malformed response received from LLM Provider."
            )


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------
@app.get("/api/health")
async def health_check():
    """Health check endpoint indicating service status and configured LLM provider."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    return {
        "status": "healthy",
        "service": "portfolio-ai-assistant",
        "provider": "google-gemini" if gemini_key else "curated-retrieval-fallback",
        "llm_key_configured": bool(gemini_key),
        "rate_limit_per_minute": RATE_LIMIT_REQUESTS
    }


@app.get("/api/suggested-questions")
async def get_suggested_questions():
    """Provide quick conversation starter prompts."""
    return [
        {"label": "RAG Intelligence", "prompt": "How does Surya's RAG Document Intelligence system work?"},
        {"label": "MES Traceability", "prompt": "What is Surya's experience with Manufacturing Execution Systems (MES)?"},
        {"label": "TeamTrack Architecture", "prompt": "How does TeamTrack handle real-time sync and HMAC security?"},
        {"label": "VisionGuard AI", "prompt": "What did Surya build for the VisionGuard AI anti-spoofing system?"},
        {"label": "Backend Stack", "prompt": "Which backend technologies and databases does Surya specialize in?"},
        {"label": "Contact Surya", "prompt": "How can I contact Surya for engineering opportunities?"}
    ]


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request, body: ChatRequest):
    """
    Process an incoming user message, validate length, rate-limit, and return
    a grounded answer with relevant portfolio action links.
    """
    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(client_ip)

    user_query = body.message.strip()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty.")

    # Determine actions to suggest based on query context
    suggested_actions = []
    q_lower = user_query.lower()

    if any(k in q_lower for k in ["rag", "faiss", "vector", "document intelligence", "chunk", "citation", "pymupdf", "ocr", "another user", "isolation", "enterprise scale", "scale"]):
        suggested_actions.append({"type": "case_study", "target": "modal-rag", "label": "Open RAG Architecture"})
    elif any(k in q_lower for k in ["teamtrack", "project management"]):
        suggested_actions.append({"type": "case_study", "target": "modal-teamtrack", "label": "Open TeamTrack Architecture"})
        suggested_actions.append({"type": "repo", "url": "https://github.com/surya-murugasen/TeamTrack_-_Real-Time_Project_Management_Platform", "label": "View TeamTrack GitHub"})
    elif any(k in q_lower for k in ["visionguard", "spoof", "yolo", "cv"]):
        suggested_actions.append({"type": "case_study", "target": "modal-visionguard", "label": "Open VisionGuard Architecture"})
        suggested_actions.append({"type": "repo", "url": "https://github.com/surya-murugasen/AI-powered_Enterprise_Anti-Face_Spoofing_System", "label": "View VisionGuard GitHub"})
    elif any(k in q_lower for k in ["mes", "traceability", "manufacturing", "knowledgeq"]):
        suggested_actions.append({"type": "case_study", "target": "modal-mes", "label": "Open MES Traceability Architecture"})
    elif any(k in q_lower for k in ["contact", "email", "hire", "phone", "resume"]):
        suggested_actions.append({"type": "scroll", "target": "#contact", "label": "Go to Contact Section"})
        suggested_actions.append({"type": "download", "url": "Surya_M_Resume.pdf", "label": "Download Resume PDF"})

    # Check for GEMINI_API_KEY
    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_key:
        try:
            reply_text = await query_gemini_api(gemini_key, user_query, body.history or [])
            return ChatResponse(
                reply=reply_text,
                suggested_actions=suggested_actions if suggested_actions else None,
                status="success",
                provider="gemini-1.5-flash"
            )
        except HTTPException:
            raise
        except Exception as e:
            # Fallback to curated retrieval if external API fails
            fallback = retrieve_curated_answer(user_query)
            if fallback:
                if "RAG Document Intelligence" in fallback and not any(a.get("target") == "modal-rag" for a in suggested_actions):
                    suggested_actions.append({"type": "case_study", "target": "modal-rag", "label": "Open RAG Architecture"})
                return ChatResponse(
                    reply=fallback,
                    suggested_actions=suggested_actions if suggested_actions else None,
                    status="fallback_success",
                    provider="curated-knowledge-retrieval"
                )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Unable to reach LLM Provider: {str(e)}"
            )

    # If no API key is configured on server, use the curated knowledge retrieval
    curated_reply = retrieve_curated_answer(user_query)
    if curated_reply:
        if ("RAG Document Intelligence" in curated_reply or "FAISS" in curated_reply or "OCR" in curated_reply) and not any(a.get("target") == "modal-rag" for a in suggested_actions):
            suggested_actions.append({"type": "case_study", "target": "modal-rag", "label": "Open RAG Architecture"})
        return ChatResponse(
            reply=curated_reply,
            suggested_actions=suggested_actions if suggested_actions else None,
            status="curated_success",
            provider="curated-knowledge-retrieval"
        )

    # Off-topic or unindexed query response
    return ChatResponse(
        reply=(
            "I don't have verified records on that specific topic in Surya's portfolio. "
            "I can answer questions regarding Surya's work at KnowledgeQ (MES Traceability), "
            "projects like TeamTrack, VisionGuard AI, and RAG Document Intelligence, technical stack (Node.js, TypeScript, Python, MySQL, React, Flutter), "
            "education, or contact details.\n\n"
            "Feel free to email Surya directly at [suryamurugasen135@gmail.com](mailto:suryamurugasen135@gmail.com)."
        ),
        suggested_actions=suggested_actions if suggested_actions else None,
        status="not_found",
        provider="curated-knowledge-retrieval"
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
