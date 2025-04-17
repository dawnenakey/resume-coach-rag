# src/semantic_baseline.py
from sentence_transformers import SentenceTransformer, util
from collections import Counter
import re

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define sample phrases that represent the baseline traits
femininity_phrases = ["compassionate", "collaborative", "nurturing", "empathetic", "supportive"]
masculinity_phrases = ["assertive", "independent", "competitive", "strong", "logical"]

def compute_similarity(reference, text):
    """
    Compute average similarity between a list of reference traits and a resume text.
    """
    reference_embeddings = model.encode(reference, convert_to_tensor=True)
    text_embedding = model.encode(text, convert_to_tensor=True)
    
    similarities = util.cos_sim(text_embedding, reference_embeddings)
    average_score = similarities.mean().item()
    return round(average_score, 4)

def baseline_scores(resume_text):
    fem_score = compute_similarity(femininity_phrases, resume_text)
    masc_score = compute_similarity(masculinity_phrases, resume_text)
    return {
        "femininity_score": fem_score,
        "masculinity_score": masc_score
    }
def extract_keywords(text, keywords=None):
    if keywords is None:
        keywords = ["python", "collaborative", "cloud", "api", "empathy", "leadership", "machine learning", "azure", "aws"]
    
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    
    keyword_freq = {kw: word_counts.get(kw.lower(), 0) for kw in keywords}
    return keyword_freq

# Example usage (temporary test for now)
if __name__ == "__main__":
    sample_text = "A highly motivated and collaborative software engineer with a strong sense of empathy and leadership."
    scores = baseline_scores(sample_text)
    print("Baseline Scores:", scores)
