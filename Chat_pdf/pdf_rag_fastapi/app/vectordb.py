import faiss
import numpy as np
import pickle
import os

class VectorDB:
    def __init__(self, index_path=None):
        self.index = None
        self.vectors = None
        self.chunks = None
        self.index_path = index_path

    def build(self, vectors, chunks):
        self.vectors = np.array(vectors).astype('float32')
        dim = self.vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.vectors)
        self.chunks = chunks

    def search(self, vector, k=3):
        D, I = self.index.search(np.array([vector]).astype('float32'), k)
        # FIX: Only use the first row of I (since query is a single vector)
        return [self.chunks[int(i)] for i in I[0]]

    def save(self, path_prefix):
        faiss.write_index(self.index, path_prefix + ".faiss")
        with open(path_prefix + ".pkl", "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self, path_prefix):
        self.index = faiss.read_index(path_prefix + ".faiss")
        with open(path_prefix + ".pkl", "rb") as f:
            self.chunks = pickle.load(f)
