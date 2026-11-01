# Production Deployment & Hosting Runbook (Phase 11)

This document outlines the hosting architecture, security controls, production configuration, and operational runbook for Surya M's Portfolio website and decoupled AI Assistant service.

> **CRITICAL PRODUCTION RULE:**  
> Do not deploy publicly, purchase domains, or push live changes until all items in the [Deployment Checklist](#deployment-readiness-checklist) have passed local verification and have received explicit user authorization.

---

## 1. Architecture & Hosting Strategy

The application is architected into two decoupled tiers:

| Component | Architecture | Recommended Platform | Alternative Platforms | Cost Model |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend UI** | Static Jamstack (HTML5, Vanilla CSS3, ES6 JS, Assets) | **Netlify** | Vercel, Cloudflare Pages, GitHub Pages | Free Tier ($0/mo) |
| **AI Assistant** | Python 3.12 + FastAPI Microservice | **Render** | Railway, Fly.io, AWS App Runner | Free / Starter ($0–$5/mo) |

### Rationale:
1. **Netlify for Frontend:**  
   - Instant edge CDN distribution with zero build overhead.  
   - Automatic SSL/TLS certificate generation via Let's Encrypt.  
   - Automatic preview deployments per branch/pull-request.  
   - Declarative security headers and asset caching via `netlify.toml`.
2. **Render for AI Assistant Backend:**  
   - Native Python 3.12 runtime with zero-config Procfile / `render.yaml` blueprint support.  
   - Automated HTTPS endpoint generation.  
   - Automatic health check probe monitoring (`/api/health`).  
   - Zero-cost starter tier with dormant spin-down or $7/mo persistent tier.

---

## 2. Production Security & Guardrails

| Security Control | Implementation | Verification Status |
| :--- | :--- | :---: |
| **API Key Protection** | LLM keys kept exclusively server-side in backend `.env` / PaaS environment variables. | Verified |
| **Git Exclusion** | `.gitignore` explicitly ignores `.env`, `*.env`, `ai-service/.env`, `venv/`, and `__pycache__/`. | Verified |
| **CORS Restriction** | `main.py` restricts origins to Netlify domain, localhost, and `ALLOWED_ORIGIN` env var. | Verified |
| **Rate Limiting** | In-memory sliding window enforcing max 20 requests/minute per client IP (HTTP 429). | Verified |
| **Input Validation** | Pydantic model enforcing 1 to 500 characters max length; sanitizes text against XSS. | Verified |
| **Confidentiality** | Knowledge base strictly sanitizes employer internal codes, customer data, and factory endpoints. | Verified |
| **RAG Isolation** | AI service does not mount or expose local RAG SQLite databases, uploaded PDFs, or FAISS indices. | Verified |
| **Honest Claims** | Assistant explicitly rejects unsupported claims (refuses OCR for scanned PDFs; clarifies local/Docker architecture vs public enterprise scale). | Verified |

---

## 3. Environment Variables Reference

### Frontend Tier (Netlify)
The frontend requires **zero secret environment variables**.  
To point the frontend to the production AI service:
- Set `<meta name="ai-api-base" content="https://<your-service>.onrender.com">` in `index.html`, OR
- Define `window.AI_API_BASE = 'https://<your-service>.onrender.com'` before `script.js` loads.  
*(If unconfigured, the frontend automatically falls back to local `http://localhost:8000` during local dev, and displays a graceful service notice in production without mixed-content errors).*

### AI Assistant Backend Tier (Render / Railway / Docker)

| Variable | Required | Default | Description |
| :--- | :---: | :---: | :--- |
| `PORT` | Auto-set by PaaS | `8000` | HTTP port on which the Uvicorn server listens. |
| `GEMINI_API_KEY` | Optional | *None* | Google Gemini 1.5/2.0 Flash API key. If omitted, service runs in deterministic curated-knowledge fallback mode. |
| `ALLOWED_ORIGIN` | Recommended | *None* | Comma-separated list of allowed client origins (e.g. `https://surya-murugasen-portfolio-5f4d33.netlify.app`). |
| `RATE_LIMIT_MAX_REQUESTS` | Optional | `20` | Maximum queries permitted per sliding window. |
| `RATE_LIMIT_WINDOW_SECONDS` | Optional | `60` | Duration of rate-limiting window in seconds. |

---

## 4. Deployment Guides

### A. Frontend Deployment (Netlify)

1. **Prerequisites:**
   - GitHub repository connected to Netlify account.
   - Branch: `main`.
2. **Build Settings in Netlify:**
   - **Base directory:** *(leave empty)*
   - **Build command:** *(leave empty — static site requires no build)*
   - **Publish directory:** `.`
3. **Configuration File (`netlify.toml`):**
   - Automatically provides HTTP security headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`).
4. **Trigger Deployment:**
   ```bash
   git add .
   git commit -m "feat(portfolio): prepare production deployment with netlify.toml and security headers"
   git push origin main
   ```

### B. AI Assistant Deployment (Render)

1. **Option 1: Using Render Blueprint (`render.yaml`):**
   - In Render Dashboard, click **New +** -> **Blueprint**.
   - Connect the repository. Render will automatically detect `render.yaml` in `ai-service/`.
   - Fill in `GEMINI_API_KEY` (if using external LLM) and deploy.

2. **Option 2: Manual Web Service:**
   - **Type:** Web Service
   - **Root Directory:** `ai-service`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/api/health`

3. **Option 3: Containerized Hosting (Docker):**
   - Build container:
     ```bash
     cd portfolio/ai-service
     docker build -t surya-portfolio-ai-assistant .
     docker run -d -p 8000:8000 --env-file .env surya-portfolio-ai-assistant
     ```

---

## 5. Post-Deployment Verification & Health Checks

Once deployed to production:

1. **Verify Health Endpoint:**
   ```bash
   curl -i https://<your-service>.onrender.com/api/health
   ```
   *Expected Response:* `HTTP/1.1 200 OK` with JSON `{"status": "healthy", ...}`.

2. **Verify CORS Preflight:**
   ```bash
   curl -i -X OPTIONS https://<your-service>.onrender.com/api/chat \
     -H "Origin: https://surya-murugasen-portfolio-5f4d33.netlify.app" \
     -H "Access-Control-Request-Method: POST"
   ```
   *Expected Response:* `Access-Control-Allow-Origin: https://surya-murugasen-portfolio-5f4d33.netlify.app`.

3. **Verify Frontend Live Site:**
   - Open live URL in Chrome/Firefox/Safari.
   - Inspect browser console: zero errors.
   - Open AI Assistant: ask `"Explain my RAG Document Intelligence architecture."`
   - Verify reply appears and clicking `"Open RAG Architecture"` opens `#modal-rag`.

---

## 6. Rollback Procedures

If an issue occurs post-deployment:

### Frontend Rollback (Netlify):
1. Navigate to **Netlify Dashboard** -> **Deploys**.
2. Locate the previous stable deploy.
3. Click **Options** -> **Publish deploy**.  
   *Rollback takes effect globally across CDN nodes within seconds.*
4. Or via Git:
   ```bash
   git revert HEAD
   git push origin main
   ```

### AI Service Rollback (Render):
1. Navigate to **Render Dashboard** -> **Events**.
2. Select the previous successful deploy and click **Rollback**.
