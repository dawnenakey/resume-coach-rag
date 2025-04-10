# src/embeddings.py
import sys
from sentence_transformers import SentenceTransformer
import numpy as np

print("Loading model...", flush=True)
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded!", flush=True)

def generate_embedding(text: str):
    embedding = model.encode(text)
    return embedding

if __name__ == "__main__":
    sample_text = "Experienced software engineer with strong Python skills and machine learning expertise."
    embedding = generate_embedding(sample_text)
    embedding = np.array(embedding)
    print("Embedding shape:", embedding.shape, flush=True)
