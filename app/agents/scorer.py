import numpy as np
from app.services.embedding_service import EmbeddingService

class ScorerAgent:

    def __init__(self):
        self.embedder = EmbeddingService()

        # 👉 USER INTEREST (customize later)
        self.user_interest = "machine learning, deep learning, AI agents"

        self.user_embedding = self.embedder.get_embedding(self.user_interest)

    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def score(self, text):
        paper_embedding = self.embedder.get_embedding(text)

        similarity = self.cosine_similarity(self.user_embedding, paper_embedding)

        return float(similarity * 10)  # scale to 0–10