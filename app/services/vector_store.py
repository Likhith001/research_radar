import faiss
import numpy as np


class VectorStore:

    def __init__(self, dim=384):  # ✅ changed from 768
        self.index = faiss.IndexFlatL2(dim)
        self.vectors = []