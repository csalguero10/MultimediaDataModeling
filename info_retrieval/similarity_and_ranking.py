import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 📌 Cargar vectores desde los archivos
doc_vectors = []
with open('doc_vector.txt', 'r') as f:
    for line in f:
        parts = line.strip().split()
        doc_vectors.append(list(map(int, parts[1:])))

query_vector = []
with open('query_vector.txt', 'r') as f:
    line = f.readline()
    query_vector = list(map(int, line.strip().split()[1:]))

# Convertir a numpy arrays
doc_vectors = np.array(doc_vectors)
query_vector = np.array(query_vector).reshape(1, -1)

# 📌 Calcular cosine similarity
similarities = cosine_similarity(doc_vectors, query_vector).flatten()

# 📌 Mostrar similitudes
for idx, sim in enumerate(similarities):
    print(f"Similarity D{idx+1}-Q: {sim:.3f}")

# 📌 Ordenar documentos por relevancia (ranking)
ranking = np.argsort(similarities)[::-1]  # orden descendente

print("\nRanking de documentos:")
for rank, doc_idx in enumerate(ranking, 1):
    print(f"{rank}. Documento D{doc_idx+1} (similaridad: {similarities[doc_idx]:.3f})")
