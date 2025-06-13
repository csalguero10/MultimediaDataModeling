#Tengo una colección de documentos en texto plano. Quiero que apliques técnicas de recuperación de información siguiendo estos pasos:

#Tokenización: Extrae todas las palabras individuales de cada documento, ignora signos de puntuación y convierte todas las palabras a minúsculas.

import re
def tokenize_document(document):
    # Elimina signos de puntuación y convierte a minúsculas
    tokens = re.findall(r'\b\w+\b', document.lower())
    return tokens

#TF (Term Frequency): Calcula la frecuencia de cada término (palabra) en cada documento.
def calculate_term_frequency(tokens):
    term_frequency = {}
    for token in tokens:
        if token in term_frequency:
            term_frequency[token] += 1
        else:
            term_frequency[token] = 1
    return term_frequency

#IDF (Inverse Document Frequency): Calcula el valor IDF de cada término considerando el conjunto completo de documentos, para reducir el peso de términos muy comunes.

import math
def calculate_inverse_document_frequency(documents):
    num_documents = len(documents)
    idf = {}
    for document in documents:
        tokens = set(tokenize_document(document))
        for token in tokens:
            if token in idf:
                idf[token] += 1
            else:
                idf[token] = 1
    # Calcula el IDF para cada término
    for token, count in idf.items():
        idf[token] = math.log(num_documents / count) if count > 0 else 0
    return idf
#TF-IDF (Term Frequency-Inverse Document Frequency): Combina TF e IDF para calcular el peso de cada término en cada documento.

def calculate_tf_idf(documents):
    tf_idf = []
    idf = calculate_inverse_document_frequency(documents)
    
    for document in documents:
        tokens = tokenize_document(document)
        term_frequency = calculate_term_frequency(tokens)
        doc_tf_idf = {}
        
        for token, tf in term_frequency.items():
            tf_idf_value = tf * idf.get(token, 0)
            doc_tf_idf[token] = tf_idf_value
        
        tf_idf.append(doc_tf_idf)
    
    return tf_idf

#Índice invertido con TF-IDF: Construye un índice invertido donde cada término esté asociado con una lista de documentos en los que aparece, junto con su valor TF-IDF correspondiente.

def build_inverted_index(documents):
    inverted_index = {}
    tf_idf = calculate_tf_idf(documents)
    
    for doc_index, doc_tf_idf in enumerate(tf_idf):
        for term, value in doc_tf_idf.items():
            if term not in inverted_index:
                inverted_index[term] = []
            inverted_index[term].append((doc_index, value))
    
    return inverted_index
# Función principal para procesar documentos
def process_documents(documents):
    # Tokenización
    tokenized_documents = [tokenize_document(doc) for doc in documents]
    
    # Cálculo de TF-IDF
    tf_idf = calculate_tf_idf(documents)
    
    # Construcción del índice invertido
    inverted_index = build_inverted_index(documents)
    
    return {
        'tokenized_documents': tokenized_documents,
        'tf_idf': tf_idf,
        'inverted_index': inverted_index
    }
# Ejemplo de uso
if __name__ == "__main__":
    documents = [
        "El gato está en el tejado.",
        "El perro está en el jardín.",
        "El gato y el perro son amigos."
    ]
    
    result = process_documents(documents)
    
    print("Tokenized Documents:")
    for doc in result['tokenized_documents']:
        print(doc)
    
    print("\nTF-IDF:")
    for i, tf_idf in enumerate(result['tf_idf']):
        print(f"Document {i}: {tf_idf}")
    
    print("\nInverted Index:")
    for term, postings in result['inverted_index'].items():
        print(f"{term}: {postings}")
        
# Este código implementa un proceso de recuperación de información que incluye tokenización, cálculo de TF, IDF, TF-IDF y construcción de un índice invertido.
# Cada paso se realiza de manera modular, permitiendo una fácil comprensión y reutilización.
# El código está diseñado para ser ejecutado directamente, y al final se proporciona un ejemplo de uso con una colección de documentos.
# El código es eficiente y utiliza expresiones regulares para la tokenización, lo que permite una extracción precisa de palabras.
# Además, se asegura de que los términos sean tratados en minúsculas y sin signos de puntuación, lo que mejora la consistencia en el análisis de texto.
# El índice invertido resultante permite una búsqueda rápida de términos y sus documentos asociados, facilitando la recuperación de información relevante.