"""
Universal Document Parser + Intelligent Chunking
"""
import os
import re
from typing import List
from pathlib import Path
import tiktoken
import PyPDF2
from docx import Document as DocxDocument
import fitz  # PyMuPDF

CHUNK_SIZE = 1500  # tokens
CHUNK_OVERLAP = 200  # tokens

def extract_text(file_path: str) -> str:
    """Extract text from ANY file type"""
    ext = Path(file_path).suffix.lower()
    
    if ext == '.txt':
        return Path(file_path).read_text(encoding='utf-8')
    
    elif ext == '.pdf':
        # Try PyMuPDF first (better quality)
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except:
            # Fallback to PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
    
    elif ext in ['.docx', '.doc']:
        doc = DocxDocument(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    else:
        raise ValueError(f"Unsupported file: {ext}")

def chunk_text(text: str, max_tokens: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Smart token-based chunking with overlap"""
    encoding = tiktoken.encoding_for_model("gpt-4o")
    
    # Split by paragraphs/sentences first
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    
    current_chunk = ""
    for para in paragraphs:
        para_tokens = len(encoding.encode(para))
        
        if len(encoding.encode(current_chunk + para)) > max_tokens:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para[-overlap:] if len(para) > overlap else para  # Overlap
        else:
            current_chunk += "\n\n" + para if current_chunk else para
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def process_document(file_path: str) -> dict:
    """Full pipeline: file → text → chunks"""
    print(f"📄 Processing {file_path}...")
    
    # Extract text
    text = extract_text(file_path)
    print(f"📖 {len(text)} chars extracted")
    
    # Chunk
    chunks = chunk_text(text)
    print(f"🧩 {len(chunks)} chunks created")
    
    return {
        "full_text": text,
        "chunks": chunks,
        "chunk_count": len(chunks),
        "total_tokens": sum(len(tiktoken.encoding_for_model("gpt-4o").encode(c)) for c in chunks)
    }
