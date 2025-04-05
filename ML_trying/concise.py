import requests
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize

HF_API_KEY = "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"
HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def get_sentences(text):
    return sent_tokenize(text)

def get_embeddings(sentences):
    url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
    payload = {"inputs": sentences}
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return np.array(response.json())

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def measure_conciseness(text):
    sentences = get_sentences(text)
    if len(sentences) < 2:
        return 1.0

    embeddings = get_embeddings(sentences)
    total_sim = 0
    count = 0

    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            total_sim += sim
            count += 1

    avg_similarity = total_sim / count
    conciseness = round(1.0 - min(avg_similarity, 1.0), 3)
    return conciseness

