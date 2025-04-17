# src/scoring.py

from sentence_transformers import SentenceTransformer, util

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity_score(text1: str, text2: str) -> float:
    """
    Compute semantic similarity between two texts.
    Returns a score between 0 and 1.
    """
    embeddings = model.encode([text1, text2], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1])
    return float(score.item())
