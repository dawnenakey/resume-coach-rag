# src/semantic_baseline.py
import torch
import streamlit as st
from sentence_transformers import SentenceTransformer, util
import numpy as np
from collections import Counter
import re
from typing import Dict, List, Any
import spacy

@st.cache_resource
def load_model():
    """Load and cache the sentence transformer model"""
    try:
        return SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

@st.cache_resource
def load_spacy():
    """Load and cache the spaCy model"""
    try:
        return spacy.load("en_core_web_sm")
    except Exception as e:
        st.error(f"Error loading spaCy model: {str(e)}")
        return None

# Define sample phrases that represent the baseline traits
femininity_phrases = [
    # Collaborative traits
    "compassionate", "collaborative", "nurturing", "empathetic", "supportive",
    # Communication traits
    "communicative", "listening", "interpersonal", "relationship-building",
    # Team-oriented traits
    "team-player", "cooperative", "helpful", "mentoring", "facilitating",
    # Emotional Intelligence
    "emotional intelligence", "empathy", "understanding", "patient", "caring"
]

masculinity_phrases = [
    # Leadership traits
    "assertive", "independent", "competitive", "strong", "logical",
    # Action-oriented traits
    "driven", "ambitious", "decisive", "direct", "results-oriented",
    # Technical traits
    "analytical", "strategic", "technical", "systematic",
    # Achievement traits
    "achieved", "led", "executed", "implemented", "delivered"
]

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

def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute semantic similarity between two texts using cached model
    """
    model = load_model()
    if not model:
        return 0.0
    
    try:
        # Encode the texts
        embedding1 = model.encode(text1, convert_to_tensor=True)
        embedding2 = model.encode(text2, convert_to_tensor=True)
        
        # Compute cosine similarity
        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        return float(similarity)
    except Exception as e:
        st.error(f"Error computing similarity: {str(e)}")
        return 0.0

def baseline_scores(resume_text):
    """
    Calculate gender baseline scores with improved normalization.
    
    Args:
        resume_text (str): The text content of the resume
        
    Returns:
        dict: Dictionary containing normalized femininity and masculinity scores
    """
    # Convert resume text to lowercase for better matching
    resume_text = resume_text.lower()
    
    # Calculate similarity scores for each phrase
    fem_scores = [compute_similarity(phrase, resume_text) for phrase in femininity_phrases]
    masc_scores = [compute_similarity(phrase, resume_text) for phrase in masculinity_phrases]
    
    # Take the average of top 5 scores for each category
    fem_scores.sort(reverse=True)
    masc_scores.sort(reverse=True)
    
    top_fem_score = sum(fem_scores[:5]) / 5 if fem_scores else 0
    top_masc_score = sum(masc_scores[:5]) / 5 if masc_scores else 0
    
    # Normalize scores to ensure they sum to less than 1
    total = top_fem_score + top_masc_score
    if total > 0:
        normalized_fem = top_fem_score / (total * 1.5)  # Divide by 1.5 to ensure sum < 1
        normalized_masc = top_masc_score / (total * 1.5)
    else:
        normalized_fem = 0
        normalized_masc = 0
    
    return {
        "femininity_score": normalized_fem,
        "masculinity_score": normalized_masc
    }

def extract_keywords(text: str) -> Dict[str, Any]:
    """
    Extract keywords from text using cached spaCy model
    """
    nlp = load_spacy()
    if not nlp:
        return {"frequency": {}, "categories": {"technical_skills": [], "soft_skills": []}}
    
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    
    # Get frequency of keywords
    keyword_freq = {kw: word_counts.get(kw.lower(), 0) for kw in default_keywords}
    
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
