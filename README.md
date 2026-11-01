# Surya M &mdash; Software Developer Portfolio

A modern, high-performance, and accessible personal portfolio website for **Surya M**, Software Developer specializing in Node.js, TypeScript, Express, MySQL relational design, React, Flutter, and enterprise Manufacturing Execution Systems (MES) Traceability platforms.

Equipped with an integrated **Grounded AI Portfolio Assistant** powered by FastAPI and Google Gemini to help recruiters, engineering managers, and clients evaluate technical capabilities in real time.

---

## 📑 Table of Contents

- [Overview & Architecture](#overview--architecture)
- [Key Features](#key-features)
- [AI Portfolio Assistant Service](#ai-portfolio-assistant-service)
- [Technical Positioning & Projects](#technical-positioning--projects)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [How to Run Locally on Windows](#how-to-run-locally-on-windows)
- [Testing & Quality Verification](#testing--quality-verification)
- [Deployment Guide (Netlify & AI Service)](#deployment-guide-netlify--ai-service)
- [Cost Estimation & Limits](#cost-estimation--limits)
- [Customization & Maintenance](#customization--maintenance)
- [Known Limitations & Future Roadmap](#known-limitations--future-roadmap)
- [Contact](#contact)

---

## 🔍 Overview & Architecture

This portfolio operates as an ultra-fast, zero-build client-side static web application with an optional decoupled Python FastAPI AI service:

### Frontend Stack
- **HTML5:** Semantic document hierarchy, SEO Open Graph metadata, accessible landmarks, and WCAG-compliant viewports.
- **CSS3 & Tailwind CSS:** Cyber-dark glassmorphism styling with `#0b0f19` midnight obsidian background, electric blue (`#3b82f6`) and amethyst violet (`#8b5cf6`) accents, and `@media (prefers-reduced-motion)` support.
- **JavaScript (Vanilla ES6+):** Pure browser DOM interactions, IntersectionObserver scroll-fade animations, keyboard-accessible ARIA modals, clipboard utilities, and conversational AI assistant widget.
- **Typography & Icons:** Google Fonts (*Inter*), Font Awesome 6.4.0.

### AI Assistant Backend Stack (`ai-service/`)
- **Runtime:** Python 3.12 + FastAPI + Uvicorn + Pydantic + httpx.
- **LLM Integration:** Google Gemini 1.5 Flash REST API with strict system prompt grounding.
- **Security & Guardrails:** API keys kept exclusively on the server (`.env`), input validation (1–500 chars), sliding-window rate limiting per IP (20 req/min), CORS restrictions, and strict rejection of off-topic queries or hallucinated claims.
- **Zero-Key Fallback:** Built-in deterministic lexical retrieval over curated knowledge base when no external API key is supplied, ensuring continuous demo availability without fake simulation.

---

## ✨ Key Features

1. **Grounded AI Portfolio Assistant:**
   - Floating interactive launcher and collapsible glassmorphism chat panel.
   - Grounded strictly in curated ground-truth facts (`knowledge.py`).
   - Recommends direct case study dialogs (`data-case-study-target`) and repository links.
   - Refuses off-topic questions, prompt injections, and unverified achievements.
   - Keyboard accessible (`Escape` to close, auto-focus, character counter).

2. **Professional Technical Positioning:**
   - Clearly documents production experience at KnowledgeQ in Manufacturing Execution Systems (MES) Traceability and Fintech mobile applications.
   - Highlights 4 technical pillars: Backend APIs, Relational Database Normalization, Cross-Platform Mobile (React Native / Flutter), and Applied Computer Vision.

3. **Demonstrable Project Evidence:**
   - **RAG Document Intelligence:** Production-grade Retrieval-Augmented Generation system with page-isolated semantic chunking, FAISS vector indexing, interactive PDF viewer with page-level citations, Chunk Inspector measuring token overlap, and Phase 10 multi-user authorization (88 automated tests passed).
   - **TeamTrack:** Full-Stack Project Management Platform with real-time Socket.IO and HMAC-SHA256 signature middleware (`hmacAuth.ts`). Direct links to the public repository.
   - **VisionGuard AI:** 3-tier enterprise presentation attack detection (anti-face spoofing) system leveraging Ultralytics YOLOv11 and OpenCV with WebSocket frame streaming.
   - **MES Traceability Platform:** Sanitized industrial case study detailing WIP state machine validations and sub-50ms barcode scan processing.

4. **In-Depth Architectural Case Studies:**
   - Interactive modals for each project documenting the problem statement, constraints, architecture diagram, security controls, and testing evidence.

5. **High-Conversion Contact Actions:**
   - Pre-formatted `mailto:` engineering inquiry template.
   - Instant 1-click clipboard email copy utility with visual confirmation.
   - Clean, verified links to GitHub, LinkedIn, and PDF resume.

6. **Accessibility & Usability (WCAG Compliant):**
   - Skip-to-content keyboard link.
   - User-scalable mobile viewport (no disabling zoom).
   - High-contrast `:focus-visible` outlines.
   - Full ARIA attributes on modals (`role="dialog"`, `aria-modal="true"`) and hamburger menu (`aria-expanded`).
   - Reduced-motion OS preference compatibility.

---

## 🤖 AI Portfolio Assistant Service

The AI Assistant is located in `ai-service/`:

```text
ai-service/
├── main.py              # FastAPI application with rate limiting, CORS, & LLM handler
├── knowledge.py         # Curated ground-truth portfolio knowledge & system prompt
├── requirements.txt     # Python dependencies (fastapi, uvicorn, pydantic, httpx, dotenv)
├── test_assistant.py    # Automated test suite (health, grounding, guardrails, limits)
└── .env.example         # Template for environment variables (GEMINI_API_KEY)
```

### Running the AI Assistant Service

1. Open PowerShell and navigate to `ai-service`:
   ```powershell
   cd C:\Projects\Production_Projects\portfolio\ai-service
   ```
2. (Optional) Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Configure your API key:
   ```powershell
   Copy-Item .env.example .env
   # Edit .env and set GEMINI_API_KEY=<your-key> (Free from https://aistudio.google.com/)
   ```
4. Start the server on port 8000:
   ```powershell
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

*Note: If no `GEMINI_API_KEY` is provided, the service automatically runs in curated retrieval mode, answering all portfolio questions factually without incurring any API costs.*

---

## 🗂️ Project Structure

```text
portfolio/
├── index.html            # Main portfolio entry point & single-page layout with AI widget
├── styles.css            # Custom animations, focus states, glassmorphism & AI panel styles
├── script.js             # Navigation, scroll animations, modals, copy & AI controller
├── resume.html           # Dedicated print/web responsive resume view
├── Surya_M_Resume.pdf    # Verified downloadable PDF resume
├── Surya M.pdf           # Backup copy of PDF resume
├── your-image.jpg        # Profile image asset
├── DEPLOYMENT.md         # Git and Netlify continuous deployment reference
├── README.md             # Complete project and developer documentation
└── ai-service/           # Decoupled Python FastAPI AI Assistant Microservice
    ├── main.py
    ├── knowledge.py
    ├── requirements.txt
    ├── test_assistant.py
    └── .env.example
```

---

## ⚙️ Prerequisites

- **Frontend:** No build steps required. Any modern web browser.
- **AI Service (Optional):** Python 3.10+ (tested on Python 3.12).

---

## 🚀 How to Run Locally on Windows

Open two terminal windows:

### Terminal 1: Static Portfolio Frontend
```powershell
cd C:\Projects\Production_Projects\portfolio
python -m http.server 3000
```
Open **`http://localhost:3000`** in your browser.

### Terminal 2: AI Assistant Backend
```powershell
cd C:\Projects\Production_Projects\portfolio\ai-service
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🧪 Testing & Quality Verification

Run automated test suites to ensure complete health:

### 1. Validate AI Assistant Service (Python)
```powershell
cd C:\Projects\Production_Projects\portfolio\ai-service
python test_assistant.py
```
**Test Results (9/9 Passed):**
- `PASS: test_health` — Verifies `/api/health` status and provider config.
- `PASS: test_suggested_questions` — Verifies starter prompt chips.
- `PASS: test_teamtrack_grounding` — Confirms real-time sync, HMAC, and repo action.
- `PASS: test_visionguard_grounding` — Confirms YOLOv11, OpenCV, 3 FPS, and GitHub action.
- `PASS: test_mes_traceability_grounding` — Confirms KnowledgeQ, state validation, and sanitized case study.
- `PASS: test_missing_information_refusal` — Asserts assistant refrains from hallucinating unverified claims (e.g. Solidity/Blockchain).
- `PASS: test_validation_empty_message` — Verifies rejection of blank inputs.
- `PASS: test_validation_oversized_message` — Verifies rejection of queries > 500 characters.
- `PASS: test_rate_limiting` — Confirms HTTP 429 response upon exceeding 20 req/min per IP.

### 2. Validate Frontend JavaScript Syntax
```powershell
cd C:\Projects\Production_Projects\portfolio
node --check script.js
```
*Expected: Clean exit code 0.*

---

## 🌐 Deployment Guide (Netlify & AI Service)

### 1. Frontend Deployment (Netlify)
The frontend remains 100% static and zero-cost on Netlify.
Every push to `main` on GitHub triggers an automatic deployment at:
**`https://surya-murugasen-portfolio-5f4d33.netlify.app`**

### 2. AI Assistant Deployment (Render / Railway / Fly.io)
Deploy the `ai-service/` subfolder as an independent Web Service:

#### Deploying on Render (Free Tier eligible):
1. Create a new **Web Service** on [Render.com](https://render.com).
2. Connect your GitHub repository.
3. Configure settings:
   - **Root Directory:** `ai-service`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set Environment Variables:
   - `GEMINI_API_KEY`: `<your-gemini-key>`
   - `ALLOWED_ORIGIN`: `https://surya-murugasen-portfolio-5f4d33.netlify.app`
5. After deployment, update the frontend client in `script.js` or set `window.AI_API_BASE = 'https://<your-render-subdomain>.onrender.com'` before loading `script.js`.

---

## 💰 Cost Estimation & Limits

| Service | Tier | Usage & Cost |
| :--- | :--- | :--- |
| **Frontend Hosting (Netlify)** | Free Tier | Unlimited bandwidth within standard personal portfolio usage ($0/mo). |
| **AI Backend (Render / Railway)** | Free / Starter | Free on Render (with spin-down on inactivity) or ~$5/mo on Railway/Render Starter for persistent 24/7 uptime. |
| **Google Gemini API (`gemini-1.5-flash`)** | Free Tier | **Free Tier:** 15 requests per minute, 1,500 requests per day, 1M TPM at **$0 cost**.<br>**Paid Tier (if exceeded):** $0.075 per 1,000,000 input tokens (~$0.00003 per conversation turn). |
| **Total Estimated Operating Cost** | | **$0.00 / month** on free tiers. |

---

## 🛠️ Customization & Maintenance

- **Updating Knowledge Base:** Update facts in `ai-service/knowledge.py` to keep the assistant aligned with new achievements, promotions, or publications.
- **Adjusting Rate Limits:** Modify `RATE_LIMIT_MAX_REQUESTS` in `ai-service/.env`.
- **Custom Starter Questions:** Edit `/api/suggested-questions` in `ai-service/main.py` and the corresponding chips in `index.html`.

---

## 📞 Contact

- **Name:** Surya M
- **Role:** Software Developer
- **Email:** [suryamurugasen135@gmail.com](mailto:suryamurugasen135@gmail.com)
- **Phone:** +91 9092436936
- **LinkedIn:** [linkedin.com/in/surya-m-softwareservicedeveloper](https://linkedin.com/in/surya-m-softwareservicedeveloper)
- **GitHub:** [github.com/surya-murugasen](https://github.com/surya-murugasen)
- **Live Portfolio:** [surya-murugasen-portfolio-5f4d33.netlify.app](https://surya-murugasen-portfolio-5f4d33.netlify.app)
