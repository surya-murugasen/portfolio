import os
import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml.shared import OxmlElement, qn

def add_heading_with_border(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(15, 23, 42)
    
    p_format = p.paragraph_format
    p_format.space_after = Pt(3)
    p_format.space_before = Pt(8)
    
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '2563EB') # Blue accent
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p

def create_resume_docx(output_path):
    doc = Document()
    
    # 0.5 inch margins for sleek modern layout
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.45)
        section.bottom_margin = Inches(0.45)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(9.5)
    
    # --- HEADER ---
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_after = Pt(1)
    p_name.paragraph_format.space_before = Pt(0)
    run_name = p_name.add_run("SURYA M")
    run_name.bold = True
    run_name.font.size = Pt(18)
    run_name.font.color.rgb = RGBColor(15, 23, 42)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(3)
    p_title.paragraph_format.space_before = Pt(0)
    r_title = p_title.add_run("SOFTWARE DEVELOPER | FULL-STACK & AI SYSTEMS")
    r_title.bold = True
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(37, 99, 235)
    
    p_contact = doc.add_paragraph()
    p_contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_contact.paragraph_format.space_after = Pt(6)
    p_contact.paragraph_format.space_before = Pt(0)
    c_run = p_contact.add_run("suryamurugasen135@gmail.com  |  +91 9092436936  |  Coimbatore, Tamil Nadu, India\nlinkedin.com/in/surya-m-softwareservicedeveloper  |  github.com/surya-murugasen  |  surya-murugasen-portfolio-5f4d33.netlify.app")
    c_run.font.size = Pt(8.5)
    c_run.font.color.rgb = RGBColor(71, 85, 105)
    
    # --- PROFESSIONAL SUMMARY ---
    add_heading_with_border(doc, "PROFESSIONAL SUMMARY")
    p_sum = doc.add_paragraph(
        "Results-driven Software Developer with full-time professional experience building enterprise applications and full-stack web and mobile systems. "
        "Currently working as a Software Developer at KnowledgeQ, engineering backend microservices and traceability workflows for enterprise Manufacturing Execution Systems (MES) "
        "and deploying React Native iOS FinTech applications. Proficient in Node.js, Express.js, TypeScript, React.js, React Native, Flutter, and MySQL. "
        "Demonstrated expertise in real-time event-driven systems (Socket.IO, HMAC-SHA256), vector retrieval AI (FAISS, RAG, PyMuPDF), and computer vision (Ultralytics YOLO, OpenCV)."
    )
    p_sum.paragraph_format.space_after = Pt(6)
    p_sum.paragraph_format.space_before = Pt(0)
    p_sum.paragraph_format.line_spacing = 1.15
    
    # --- PROFESSIONAL EXPERIENCE ---
    add_heading_with_border(doc, "PROFESSIONAL EXPERIENCE")
    
    # 1. KnowledgeQ
    t_exp1 = doc.add_table(rows=1, cols=2)
    t_exp1.autofit = False
    t_exp1.columns[0].width = Inches(5.8)
    t_exp1.columns[1].width = Inches(1.7)
    
    c0 = t_exp1.rows[0].cells[0].paragraphs[0]
    c0.paragraph_format.space_after = Pt(1)
    r1 = c0.add_run("Software Developer  ")
    r1.bold = True
    r1.font.size = Pt(10)
    r1_comp = c0.add_run("|  KnowledgeQ, Coimbatore (Full-time · On-site)")
    r1_comp.bold = True
    r1_comp.font.color.rgb = RGBColor(37, 99, 235)
    
    c1 = t_exp1.rows[0].cells[1].paragraphs[0]
    c1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    c1.paragraph_format.space_after = Pt(1)
    r_date1 = c1.add_run("Jun 2025 – Present")
    r_date1.bold = True
    r_date1.font.size = Pt(9.5)
    
    bullets_kq = [
        "Develop and maintain enterprise Manufacturing Execution System (MES) Traceability applications to improve production tracking, product traceability, and manufacturing workflows.",
        "Build and enhance scalable backend services using Node.js, Express.js, TypeScript, REST APIs, and MySQL.",
        "Develop and maintain React Native iOS applications for FinTech solutions, delivering new features, resolving production issues, and supporting App Store releases.",
        "Collaborate with cross-functional teams including developers, QA engineers, business analysts, and stakeholders in an Agile/Scrum environment.",
        "Participate in application debugging, performance optimization, code reviews, testing, and deployment activities.",
        "Work with Git for version control and contribute to clean, maintainable, and production-ready code following software engineering best practices."
    ]
    for b in bullets_kq:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(1.5)
        bp.paragraph_format.space_before = Pt(0)
        bp.paragraph_format.line_spacing = 1.1
        run_b = bp.add_run(b)
        run_b.font.size = Pt(9.2)
        
    p_tkq = doc.add_paragraph()
    p_tkq.paragraph_format.space_before = Pt(2)
    p_tkq.paragraph_format.space_after = Pt(6)
    rt_l = p_tkq.add_run("Tech Stack: ")
    rt_l.bold = True
    rt_l.font.size = Pt(9)
    rt_v = p_tkq.add_run("Node.js, Express.js, TypeScript, React.js, React Native (iOS), Flutter, MySQL, REST APIs, Git, Xcode, Agile/Scrum")
    rt_v.font.size = Pt(9)
    
    # 2. Qtree
    t_exp2 = doc.add_table(rows=1, cols=2)
    t_exp2.autofit = False
    t_exp2.columns[0].width = Inches(5.8)
    t_exp2.columns[1].width = Inches(1.7)
    
    c0 = t_exp2.rows[0].cells[0].paragraphs[0]
    c0.paragraph_format.space_after = Pt(1)
    r2 = c0.add_run("Full Stack Web Development Trainee  ")
    r2.bold = True
    r2.font.size = Pt(10)
    r2_comp = c0.add_run("|  Qtree Technologies, Coimbatore")
    r2_comp.bold = True
    r2_comp.font.color.rgb = RGBColor(71, 85, 105)
    
    c1 = t_exp2.rows[0].cells[1].paragraphs[0]
    c1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    c1.paragraph_format.space_after = Pt(1)
    r_date2 = c1.add_run("July 2024 – Dec 2024")
    r_date2.bold = True
    r_date2.font.size = Pt(9.5)
    
    bullets_qt = [
        "Developed responsive web applications and built RESTful APIs using React.js, Node.js, Express.js, HTML, CSS, JavaScript, and MySQL, successfully integrating frontend interfaces with backend services.",
        "Collaborated in Agile development teams using Git and GitHub, actively performing debugging, testing, and performance optimization."
    ]
    for b in bullets_qt:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(1.5)
        bp.paragraph_format.space_before = Pt(0)
        bp.paragraph_format.line_spacing = 1.1
        run_b = bp.add_run(b)
        run_b.font.size = Pt(9.2)
        
    p_tqt = doc.add_paragraph()
    p_tqt.paragraph_format.space_before = Pt(2)
    p_tqt.paragraph_format.space_after = Pt(6)
    rt_l = p_tqt.add_run("Tech Stack: ")
    rt_l.bold = True
    rt_l.font.size = Pt(9)
    rt_v = p_tqt.add_run("React.js, Node.js, Express.js, HTML5, CSS3, JavaScript (ES6+), MySQL, REST APIs, Git")
    rt_v.font.size = Pt(9)
    
    # --- FEATURED PROJECTS ---
    add_heading_with_border(doc, "FEATURED TECHNICAL PROJECTS")
    
    # Project 1: TeamTrack
    p_p1 = doc.add_paragraph()
    p_p1.paragraph_format.space_after = Pt(1)
    p_p1.paragraph_format.space_before = Pt(2)
    r = p_p1.add_run("TeamTrack – Real-Time Project Management Platform")
    r.bold = True
    r.font.size = Pt(9.8)
    
    bullets_p1 = [
        "Architected an enterprise project tracking platform featuring secure JWT authentication and role-based access control (RBAC).",
        "Engineered real-time collaboration engines using Socket.IO room broadcasting, departmental dashboards, notifications, and document versioning.",
        "Designed modular TypeScript backend architecture, server-to-server HMAC-SHA256 authentication, and optimized relational MySQL queries."
    ]
    for b in bullets_p1:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(1.5)
        bp.paragraph_format.space_before = Pt(0)
        run_b = bp.add_run(b)
        run_b.font.size = Pt(9.2)
    p_tp1 = doc.add_paragraph()
    p_tp1.paragraph_format.space_before = Pt(1)
    p_tp1.paragraph_format.space_after = Pt(5)
    rt_l = p_tp1.add_run("Tech Stack: ")
    rt_l.bold = True
    rt_l.font.size = Pt(8.8)
    p_tp1.add_run("Next.js, Node.js, Express, TypeScript, MySQL (Sequelize), Socket.IO, HMAC-SHA256, JWT, Git").font.size = Pt(8.8)
    
    # Project 2: VisionGuard AI
    p_p2 = doc.add_paragraph()
    p_p2.paragraph_format.space_after = Pt(1)
    p_p2.paragraph_format.space_before = Pt(2)
    r = p_p2.add_run("VisionGuard AI – Enterprise Anti-Face Spoofing System")
    r.bold = True
    r.font.size = Pt(9.8)
    
    bullets_p2 = [
        "Built a deep learning anti-face spoofing system using Ultralytics YOLO and OpenCV to detect presentation attacks in real time.",
        "Engineered live webcam frame processing with Flask-SocketIO streaming microservice, detecting printed photos and digital video replays.",
        "Integrated Python AI inferencing with a React admin dashboard and Node.js SQLite audit logging microservice."
    ]
    for b in bullets_p2:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(1.5)
        bp.paragraph_format.space_before = Pt(0)
        run_b = bp.add_run(b)
        run_b.font.size = Pt(9.2)
    p_tp2 = doc.add_paragraph()
    p_tp2.paragraph_format.space_before = Pt(1)
    p_tp2.paragraph_format.space_after = Pt(5)
    rt_l = p_tp2.add_run("Tech Stack: ")
    rt_l.bold = True
    rt_l.font.size = Pt(8.8)
    p_tp2.add_run("Python, Ultralytics YOLO (v8/v11), OpenCV, Flask-SocketIO, Node.js, React, SQLite").font.size = Pt(8.8)
    
    # Project 3: RAG
    p_p3 = doc.add_paragraph()
    p_p3.paragraph_format.space_after = Pt(1)
    p_p3.paragraph_format.space_before = Pt(2)
    r = p_p3.add_run("RAG Document Intelligence – Citation Engine & Multi-User Isolation")
    r.bold = True
    r.font.size = Pt(9.8)
    
    bullets_p3 = [
        "Engineered an asynchronous Retrieval-Augmented Generation platform using FastAPI, FAISS vector indexing, and PyMuPDF text extraction.",
        "Implemented strict page-isolated chunking, interactive PDF viewer (pdfjs-dist) with jump citations, and Chunk Inspector measuring token overlap.",
        "Validated server-side session authentication, document ownership authorization, and vector tenant isolation across 88 automated regression tests."
    ]
    for b in bullets_p3:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(1.5)
        bp.paragraph_format.space_before = Pt(0)
        run_b = bp.add_run(b)
        run_b.font.size = Pt(9.2)
    p_tp3 = doc.add_paragraph()
    p_tp3.paragraph_format.space_before = Pt(1)
    p_tp3.paragraph_format.space_after = Pt(6)
    rt_l = p_tp3.add_run("Tech Stack: ")
    rt_l.bold = True
    rt_l.font.size = Pt(8.8)
    p_tp3.add_run("Python 3.12, FastAPI, FAISS (IndexFlatIP), PyMuPDF, React 19, TypeScript, SQLite (Alembic), Docker Compose").font.size = Pt(8.8)
    
    # --- EDUCATION & CERTIFICATIONS ---
    add_heading_with_border(doc, "EDUCATION & CERTIFICATIONS")
    
    t_edu = doc.add_table(rows=1, cols=2)
    t_edu.autofit = False
    t_edu.columns[0].width = Inches(5.8)
    t_edu.columns[1].width = Inches(1.7)
    
    c0 = t_edu.rows[0].cells[0].paragraphs[0]
    c0.paragraph_format.space_after = Pt(1)
    r_deg = c0.add_run("B.E. – Computer Science and Engineering  ")
    r_deg.bold = True
    r_deg.font.size = Pt(9.5)
    c0.add_run("\nHindusthan College of Engineering and Technology, Coimbatore").font.size = Pt(9)
    
    c1 = t_edu.rows[0].cells[1].paragraphs[0]
    c1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    c1.paragraph_format.space_after = Pt(1)
    r_cgpa = c1.add_run("2020 – 2024\nCGPA: 8.21 / 10")
    r_cgpa.bold = True
    r_cgpa.font.size = Pt(9)
    
    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.space_before = Pt(3)
    p_cert.paragraph_format.space_after = Pt(6)
    r_ct = p_cert.add_run("Certification: ")
    r_ct.bold = True
    r_ct.font.size = Pt(9)
    p_cert.add_run("Full Stack Web Development (6-Month Intensive Training) – Qtree Technologies (July 2024 – Dec 2024)").font.size = Pt(9)
    
    # --- TECHNICAL SKILLS ---
    add_heading_with_border(doc, "TECHNICAL SKILLS")
    
    skills = [
        ("Programming Languages: ", "JavaScript (ES6+), TypeScript, Java, Python, Dart, SQL"),
        ("Backend & APIs: ", "Node.js, Express.js, RESTful APIs, Microservices, Socket.IO, HMAC-SHA256, JWT, Middleware"),
        ("Frontend & Mobile: ", "React.js, Next.js, React Native (iOS), Flutter, HTML5, CSS3, Tailwind CSS, Vite"),
        ("Databases: ", "MySQL (Indexing, Normalization, Query Tuning), SQLite, PostgreSQL, Oracle, Sequelize ORM"),
        ("AI & Computer Vision: ", "Ultralytics YOLO (v8/v11), OpenCV, FAISS Vector Indexing, PyMuPDF, RAG Architecture, Prompt Engineering"),
        ("Developer Tools: ", "Git, GitHub, Docker, Postman, Xcode, Jira, Splunk, Firebase, Playwright, Vitest, Pytest"),
        ("Core Engineering: ", "Object-Oriented Programming (OOP), Data Structures & Algorithms (DSA), System Design, Agile/Scrum")
    ]
    for lbl, val in skills:
        sp = doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(1.5)
        sp.paragraph_format.space_before = Pt(0)
        rl = sp.add_run(lbl)
        rl.bold = True
        rl.font.size = Pt(9)
        rv = sp.add_run(val)
        rv.font.size = Pt(9)
        
    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == '__main__':
    out_file = sys.argv[1] if len(sys.argv) > 1 else "c:/Projects/Production_Projects/portfolio/Surya M.docx"
    create_resume_docx(out_file)
