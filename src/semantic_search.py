# src/semantic_search.py
from sentence_transformers import SentenceTransformer, util
from resume_parser import parse_pdf_resume, parse_docx_resume
import os

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarities(resume_text, job_texts):
    query_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embeddings = model.encode(job_texts, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, job_embeddings)[0]

    results = sorted(
        zip(job_texts, cosine_scores.cpu().numpy()),
        key=lambda x: x[1],
        reverse=True
    )
    return results

if __name__ == "__main__":
    # === Load resume from file ===
    resume_dir = "data/sample_resumes"
    resume_pdf = os.path.join(resume_dir, "sample_resume.pdf")
    resume_docx = os.path.join(resume_dir, "sample_resume.docx")

    if os.path.exists(resume_pdf):
        print("Using resume:", resume_pdf)
        resume_text = parse_pdf_resume(resume_pdf)
    elif os.path.exists(resume_docx):
        print("Using resume:", resume_docx)
        resume_text = parse_docx_resume(resume_docx)
    else:
        print("❌ No sample resume found!")
        exit()

    print("\nParsed Resume Text Snippet:\n", resume_text[:300], "...")

    # === Sample job descriptions (you'll plug in real data soon) ===
    job_texts = [
        "Looking for a Python developer with expertise in machine learning.",
        "Data scientist required with advanced analytical skills.",
        "Front-end developer needed with experience in React."
    ]

    matches = compute_similarities(resume_text, job_texts)

    print("\n🔍 Top Job Matches:")
    for job, score in matches:
        print(f"\nMatch Score: {score:.4f}")
        print(f"Job Description: {job}")

import json
from datetime import datetime
import os

# Save results
output_dir = "data/results"
os.makedirs(output_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"match_results_{timestamp}.json"
filepath = os.path.join(output_dir, filename)

# Format for saving
results_to_save = [
    {
        "match_score": round(float(score), 4),
        "job_description": job
    }
    for job, score in matches
]

with open(filepath, "w") as f:
    json.dump(results_to_save, f, indent=4)

print(f"\n✅ Results saved to {filepath}")
