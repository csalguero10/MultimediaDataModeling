import numpy as np

# Vectores de ejemplo
doc_vector = np.array([2, 1, 0])
query_vector = np.array([1, 1, 1])

# Cosine similarity
def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

similarity = cosine_similarity(doc_vector, query_vector)
print(f"Cosine Similarity: {similarity:.3f}")

#cosine similarity con documentos txt
def read_vector_from_file(file_path):
    with open(file_path, 'r') as file:
        vector = np.array([float(x) for x in file.read().strip().split()])
    return vector

# Ejemplo de uso
doc_vector_file = 'doc_vector.txt'
query_vector_file = 'query_vector.txt'
doc_vector = read_vector_from_file(doc_vector_file)
query_vector = read_vector_from_file(query_vector_file)
similarity = cosine_similarity(doc_vector, query_vector)
print(f"Cosine Similarity from files: {similarity:.3f}")
# Guardar vectores de ejemplo en archivos
def save_vector_to_file(vector, file_path):
    with open(file_path, 'w') as file:
        file.write(' '.join(map(str, vector)))
save_vector_to_file(doc_vector, doc_vector_file)
save_vector_to_file(query_vector, query_vector_file)

# Guardar vectores de ejemplo en archivos
doc_vector = np.array([2, 1, 0])
query_vector = np.array([1, 1, 1])
save_vector_to_file(doc_vector, doc_vector_file)
save_vector_to_file(query_vector, query_vector_file)