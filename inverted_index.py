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

#los documeentos estan cargados en el repositorio 
def boolean_query_inverted_index(inverted_index, query):
    query_terms = query.split()
    result = None  # Inicializar el resultado
    
    for term in query_terms:
        if term == 'AND':
            continue
        elif term.startswith('NOT'):
            keyword = term[4:]  # Extraer la palabra clave después de 'NOT'
            if keyword in inverted_index:
                if result is None:
                    result = set(range(len(inverted_index)))  # Todos los documentos
                result -= set(inverted_index[keyword])  # Excluir documentos que contienen el término
        else:  # Es un término normal (AND)
            if term in inverted_index:
                if result is None:
                    result = set(inverted_index[term])  # Iniciar con los documentos que contienen el término
                else:
                    result &= set(inverted_index[term])  # Intersección con los documentos que contienen el término
    
    return list(result) if result is not None else []

# Ejemplo de uso
if __name__ == "__main__":
    n = int(input("Ingrese el número de documentos: "))
    documents = []
    
    for i in range(n):
        doc_content = input(f"Ingrese el contenido del documento {i + 1}: ")
        documents.append(doc_content)
    
    inverted_index = build_inverted_index(documents)
    
    query = input("Ingrese su consulta booleana (ejemplo: palabra1 AND palabra2 AND NOT palabra3): ")
    
    results = boolean_query_inverted_index(inverted_index, query)
    
    print("Documentos que cumplen con la consulta:")
    for result in results:
        print(documents[result])  # Mostrar el contenido del documento

