# CodeMedic++ 🧬

### Emotionally Interactive Explainable AI Debugging Platform

A futuristic full-stack AI debugging platform with an animated AI companion, live code analysis, change detection, and security scanning.

-----

## 📁 Project Structure

```text
CodeMedicPlusPlus/
├── frontend/
└── backend/
```

-----

## ⚡ Quick Setup (Step by Step)

### Prerequisites

* Python 3.10+
* Node.js 18+
* PostgreSQL
* Git (optional)

---

## 🗄️ Step 1 — PostgreSQL Database Setup

Open PostgreSQL and run:

```sql
CREATE DATABASE codemedic_db;
CREATE USER codemedic_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE codemedic_db TO codemedic_user;
```

----

## 🐍 Step 2 — Backend Setup

```bash
# Navigate to backend
cd CodeMedicPlusPlus/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit environment variables
cp .env.example .env
```

### Edit `.env` file:

```env
SECRET_KEY=my-super-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=codemedic_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5432
```

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start backend server
python manage.py runserver
```

Backend runs at: **http://localhost:8000**

----

## ⚛️ Step 3 — Frontend Setup

```bash
# Open a NEW terminal tab/window
cd CodeMedicPlusPlus/frontend

# Install dependencies
npm install

# Start frontend
npm start
```

Frontend runs at: **http://localhost:3000**

----

## 🚀 Open in Browser

1. Go to **http://localhost:3000**
2. Upload or paste source code
3. Click **Analyze**
4. View bug detection results, explanations, and suggested fixes

---

## 🧪 API Endpoints

| Method | Endpoint               | Description                |
| ------ | ---------------------- | -------------------------- |
| POST   | `/api/analyze/`        | Analyze source code        |
| POST   | `/api/bug-detect/`     | Detect bugs using CodeBERT |
| POST   | `/api/explain/`        | Explain detected bug       |
| POST   | `/api/fix-suggestion/` | Generate fix suggestion    |
| GET    | `/api/history/`        | View previous analyses     |
| POST   | `/api/feedback/`       | Store user feedback        |

----

## 🔥 Features

* **Real-Time Code Analysis**
* **AI-Powered Bug Detection**
* **Bug Classification (Syntax, Logical, Runtime)**
* **Code Structure Analysis using AST**
* **Bug Explanation Engine**
* **Auto-Fix Suggestions**
* **Bug History Tracking**
* **Continuous Learning through User Feedback**
* **Instant AJAX-Based Result Updates**
* **Web-Based Interactive Interface**

----

## 🛠️ Troubleshooting

**PostgreSQL connection error**

```bash
Check PostgreSQL service is running

Verify:
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

**Model loading error**

```bash
pip install transformers torch
```

**Module not found**

```bash
pip install -r requirements.txt
```

**AJAX not returning data**

```bash
Check Django server is running
Verify API URL configuration
```

----

## 📦 Tech Stack

| Layer                   | Technology                 |
| ----------------------- | -------------------------- |
| Frontend UI             | HTML, CSS                  |
| Client-side Interaction | JavaScript, jQuery (AJAX)  |
| Backend Framework       | Django (Python)            |
| AI Model                | CodeBERT (HuggingFace)     |
| Deep Learning           | PyTorch                    |
| Code Structure Analysis | Tree-sitter (AST)          |
| Bug Explanation Engine  | Python Rule-Based Logic    |
| Auto-Fix Engine         | Pattern-Based Python Logic |
| Database                | PostgreSQL                 |
| Feedback Learning       | Django + PostgreSQL        |
| Real-Time Updates       | jQuery AJAX                |
| Deployment              | Render / Railway           |

----

## 🔍 System Workflow

1. User enters source code in the web interface.
2. jQuery AJAX sends code to Django backend.
3. Django forwards code to CodeBERT.
4. Tree-sitter generates AST for structural analysis.
5. CodeBERT predicts bug type.
6. Rule-based engine explains the issue.
7. Auto-fix module suggests corrected code.
8. Results are stored in PostgreSQL.
9. User feedback is saved for future improvements.
10. Results are displayed instantly on the webpage.

----

Built with ❤️ — CodeMedic++ v1.0
