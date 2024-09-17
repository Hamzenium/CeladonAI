import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity

def cosine_similarity(question_embedding, embeddings):
    similarity_scores = sklearn_cosine_similarity([question_embedding], embeddings)[0]
    return embeddings[np.argmax(similarity_scores)]
