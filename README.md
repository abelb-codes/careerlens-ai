# 🚀 CareerLens AI

CareerLens AI is an AI-powered resume analysis and recruitment intelligence platform designed to help job seekers improve their resumes and help recruiters discover the best candidates faster.

The platform uses document processing, natural language processing (NLP), and machine learning techniques to transform unstructured resumes into meaningful insights such as ATS scores, skill analysis, job matching, and candidate ranking.

---

## 📌 Overview

Traditional recruitment processes require recruiters to manually review hundreds of resumes, while candidates often do not understand why their applications are rejected.

CareerLens AI solves this problem by providing automated resume understanding and intelligent candidate evaluation.

The platform supports two main users:

- **Candidates** → Analyze and improve their resumes
- **Recruiters** → Screen, rank, and evaluate candidates efficiently

---

# ✨ Features

## 👤 Candidate Features

### Resume Analysis

Users can upload their resumes and receive:

- Resume quality score
- ATS compatibility score
- Resume structure evaluation
- Skill extraction
- Missing skill identification
- Improvement recommendations


### Job Compatibility Analysis

Compare a resume with a job description:

- Resume-job similarity score
- Matching skills
- Missing requirements
- Candidate strengths
- Improvement suggestions


---

## 👨‍💼 Recruiter Features

### AI Resume Screening

Recruiters can:

- Upload job descriptions
- Upload multiple resumes
- Automatically analyze candidates
- Rank candidates based on job compatibility
- Compare candidate skills


### Interview Assistant

The system generates:

- Role-specific interview questions
- Technical questions
- Candidate-focused discussion points

---

# 🏗️ System Architecture

```
                     User
                       |
                       |
              React Frontend
                       |
                       |
             Django REST Backend
                       |
        --------------------------------
        |                              |
 PostgreSQL Database              AI Engine
                                      |
                         NLP + ML Processing
                                      |
                         Resume Intelligence
```

---

# 🛠️ Technology Stack

## Frontend

- React.js
- Vite
- Tailwind CSS
- Axios
- JWT Authentication

## Backend

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Celery
- Redis

## AI Engine

- Python
- Natural Language Processing
- Sentence Transformers
- OCR Processing
- Resume Parsing
- Semantic Similarity Models
- Skill Extraction Algorithms

## Tools

- Git
- Docker
- REST APIs

---

# 📂 Project Structure

```
careerlens-ai/

│
├── career-lens-ai-main/
│   └── React Frontend Application
│
├── resume-recruiter-backend/
│   └── Django REST API
│
├── CareerLens-AI/
│   └── AI Processing Engine
│
└── README.md
```

---

# 🧠 AI Processing Pipeline

```
Resume Upload

        ↓

Document Extraction

        ↓

Text Processing

        ↓

Information Extraction

        ↓

Skill Identification

        ↓

Semantic Matching

        ↓

AI Evaluation Report
```

---

# 🔐 Security

CareerLens AI implements:

- JWT authentication
- Protected API endpoints
- File upload validation
- Environment variable configuration
- Secure user data handling

---

# ⚙️ Installation & Setup

## Clone Repository

```bash
git clone https://github.com/abelb-codes/careerlens-ai.git

cd careerlens-ai
```

---

# Backend Setup

Navigate to backend:

```bash
cd resume-recruiter-backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start backend:

```bash
python manage.py runserver
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

# Frontend Setup

Navigate to frontend:

```bash
cd career-lens-ai-main
```

Install dependencies:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

# Environment Variables

## Backend `.env`

Example:

```
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
DEBUG=True
```

## Frontend `.env`

Example:

```
VITE_API_URL=http://127.0.0.1:8000/api
```

---

# 🧪 Testing

Backend:

```bash
python manage.py test
```

AI Engine:

```bash
pytest
```

---

# 🚀 Deployment

The recommended deployment architecture:

```
Frontend
   |
   | → Vercel

Backend
   |
   | → Cloud Server

Database
   |
   | → PostgreSQL

AI Engine
   |
   | → AI Service/API
```

---

# 🔮 Future Improvements

Planned features:

- Advanced LLM-powered resume feedback
- Automated resume improvement generation
- Job recommendation system
- Real-time recruiter collaboration
- Improved skill ontology
- Cloud-based AI inference
- Resume generation assistant

---

# 👨‍💻 Author

**Abel Bekele**

Computer Science Graduate | Software Developer | AI Enthusiast

GitHub:
https://github.com/abelb-codes

---

⭐ If you find CareerLens AI useful, consider giving the project a star.
