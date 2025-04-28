# src/semantic_baseline.py
try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'sentence-transformers'])
    from sentence_transformers import SentenceTransformer, util

from collections import Counter
import re

# Load the model with error handling
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

# Define sample phrases that represent the baseline traits
femininity_phrases = ["compassionate", "collaborative", "nurturing", "empathetic", "supportive"]
masculinity_phrases = ["assertive", "independent", "competitive", "strong", "logical"]

# Expanded keyword lists
technical_keywords = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "ruby", "php", "swift", "kotlin",
    # Web Technologies
    "html", "css", "react", "angular", "vue.js", "node.js", "express", "django", "flask",
    # Database
    "sql", "mysql", "postgresql", "mongodb", "nosql", "redis", "elasticsearch",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ci/cd", "git",
    # Data Science & AI
    "machine learning", "deep learning", "ai", "data science", "tensorflow", "pytorch", "nlp",
    # Architecture & APIs
    "microservices", "rest", "graphql", "api", "system design", "cloud architecture",
    # Methodologies
    "agile", "scrum", "devops", "test-driven development", "continuous integration"
]

soft_skills_keywords = [
    # Leadership & Management
    "leadership", "project management", "team management", "strategic planning",
    # Communication
    "communication", "presentation", "documentation", "technical writing",
    # Collaboration
    "teamwork", "collaboration", "cross-functional", "mentoring",
    # Problem Solving
    "problem-solving", "analytical", "critical thinking", "debugging",
    # Personal Traits
    "adaptability", "creativity", "innovation", "initiative",
    # Professional Skills
    "time management", "organization", "attention to detail", "multitasking"
]

# Combine all keywords
default_keywords = technical_keywords + soft_skills_keywords

def compute_similarity(reference, text):
    """
    Compute average similarity between a list of reference traits and a resume text.
    """
    if model is None:
        return 0.0
        
    try:
        reference_embeddings = model.encode(reference, convert_to_tensor=True)
        text_embedding = model.encode(text, convert_to_tensor=True)
        
        similarities = util.cos_sim(text_embedding, reference_embeddings)
        average_score = similarities.mean().item()
        return round(average_score, 4)
    except Exception as e:
        print(f"Error computing similarity: {str(e)}")
        return 0.0

def baseline_scores(resume_text):
    fem_score = compute_similarity(femininity_phrases, resume_text)
    masc_score = compute_similarity(masculinity_phrases, resume_text)
    return {
        "femininity_score": fem_score,
        "masculinity_score": masc_score
    }

def extract_keywords(text, keywords=None):
    """
    Extract keywords from text with categorization.
    Returns both frequency and categories of found keywords.
    """
    if keywords is None:
        keywords = default_keywords
    
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    
    # Get frequency of keywords
    keyword_freq = {kw: word_counts.get(kw.lower(), 0) for kw in keywords}
    
    # Categorize found keywords
    categories = {
        "technical_skills": [kw for kw in technical_keywords if word_counts.get(kw.lower(), 0) > 0],
        "soft_skills": [kw for kw in soft_skills_keywords if word_counts.get(kw.lower(), 0) > 0]
    }
    
    return {
        "frequency": keyword_freq,
        "categories": categories
    }

# Example usage (temporary test for now)
if __name__ == "__main__":
    sample_text = "A highly motivated and collaborative software engineer with a strong sense of empathy and leadership."
    scores = baseline_scores(sample_text)
    keywords = extract_keywords(sample_text)
    print("Baseline Scores:", scores)
    print("Keywords by Category:", keywords["categories"])
