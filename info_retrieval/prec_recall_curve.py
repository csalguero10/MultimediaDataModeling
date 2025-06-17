# Documentos y consulta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_recall_curve, average_precision_score
import matplotlib.pyplot as plt
import numpy as np

# 📌 Lista de documentos (pueden ser los textos que quieras)
docs = [
    "Gabriel García Márquez wrote many novels.",
    "This project is about literature and legacy.",
    "Gabriel García Márquez and Latin American literature.",
    "Legacy projects connect data and archives.",
    "Gabo’s work influenced generations."
]

# 📌 Consulta
query = ["Gabriel García Márquez legacy project"]

#Paso 2: Vectorización (TF-IDF)
# 📌 Crear vectorizador TF-IDF
vectorizer = TfidfVectorizer()

# 📌 Unir documentos y consulta para vectorizar juntos
all_texts = docs + query

# 📌 Crear matriz TF-IDF
tfidf_matrix = vectorizer.fit_transform(all_texts)

# 📌 Separar vectores de documentos y de consulta
doc_vectors = tfidf_matrix[:-1]
query_vector = tfidf_matrix[-1:]

#Paso 3: Calcular similitud coseno
# 📌 Similaridad coseno entre la consulta y cada documento
cosine_similarities = cosine_similarity(doc_vectors, query_vector).flatten()

# 📌 Mostrar ranking
for i, score in enumerate(cosine_similarities):
    print(f"Documento {i+1}: Similaridad = {score:.3f}")

#  Paso 4: Definir relevancia real (ground truth)
# 📌 Definimos qué documentos son realmente relevantes (por juicio humano)
# Supongamos que documentos 1, 3 y 5 son relevantes
y_true = np.array([1, 0, 1, 0, 1])

#Paso 5: Precision-Recall Curve
# 📌 Calcular Precision, Recall y thresholds
precision, recall, thresholds = precision_recall_curve(y_true, cosine_similarities)

# 📌 Average Precision (área bajo la curva)
ap = average_precision_score(y_true, cosine_similarities)

# 📌 Graficar la curva
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, marker='o', label=f'AP = {ap:.2f}')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve para Consulta')
plt.grid(True)
plt.legend()
plt.show()