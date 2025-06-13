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
