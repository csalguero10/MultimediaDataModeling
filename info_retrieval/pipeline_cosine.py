import nltk
from sklearn.feature_extraction.text import CountVectorizer
import string

# Descargar stopwords si no lo tenés
nltk.download('stopwords')
from nltk.corpus import stopwords

# 📌 Textos de ejemplo
documents = [
    """LOD Gabriel García Márquez: A Journey Through Gabo’s World is a project that brings together both objects produced by Gabriel García Márquez and materials related to his figure, with the goal of building a Linked Open Data model to represent and visualize knowledge surrounding his legacy.""",
    """Another document about literature, discussing the legacy of Gabriel García Márquez and the impact of his work in Latin American culture.""",
]

query = """Gabriel García Márquez legacy"""

# 📌 Preprocesado
stop_words = set(stopwords.words('english'))

def preprocess(text):
    # Minúsculas, quitar puntuación y stopwords
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Preprocesar documentos y consulta
processed_docs = [preprocess(doc) for doc in documents]
processed_query = preprocess(query)

# 📌 Definir vocabulario manualmente (opcional)
vocabulario = ['gabriel', 'garcía', 'márquez', 'project', 'data', 'documents', 'legacy']

# 📌 Vectorizador con vocabulario fijo
vectorizer = CountVectorizer(vocabulary=vocabulario)

# 📌 Vectorizar documentos y consulta
doc_vectors = vectorizer.fit_transform(processed_docs).toarray()
query_vector = vectorizer.transform([processed_query]).toarray()

# 📌 Guardar doc_vector.txt
with open('doc_vector.txt', 'w') as f:
    for idx, vec in enumerate(doc_vectors):
        f.write(f"D{idx+1}  {' '.join(map(str, vec))}\n")

# 📌 Guardar query_vector.txt
with open('query_vector.txt', 'w') as f:
    f.write(f"Q  {' '.join(map(str, query_vector[0]))}\n")

# 📌 Mostrar resultados en consola
print("Document Vectors:\n", doc_vectors)
print("\nQuery Vector:\n", query_vector)
