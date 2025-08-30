from pathlib import Path
from PyPDF2 import PdfReader

UPLOAD_DIR = Path("uploads")

def ensure_upload_dir():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def is_pdf(filename: str) -> bool:
    return filename.lower().endswith(".pdf")

def is_txt(filename: str) -> bool:
    return filename.lower().endswith(".txt")

def extract_text_from_pdf(filepath: Path) -> str:
    text_parts: list[str] = []
    with filepath.open("rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts).strip()

def extract_text_from_txt(filepath: Path) -> str:

    return filepath.read_text(encoding="utf-8", errors="ignore")

