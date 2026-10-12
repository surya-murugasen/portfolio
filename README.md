# Surya M &mdash; Software Developer Portfolio

A modern, high-performance, and accessible personal portfolio website for **Surya M**, Software Developer specializing in Node.js, TypeScript, Express, MySQL relational design, React, Flutter, and enterprise Manufacturing Execution Systems (MES) Traceability platforms.

Built with semantic HTML5, modern CSS3 (Tailwind CSS CDN + custom design tokens), vanilla JavaScript (ES6+), and Font Awesome 6.

---

## 📑 Table of Contents

- [Overview & Architecture](#overview--architecture)
- [Key Features](#key-features)
- [Technical Positioning & Projects](#technical-positioning--projects)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [How to Run Locally on Windows](#how-to-run-locally-on-windows)
- [Testing & Quality Verification](#testing--quality-verification)
- [Deployment Guide (Netlify & Static Hosting)](#deployment-guide-netlify--static-hosting)
- [Customization & Maintenance](#customization--maintenance)
- [Known Limitations & Future Roadmap](#known-limitations--future-roadmap)
- [Contact](#contact)

---

## 🔍 Overview & Architecture

This portfolio operates as an ultra-fast, zero-build client-side static web application designed to be directly deployable to any static hosting provider (such as Netlify, GitHub Pages, or Vercel) or served locally using Python or Node.js.

### Core Stack
- **HTML5:** Semantic document hierarchy, SEO Open Graph metadata, accessible landmarks, and WCAG-compliant viewports.
- **CSS3 & Tailwind CSS:** Cyber-dark glassmorphism styling with `#0b0f19` midnight obsidian background, electric blue (`#3b82f6`) and amethyst violet (`#8b5cf6`) accents, and `@media (prefers-reduced-motion)` support.
- **JavaScript (Vanilla ES6+):** Pure browser DOM interactions, IntersectionObserver scroll-fade animations, keyboard-accessible ARIA modals, and clipboard copy utilities.
- **Typography & Icons:** Google Fonts (*Inter*), Font Awesome 6.4.0.

---

## ✨ Key Features

1. **Professional Technical Positioning:**
   - Clearly documents production experience at KnowledgeQ in Manufacturing Execution Systems (MES) Traceability and Fintech mobile applications.
   - Highlights 4 technical pillars: Backend APIs, Relational Database Normalization, Cross-Platform Mobile (React Native / Flutter), and Applied Computer Vision.

2. **Demonstrable Project Evidence:**
   - **TeamTrack:** Full-Stack Project Management Platform with real-time Socket.IO and HMAC-SHA256 signature middleware (`hmacAuth.ts`). Direct links to the public repository.
   - **VisionGuard AI:** 3-tier enterprise presentation attack detection (anti-face spoofing) system leveraging Ultralytics YOLOv11 and OpenCV with WebSocket frame streaming.
   - **MES Traceability Platform:** Sanitized industrial case study detailing WIP state machine validations and sub-50ms barcode scan processing.

3. **In-Depth Architectural Case Studies:**
   - Interactive modals for each project documenting the problem statement, constraints, architecture diagram, security controls, and testing evidence.

4. **High-Conversion Contact Actions:**
   - Pre-formatted `mailto:` engineering inquiry template.
   - Instant 1-click clipboard email copy utility with feedback.
   - Clean, verified links to GitHub, LinkedIn, and PDF resume.

5. **Accessibility & Usability (WCAG Compliant):**
   - Skip-to-content keyboard link.
   - User-scalable mobile viewport (no disabling zoom).
   - High-contrast `:focus-visible` outlines.
   - Full ARIA attributes on modals (`role="dialog"`, `aria-modal="true"`) and hamburger menu (`aria-expanded`).
   - Reduced-motion OS preference compatibility.

---

## 🗂️ Project Structure

```text
portfolio/
├── index.html            # Main portfolio entry point & single-page layout
├── styles.css            # Custom animations, focus states, glassmorphism & media queries
├── script.js             # Mobile menu, intersection observer, modals & clipboard copy
├── resume.html           # Dedicated print/web responsive resume view
├── Surya_M_Resume.pdf    # Verified downloadable PDF resume (clean URL filename)
├── Surya M.pdf           # Backup copy of PDF resume
├── your-image.jpg        # Profile image asset
├── DEPLOYMENT.md         # Git and Netlify continuous deployment reference
└── README.md             # Complete project and developer documentation
```

---

## ⚙️ Prerequisites

No compilation tools, bundlers, or package installations are required to run this website.

To run via a local HTTP server on Windows, you only need one of the following:
- **Python 3.x** (Standard on developer machines)
- **Node.js** (v18 or higher)
- **VS Code** with the *Live Server* extension

---

## 🚀 How to Run Locally on Windows

Open PowerShell or Command Prompt in the project folder:

```powershell
cd C:\Projects\Production_Projects\portfolio
```

### Option A: Local Python Web Server (Recommended)
```powershell
python -m http.server 3000
```
Then visit: **`http://localhost:3000`** in your browser. *(Press `Ctrl + C` in the terminal to stop).*

---

### Option B: Local Node.js / `npx serve`
```powershell
npx serve .
```
Then visit the local port displayed in the console (typically **`http://localhost:3000`**).

---

### Option C: Direct File Execution
```powershell
Start-Process "index.html"
```
Or double-click `index.html` in File Explorer.

---

## 🧪 Testing & Quality Verification

Run these verification steps to ensure site health before pushing:

### 1. Validate JavaScript Syntax
```powershell
node --check script.js
```
*Expected: Exits with code 0 and no syntax errors.*

### 2. Verify Local HTTP Serving
```powershell
# In terminal 1:
python -m http.server 3000

# In terminal 2:
curl http://localhost:3000/index.html -UseBasicParsing | Select-Object -ExpandProperty StatusCode
```
*Expected: 200 OK.*

### 3. Verification Checklist:
- [x] **Navigation:** All in-page jump links (`#home`, `#about`, `#experience`, `#projects`, `#case-studies`, `#skills`, `#education`, `#contact`) scroll smoothly.
- [x] **Mobile Menu:** Hamburger button toggles navigation drawer, sets `aria-expanded`, and closes on link click or `Escape` key.
- [x] **Case Studies:** Modal dialogs open, trap focus, and close via Close button, Backdrop click, or `Escape` key.
- [x] **Email Copy:** Clicking "Copy Email Address" copies `suryamurugasen135@gmail.com` and shows confirmation.
- [x] **Resume Download:** Clicking "Download Resume (PDF)" triggers `Surya_M_Resume.pdf`.
- [x] **External Links:** GitHub, LinkedIn, and project repositories open safely in new tabs with `rel="noopener noreferrer"`.
- [x] **Reduced Motion:** When user prefers reduced motion, animations and auto-scroll are disabled.

---

## 🌐 Deployment Guide (Netlify & Static Hosting)

The repository is configured for automatic continuous deployment to Netlify from the `main` branch.

### Deployment Workflow:
1. Stage modified files:
   ```powershell
   git add index.html styles.css script.js README.md
   ```
2. Commit changes:
   ```powershell
   git commit -m "feat: upgrade professional positioning, case studies, and accessibility"
   ```
3. Push to GitHub:
   ```powershell
   git push origin main
   ```
4. Netlify automatically rebuilds and serves the static files within 30–60 seconds at:
   **`https://surya-murugasen-portfolio-5f4d33.netlify.app`**

### Alternative Static Hosts:
- **GitHub Pages:** Go to Repo Settings &rarr; Pages &rarr; Source: `Deploy from branch main` / `/(root)`.
- **Cloudflare Pages / Vercel:** Point repository root to `.` with empty build command.

---

## 🛠️ Customization & Maintenance

- **Updating Work Experience:** Add new timeline cards inside `<section id="experience">` in `index.html`.
- **Adding Projects:** Duplicate a project card block inside `<section id="projects">` and add the corresponding case study modal template at the bottom of `index.html`.
- **Changing Profile Image:** Replace `your-image.jpg` with an optimized 400x400 JPG/WebP image.
- **Updating Resume:** Replace `Surya_M_Resume.pdf` and synchronize details in `resume.html`.

---

## ⚠️ Known Limitations & Future Roadmap

- **Tailwind CDN Dependency:** The page currently utilizes the Tailwind CSS browser CDN script for styling. While lightweight and zero-config, a future improvement would be compiling a purged, standalone CSS stylesheet via the Tailwind CLI to remove runtime CDN script evaluation.
- **Sanitized Proprietary Work:** Details regarding the KnowledgeQ MES Traceability platform are presented as a sanitized architectural case study without proprietary client code or internal endpoints to respect confidentiality agreements.

---

## 📞 Contact

- **Name:** Surya M
- **Role:** Software Developer
- **Email:** [suryamurugasen135@gmail.com](mailto:suryamurugasen135@gmail.com)
- **Phone:** +91 9092436936
- **LinkedIn:** [linkedin.com/in/surya-m-softwareservicedeveloper](https://linkedin.com/in/surya-m-softwareservicedeveloper)
- **GitHub:** [github.com/surya-murugasen](https://github.com/surya-murugasen)
- **Live Portfolio:** [surya-murugasen-portfolio-5f4d33.netlify.app](https://surya-murugasen-portfolio-5f4d33.netlify.app)
