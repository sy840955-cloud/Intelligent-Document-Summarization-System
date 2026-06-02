# 🧠 Intelligent Document Summarization System

An AI-powered web application that allows users to upload documents (PDF/Text) and receive **smart, concise, and accurate summaries** using Natural Language Processing (NLP) and AI techniques.

---

## 🚀 Features

- 📄 Upload PDF / Text documents
- 🧠 AI-powered automatic summarization
- ⚡ Fast backend processing
- 🌐 Modern React frontend (Vite)
- 🗄️ Python backend (FastAPI/Flask)
- 📊 Clean and readable summaries
- 🔐 Environment variable support

---

## 🏗️ Tech Stack

**Frontend**
- React (Vite)
- JavaScript
- HTML, CSS

**Backend**
- Python
- FastAPI / Flask
- NLP models

**Libraries**
- NLTK / spaCy / Transformers
- PyPDF2 / pdfminer

---

## 📁 Project Structure

Intelligent-Document-Summarization-System/
│
├── frontend/
├── main.py
├── summarizer.py
├── utils.py
├── requirements.txt
├── package.json
├── vite.config.js
├── .env.example
└── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/sy840955-cloud/Intelligent-Document-Summarization-System.git
cd Intelligent-Document-Summarization-System
---
## 2️⃣ Backend Setup

```bash
pip install -r requirements.txt
python main.py
```

Backend runs on:

```text
http://localhost:8000
```## 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
MONGO_URI=your_mongodb_url
SECRET_KEY=your_secret_key
API_KEY=your_api_key
```

---

## 🧠 How It Works

1. User uploads a document
2. Backend extracts text from the document
3. AI/NLP model processes the content
4. Summary is generated
5. Result is displayed in the frontend

---

## 🚀 Future Improvements

- JWT Authentication
- Document History (MongoDB)
- OpenAI / Gemini Integration
- Cloud Deployment
- Mobile Responsive UI

---

## 👨‍💻 Author

**Sunny Yadav**

GitHub: https://github.com/sy840955-cloud

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!








