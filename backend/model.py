from sentence_transformers import SentenceTransformer
from keybert import KeyBERT

# Load embedding model once
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load KeyBERT with the same model
keyword_model = KeyBERT(model=embedding_model)

def get_embedding_model():
    return embedding_model

def get_keyword_model():
    return keyword_model


