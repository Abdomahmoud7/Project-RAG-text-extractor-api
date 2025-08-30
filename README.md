# 📄 Mini Text Extractor API

A lightweight FastAPI-based service that allows you to **upload PDF or TXT files**, **extract text**, and perform **in-memory search** across uploaded documents.

## 🚀 Features

- Upload `.pdf` or `.txt` files.
- Extract text from uploaded documents (supports UTF-8).
- Store documents in an **in-memory storage** with unique IDs.
- Retrieve full document content by ID.
- Perform simple text-based search across all documents.
- Interactive API docs via **Swagger UI**.

---

## 📁 Project Structure

```
mini-text-api/
├─ app/
│  ├─ main.py        # Main FastAPI app
│  ├─ storage.py     # In-memory document storage
│  └─ utils.py       # File handling & text extraction utilities
├─ uploads/          # Generated upload directory
├─ requirements.txt  # Dependencies
└─ .gitignore
```

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd mini-text-api
   ```

2. **(Optional) Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Application

Start the FastAPI server with **Uvicorn**:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Root health check: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📌 API Endpoints

### Root

- `GET /` → Health check.

### Upload

- `POST /upload` → Upload `.pdf` or `.txt` file.  
  Returns file ID, filename, and extracted text length.

### Document

- `GET /document/{doc_id}` → Retrieve full document by ID.

### Search

- `POST /search` → Search query across all stored documents.  
  Returns matching files with preview snippets.

### List Documents

- `GET /documents` → List all uploaded documents with metadata.

---

## 🧪 Example Usage

### Upload a PDF

```bash
curl -X POST "http://127.0.0.1:8000/upload"   -H "accept: application/json"   -H "Content-Type: multipart/form-data"   -F "file=@sample.pdf"
```

### Search for a Keyword

```bash
curl -X POST "http://127.0.0.1:8000/search"   -H "Content-Type: application/json"   -d '{"query": "introduction"}'
```

### Get a Document by ID

```bash
curl "http://127.0.0.1:8000/document/<DOCUMENT_ID>"
```

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – API framework
- [Uvicorn](https://www.uvicorn.org/) – ASGI server
- [PyPDF2](https://pypi.org/project/PyPDF2/) – PDF text extraction
- Python standard libraries (`uuid`, `pathlib`, `dataclasses`)

---

## 🔒 .gitignore

- `__pycache__/`
- `*.pyc`
- `uploads/`
- `.env`

---

## 📜 License

This project is open-source and available under the **MIT License**.

---
