from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

from pypdf import PdfReader
import google.generativeai as genai
import os
import tempfile

from dotenv import load_dotenv
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

faiss_index = None
pdf_chunks = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("=" * 50)
print("ENV FILE:", ENV_PATH)
print("GEMINI KEY FOUND:", bool(GEMINI_API_KEY))
print("=" * 50)


app = FastAPI(title="AI Document Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_model = None

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)

        print("\nAVAILABLE MODELS:\n")

        for model in genai.list_models():
            print(model.name)

        # USE WORKING MODEL
        gemini_model = genai.GenerativeModel(
            "models/gemini-2.5-flash"
        )

        print("Gemini Initialized Successfully")

    except Exception as e:
        print("Gemini Error:", e)
else:
    print("GEMINI_API_KEY not found")


summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

pdf_text_store = ""

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {
        "message": "AI Document Assistant Running"
    }

@app.post("/summarize-text")
def summarize_text(req: TextRequest):

    text = req.text.strip()

    if not text:
        return {
            "summary": "Please enter text"
        }

    if len(text.split()) < 20:
        return {
            "summary": text
        }

    try:

        result = summarizer(
            text,
            max_length=80,
            min_length=20,
            do_sample=False
        )

        return {
            "summary": result[0]["summary_text"]
        }

    except Exception as e:

        return {
            "summary": str(e)
        }


@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    global pdf_text_store
    global faiss_index
    global pdf_chunks

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Please upload a PDF file only"
        }

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            content = await file.read()

            temp_file.write(content)

            temp_path = temp_file.name

        reader = PdfReader(temp_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        pdf_text_store = text

        # Create chunks
        pdf_chunks = []

        chunk_size = 500

        for i in range(0, len(text), chunk_size):
            pdf_chunks.append(
                text[i:i + chunk_size]
            )

        embeddings = embedding_model.encode(
            pdf_chunks
        )

        dimension = embeddings.shape[1]

        faiss_index = faiss.IndexFlatL2(
            dimension
        )

        faiss_index.add(
            np.array(embeddings).astype(
                "float32"
            )
        )

        return {
            "message": "PDF uploaded successfully",
            "characters": len(text)
        }

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.get("/pdf-summary")
def pdf_summary():

    global pdf_text_store

    if not pdf_text_store:
        return {
            "summary": "No PDF uploaded"
        }

    try:

        result = summarizer(
            pdf_text_store[:4000],
            max_length=120,
            min_length=40,
            do_sample=False
        )

        return {
            "summary": result[0]["summary_text"]
        }

    except Exception as e:

        return {
            "summary": str(e)
        }

@app.post("/ask-pdf")
async def ask_pdf(
    question: str = Form(...)
):

    global pdf_text_store
    global faiss_index
    global pdf_chunks

    if not pdf_text_store:
        return {
            "answer": "Please upload PDF first"
        }

    if gemini_model is None:
        return {
            "answer": "Gemini API key not loaded. Check .env file."
        }

    try:

        # Create question embedding
        question_embedding = embedding_model.encode(
            [question]
        )

        # Search top 3 chunks
        D, I = faiss_index.search(
            np.array(question_embedding).astype("float32"),
            3
        )

        context = "\n".join(
            [pdf_chunks[idx] for idx in I[0]]
        )

        prompt = f"""
Answer only using the provided context.

CONTEXT:
{context}

QUESTION:
{question}
"""

        response = gemini_model.generate_content(
            prompt
        )

        return {
            "answer": response.text
        }

    except Exception as e:

        return {
            "answer": str(e)
        }
