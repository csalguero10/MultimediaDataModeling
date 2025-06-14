#escribe un programa en Python que: cree un índice invertido a partir de un conjunto de documentos,
# permita al usuario realizar consultas booleanas sobre el índice invertido,
# y devuelva los documentos que cumplen con la consulta.


def build_inverted_index(documents):
    inverted_index = {}
    
    for doc_index, doc in enumerate(documents):
        tokens = set(doc.split())  # Usar un conjunto para evitar duplicados
        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = []
            inverted_index[token].append(doc_index)
    
    return inverted_index

#los documeentos estan cargados en el repositorio para hacer un inverted index
def boolean_query(inverted_index, query):
    query_terms = query.split()
    result_set = None
    
    for term in query_terms:
        if term == 'AND':
            continue
        elif term.startswith('NOT'):
            keyword = term[4:]  # Extraer la palabra clave después de 'NOT'
            if keyword in inverted_index:
                doc_indices = set(inverted_index[keyword])
                if result_set is None:
                    result_set = set(range(len(documents))) - doc_indices
                else:
                    result_set -= doc_indices
            else:
                if result_set is None:
                    result_set = set(range(len(documents)))
        else:  # Es un término normal (AND)
            if term in inverted_index:
                doc_indices = set(inverted_index[term])
                if result_set is None:
                    result_set = doc_indices
                else:
                    result_set &= doc_indices
            else:
                return set()  # Si un término no está en el índice, no hay resultados
    
    return result_set

# Ejemplo de uso
if __name__ == "__main__":
    documents = [
        "el gato come pescado",
        "el perro juega con la pelota",
        "el gato y el perro son amigos",
        "la casa es grande y bonita"
    ]
    
    inverted_index = build_inverted_index(documents)
    
    print("Índice Invertido:")
    for term, doc_indices in inverted_index.items():
        print(f"{term}: {doc_indices}")
    
    query = input("Ingrese su consulta booleana (ejemplo: gato AND perro AND NOT casa): ")
    
    results = boolean_query(inverted_index, query)
    
    print("Documentos que cumplen con la consulta:")
    for doc_index in results:
        print(documents[doc_index])
# Este código crea un índice invertido a partir de un conjunto de documentos y permite realizar consultas booleanas sobre él.

#eliminar las stopwords y los signos de puntuación
import string
def remove_stopwords_and_punctuation(documents, stopwords):
    cleaned_documents = []
    for doc in documents:
        # Convertir a minúsculas y eliminar signos de puntuación
        doc = doc.lower().translate(str.maketrans('', '', string.punctuation))
        # Eliminar stopwords
        tokens = [word for word in doc.split() if word not in stopwords]
        cleaned_documents.append(' '.join(tokens))
    return cleaned_documents
# Lista de stopwords en español
stopwords = [
    'el', 'la', 'los', 'las', 'de', 'y', 'a', 'en', 'que', 'con', 
    'por', 'para', 'un', 'una', 'es', 'del', 'se', 'lo', 'las',
    # Agrega más stopwords según sea necesario
]
# Ejemplo de uso de la función para eliminar stopwords y signos de puntuación
if __name__ == "__main__":
    documents = [
        "El gato come pescado.",
        "El perro juega con la pelota.",
        "El gato y el perro son amigos.",
        "La casa es grande y bonita."
    ]
    
    cleaned_documents = remove_stopwords_and_punctuation(documents, stopwords)
    
    print("Documentos limpios:")
    for doc in cleaned_documents:
        print(doc)
    
    inverted_index = build_inverted_index(cleaned_documents)
    
    print("\nÍndice Invertido:")
    for term, doc_indices in inverted_index.items():
        print(f"{term}: {doc_indices}")
    
    query = input("Ingrese su consulta booleana (ejemplo: gato AND perro AND NOT casa): ")
    
    results = boolean_query(inverted_index, query)
    
    print("Documentos que cumplen con la consulta:")
    for doc_index in results:
        print(cleaned_documents[doc_index])
# Este código implementa un índice invertido y permite realizar consultas booleanas sobre un conjunto de documentos.

# Algoritmo para identifiar stemmas y lemas en un conjunto de documentos,
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')
def stem_and_lemmatize(documents):
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    stemmed_documents = []
    lemmatized_documents = []
    
    for doc in documents:
        tokens = doc.split()
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
        
        stemmed_documents.append(' '.join(stemmed_tokens))
        lemmatized_documents.append(' '.join(lemmatized_tokens))
    
    return stemmed_documents, lemmatized_documents
# Ejemplo de uso de la función para identificar stemmas y lemas
if __name__ == "__main__":
    documents = [
        "El gato está corriendo rápidamente.",
        "Los perros juegan en el parque.",
        "El gato y el perro son amigos."
    ]
    
    stemmed_docs, lemmatized_docs = stem_and_lemmatize(documents)
    
    print("Documentos con Stemmas:")
    for doc in stemmed_docs:
        print(doc)
    
    print("\nDocumentos con Lemas:")
    for doc in lemmatized_docs:
        print(doc)
    
    inverted_index_stemmed = build_inverted_index(stemmed_docs)
    inverted_index_lemmatized = build_inverted_index(lemmatized_docs)
    
    print("\nÍndice Invertido (Stemmas):")
    for term, doc_indices in inverted_index_stemmed.items():
        print(f"{term}: {doc_indices}")
    
    print("\nÍndice Invertido (Lemas):")
    for term, doc_indices in inverted_index_lemmatized.items():
        print(f"{term}: {doc_indices}")


