import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
from app.vectordb import VectorDB
import os

model_name = 'all-MiniLM-L6-v2'

def extract_text_pdf_with_ocr(pdf_path, dpi=200):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pg_text = page.extract_text()
            if pg_text:
                text += pg_text + "\n"
    if not text.strip():
        images = convert_from_path(pdf_path, dpi=dpi)
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
    return chunks

def embed_chunks(chunks):
    model = SentenceTransformer(model_name)
    vectors = model.encode(chunks, show_progress_bar=False)
    return model, vectors

def retrieve_top_k(query, model, db, k=3):
    q_emb = model.encode([query])[0]
    top_chunks = db.search(q_emb, k=k)
    return top_chunks

def generate_answer_gemini(client, question, retrieved_chunks, use_outside_knowledge=False,
                           model_name="models/gemini-1.5-flash-latest"):
    context = "\n\n".join([
        f"Context {i+1}:\n{chunk}"
        for i, chunk in enumerate(retrieved_chunks)
    ])
    if use_outside_knowledge:
        sys_prompt = (
            "You are a helpful assistant. Answer the user's question using the provided PDF context. "
            "You MAY also include helpful outside knowledge, but cite the PDF if it has the answer."
        )
    else:
        sys_prompt = (
            "You are a helpful assistant. Answer using ONLY the PDF context below. "
            "If the answer isn't present, say so (do NOT add outside knowledge)."
        )
    prompt = f"""{sys_prompt}

Context:
{context}
Question: {question}
Answer:"""
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    return response.text.strip()
