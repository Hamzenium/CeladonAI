import openai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

openai.api_key = 'sk-0tsxXxXpqVdU7Mom2BFOT3BlbkFJzqv7WcNkFfGKbdvtnEyY'

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

def array_embedder(sub_paragraphs):
    embeddings = [get_embedding(paragraph) for paragraph in sub_paragraphs]
    return embeddings

def similarity(question, embeddings, paragraphs):
    similarity_scores = cosine_similarity([question], embeddings)[0]
    most_similar_indices = np.argsort(similarity_scores)[-2:]
    most_similar_paragraphs = [(paragraphs[i], similarity_scores[i]) for i in most_similar_indices[::-1]]
    return most_similar_paragraphs
