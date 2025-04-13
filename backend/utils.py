from backend.model import get_keyword_model
import re

# Load once
kw_model = get_keyword_model()

def extract_keywords(text: str, num_keywords: int = 15) -> list:
    cleaned = clean_text(text)
    keywords = kw_model.extract_keywords(
        cleaned,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=num_keywords
    )
    return list(set([kw[0].lower() for kw in keywords if len(kw[0]) > 2]))

def clean_text(text: str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()
