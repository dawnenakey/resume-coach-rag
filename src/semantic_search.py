# src/semantic_search.py
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Initialize the same model from embeddings.py
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarities(query_text: str, corpus_texts: list):
    """
    Compute cosine similarity scores between a query (resume) and a list of corpus texts (job postings).
    
    Returns:
        A sorted list of tuples: (text, similarity_score)
    """
    query_embedding = model.encode(query_text, convert_to_tensor=True)
    corpus_embeddings = model.encode(corpus_texts, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    
    # Pair each text with its score and sort by score descending
    scored_texts = sorted(zip(corpus_texts, cosine_scores.cpu().numpy()), key=lambda x: x[1], reverse=True)
    return scored_texts

if __name__ == "__main__":
    # Example texts
    resume_text = "Experienced software engineer with strong background in Python and machine learning."
    job_texts = [
        "Looking for a Python developer with expertise in machine learning.",
        "Front-end developer needed with experience in React.",
        "Data scientist required with advanced analytical skills."
    ]
    
    similarities = compute_similarities(resume_text, job_texts)
    for job, score in similarities:
        print(f"Job: {job}\nSimilarity Score: {score:.4f}\n")
