import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import status
from app.models import UploadResponse, QueryRequest, AnswerResponse
from app import rag
from app.vectordb import VectorDB
from google import genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

PDF_DIR = "pdfs"
INDEX_DIR = "indexes"
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

# Load environment variables and create Gemini client
load_dotenv()
client = genai.Client()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set your domains in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Show user-friendly message for all validation (422) errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Invalid input. Please check your uploaded file or your JSON fields and try again."}
    )

# Stores in-memory indices/models for session (RAM only)
pdf_indices = {}

@app.post("/upload_pdf/", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    pdf_path = os.path.join(PDF_DIR, file.filename)
    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    text = rag.extract_text_pdf_with_ocr(pdf_path)
    chunks = rag.chunk_text(text)
    model, vectors = rag.embed_chunks(chunks)
    vectordb = VectorDB()
    vectordb.build(vectors, chunks)
    # Save index+chunks to disk for persistence
    index_file_prefix = os.path.join(INDEX_DIR, file.filename)
    vectordb.save(index_file_prefix)
    pdf_indices[file.filename] = (vectordb, model)
    return UploadResponse(filename=file.filename, chunks=len(chunks))

@app.post("/ask_pdf/", response_model=AnswerResponse)
async def ask_pdf(req: QueryRequest):
    index_file_prefix = os.path.join(INDEX_DIR, req.filename)
    if req.filename not in pdf_indices:
        # Load from disk if exists
        vectordb = VectorDB()
        if not os.path.exists(index_file_prefix + ".faiss"):
            raise HTTPException(status_code=404, detail="PDF not indexed.")
        vectordb.load(index_file_prefix)
        model = SentenceTransformer(rag.model_name)
        pdf_indices[req.filename] = (vectordb, model)
    else:
        vectordb, model = pdf_indices[req.filename]
    top_chunks = rag.retrieve_top_k(req.question, model, vectordb, k=3)
    answer = rag.generate_answer_gemini(client, req.question, top_chunks, req.use_outside_knowledge)
    return AnswerResponse(answer=answer, context=top_chunks)

@app.get("/")
def root():
    return {"message": "Gemini PDF RAG FastAPI is running"}
