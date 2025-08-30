from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import uuid4
from pathlib import Path

from .storage import store, Document
from .utils import (
    ensure_upload_dir, is_pdf, is_txt,
    extract_text_from_pdf, extract_text_from_txt, UPLOAD_DIR
)

app = FastAPI(
    title = "Mini Text Extractor API",
    description = "Upload PDF/TXT → extract text + simple search (in-memory)",
    version = "0.1",
)

class UploadResponse(BaseModel):
    id: str
    filename: str
    length: int

class SearchQuery(BaseModel):
    query: str

@app.on_event("startup")
def on_startup():
    ensure_upload_dir()

@app.get("/")
def root():
    return {"status": "ok", "message": "See /docs for Swagger UI"}

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):

    filename = file.filename or ""
    if not (is_pdf(filename) or is_txt(filename)):
        raise HTTPException(status_code=400, detail="Only .pdf or .txt are supported")
    
    file_id = str(uuid4())
    save_name = f"{file_id}_{Path(filename).name}"
    dest: Path = UPLOAD_DIR / save_name

    try:
        content = await file.read()
        dest.write_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    
    try:
        if is_pdf(filename):
            text = extract_text_from_pdf(dest)
        else:
            text = extract_text_from_txt(dest)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {e}")
    
    doc = Document(id=file_id, filename=filename, content=text or "")
    store.add(doc)

    return UploadResponse(id=file_id, filename=filename, length=len(doc.content))

@app.get("/document/{doc_id}")
def get_document(doc_id: str):
    doc = store.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return JSONResponse({"id": doc.id, "filename": doc.filename, "content": doc.content})

@app.post("/search")
def search(q: SearchQuery):
    results = store.search(q.query)
    return{
        "query": q.query,
        "count": len(results),
        "results": [
            {"id": d.id, "filename": d.filename, "preview": d.content[:300]} for d in results
        ],
    }

@app.get("/documents")
def list_documents():
    docs = store.all()
    return [{"id": d.id, "filename": d.filename, "length": len(d.content)} for d in docs]

