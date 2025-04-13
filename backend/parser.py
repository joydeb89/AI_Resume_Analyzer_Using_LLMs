import fitz  # PyMuPDF
import docx2txt
import os

def parse_resume(file_path: str) -> str:
    """
    Parses resume from PDF or DOCX file and returns extracted text.
    """
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Upload PDF or DOCX.")

def extract_text_from_pdf(path: str) -> str:
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(path: str) -> str:
    return docx2txt.process(path)

def parse_job_description(jd_text: str) -> str:
    return jd_text.strip()

