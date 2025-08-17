# 🏦 Loan Default Risk Scoring API & 📄 AI-Powered PDF Context Retrieval Chatbot (RAG)

This repository contains two production-ready AI microservices:
1. **Loan Default Risk Scoring API:** Real-time borrower risk scoring with ML model and analytics.
2. **PDF RAG Chatbot:** Upload any PDF, index via semantic search, and answer queries with a Retrieval-Augmented Generation (RAG) pipeline using FastAPI and Gemini LLM.

---

## 🚀 Project Overview

### Loan Default Risk Scoring API
An end-to-end ML solution for predicting borrower loan default risk. Includes robust data science, model training, evaluation, and RESTful FastAPI backend for score serving and analytics.

### PDF Context Retrieval Chatbot (RAG)
A backend system for ingesting PDFs, extracting text segments, storing chunk embeddings in FAISS, and answering questions using the latest Gemini LLM, all exposed via FastAPI REST endpoints.

---

## 📦 Features

### Loan Risk API
- **Data Science & ML**
  - Data cleaning, preprocessing, feature engineering
  - RandomForest model (SMOTE balanced, GridSearchCV tuned)
  - Model evaluation: ROC-AUC, confusion matrix, feature importances
  - Feature importance reports

- **RESTful API**
  - `/predict`: POST - Predicts loan default probability from borrower data
  - `/model-info`: GET - Returns model meta & top features
  - Robust Pydantic input validation, error handling

- **Visualizations**
  - Distribution plots, class imbalance, ROC curve, feature importances
  - See `/notebooks/` and `/Output/` for artifacts and PNG plots

---

### PDF RAG Chatbot
- **PDF Processing & Retrieval**
  - Upload PDF files
  - Extract selectable text, fallback to OCR if scanned
  - Split into overlapping chunks
  - Generate semantic embeddings (`all-MiniLM-L6-v2`)
  - Store embeddings in a FAISS vector DB with save/load support

- **Retrieval-Augmented Generation (RAG)**
  - Retrieve top relevant chunks for any query
  - Use Google Gemini LLM to answer based on retrieved chunk context
  - Return LLM answer + source context passages

- **FastAPI Backend**
  - `/upload_pdf`: POST - Upload a PDF and index for semantic search
  - `/ask_pdf`: POST - Question answering with PDF context
  - Input validation and error handling via Pydantic
  - CORS-enabled, clean modular code

---

## 🗂️ Directory Structure

```
Chat_pdf/
  ├── app/
  ├── pdfs/
  ├── indexes/
  ├── requirements.txt
  └── README.md

Loan_Defaulters/
  ├── app/
  ├── artifacts/
  ├── notebooks/
  ├── requirements.txt
  └── README.md

LICENSE
README.md
```

---

## 🛠️ Setup & Run

### 1. Clone the repository

```
git clone https://github.com/Yuvaraj878/6sconsulting-loan-risk-and-rag.git
```

### 2. Install dependencies

```
fastapi==0.113.0
uvicorn[standard]==0.23.1
pydantic==2.8.0
scikit-learn==1.3.0
pandas==2.0.1
imblearn==0.1.10
matplotlib==3.7.1
seaborn==0.12.2
joblib==1.3.1
openpyxl==3.1.2
```

```
fastapi
uvicorn
python-multipart
pdfplumber
pytesseract
pdf2image
Pillow
sentence-transformers
scikit-learn
faiss-cpu
python-dotenv
google-genai

```


### 3. Configure environment variables

Create a `.env` file in the project root and add (for Gemini PDF RAG):

```
GOOGLE_API_KEY=your_google_genai_api_key_here
```


### 4. Run FastAPI Servers

Loan Risk API:
```
uvicorn app.main:app --reload
```


PDF RAG Chatbot:
```
uvicorn app.main:app --reload
```


(If running both, use different ports: add `--port 8001` etc.)

---

## 🎯 API Endpoints

### Loan Default Risk Scoring API

#### 1. Predict Default Risk
- **POST** `/predict`
- Body Example:
```
{
"Age": 52,
"Income": 45000,
"LoanAmount": 120000,
"CreditScore": 590,
"MonthsEmployed": 20,
"NumCreditLines": 1,
"InterestRate": 13.2,
"LoanTerm": 48,
"DTIRatio": 0.77,
"Education": "High School",
"EmploymentType": "Unemployed",
"MaritalStatus": "Single",
"HasMortgage": "No",
"HasDependents": "No",
"LoanPurpose": "Auto",
"HasCoSigner": "Yes"
}
```

- **Response**:
```
{
"risk_score": 0.56,
"predicted_default": true
}
```


#### 2. Model Info/Feature Importances
- **GET** `/model-info`
- Returns metadata and most important features.

---

### PDF RAG Chatbot API

#### 1. Upload PDF
- **POST** `/upload_pdf/`
- Form-data: `file` (PDF file)
- Response:

```
{
"filename": "ML_Resume.pdf",
"chunks": 25
}
```


#### 2. Ask PDF a Question
- **POST** `/ask_pdf/`
- JSON:

```
{
"filename": "ML_Resume.pdf",
"question": "What are the candidate's main achievements?",
"use_outside_knowledge": false
}
```

- Response:
```
{
"answer": "The candidate has experience in ...",
"context": [
"Context chunk 1 ...",
"Context chunk 2 ...",
"Context chunk 3 ..."
]
}
```


#### 3. Healthcheck
- **GET** `/`
- Returns `{ "message": "Gemini PDF RAG FastAPI is running" }`

---

## 📊 Visualizations

See `/notebooks/` and `/Output/` for:
- Class imbalance
- Feature distributions
- Correlation heatmaps
- Feature importances
- ROC curves
- Example screenshots for Postman and Swagger UI

---

## 💡 Insights & Usage Scenarios

- Loan API helps assess borrower risk, set fair interest rates, and comply with lending rules.
- PDF RAG chatbot enables semantic search against any uploaded document, reference-backed answers.
- Designed for extensibility, production, and both internal analytic/expert user scenarios.

---

## ⚙️ Notes & Recommendations

- FAISS index and chunks are saved with the PDF’s filename as key; do not delete `/indexes/` between runs to retain persistent search.
- Gemini API key (for PDF RAG) must be in `.env`.
- For advanced scaling or real-time analytics, consider cloud vector DBs or model artifact stores.

---

## 📝 Retraining & Updating

- For Loan API, update artifacts in `/app/artifacts/` after retraining models and feature pickles.
- For PDF RAG, re-upload PDFs or refresh index files for new documents.

---

## 📫 Contact & Contributing

Questions, issues, PRs welcome!  
Fork, star, or raise issues for feature requests.

**Email:** [ai.yuvaraj21@gmail.com]

---

## 📜 License

Apache 2.0 License © 6s Consulting — AI Mini-Project Challenge.

---

## 🙏 Acknowledgements

- Google Gemini GenAI
- FastAPI framework
- FAISS/Chroma/Pinecone projects
- Sentence Transformers and Scikit-learn communities

---

**Explore real-world risk analytics and next-gen document AI—powered by modern open source ML!**
