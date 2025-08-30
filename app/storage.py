from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class Document:
    id: str
    filename: str
    content: str

class InMemoryStore:
    def __init__(self):
        self._docs: Dict[str, Document] = {}
    
    def add(self, doc: Document):
        self._docs[doc.id] = doc
    
    def get(self, doc_id: str) -> Document | None:
        return self._docs.get(doc_id)
    
    def all(self) -> List[Document]:
        return list(self._docs.values())
    
    def search(self, query: str) -> List[Document]:
        q = query.lower().strip()

        if not q:
            return []
        return [d for d in self._docs.values() if q in d.content.lower() or q in d.filename.lower()]

store = InMemoryStore()

