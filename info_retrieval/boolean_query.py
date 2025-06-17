#Escribe un programa en Python que:
# permita al usuario ingresar un número n de documentos,

#Permita ingresar un número n de documentos especificar formato.
# permita al usuario ingresar 3 palabras clave,
# construya una matriz binaria que indique si cada palabra clave está presente en cada documento,
#Por cada documento, permita al usuario ingresar su contenido (como string).
# y evalúe una consulta booleana de la forma: palabra1 AND palabra2 AND NOT palabra3.
#     for i, doc in enumerate(documents):

def boolean_query(documents, keywords, query):
    # Crear una matriz binaria para las palabras clave
    binary_matrix = []
    
    for doc in documents:
        row = []
        for keyword in keywords:
            row.append(1 if keyword in doc else 0)
        binary_matrix.append(row)
    
    # Evaluar la consulta booleana
    query_terms = query.split()
    result = [1] * len(documents)  # Inicializar con todos los documentos
    
    for term in query_terms:
        if term == 'AND':
            continue
        elif term.startswith('NOT'):
            keyword = term[4:]  # Extraer la palabra clave después de 'NOT'
            for i, doc in enumerate(binary_matrix):
                if keyword in keywords and doc[keywords.index(keyword)] == 1:
                    result[i] = 0  # Excluir este documento
        else:  # Es un término normal (AND)
            if term in keywords:
                index = keywords.index(term)
                for i, doc in enumerate(binary_matrix):
                    if doc[index] == 0:
                        result[i] = 0  # Excluir este documento si no contiene el término
    
    return [documents[i] for i in range(len(documents)) if result[i] == 1]
# Ejemplo de uso
if __name__ == "__main__":
    n = int(input("Ingrese el número de documentos: "))
    documents = []
    
    for i in range(n):
        doc_content = input(f"Ingrese el contenido del documento {i + 1}: ")
        documents.append(doc_content)
    
    keywords = input("Ingrese 3 palabras clave separadas por comas: ").split(',')
    keywords = [keyword.strip() for keyword in keywords]
    
    query = input("Ingrese su consulta booleana (ejemplo: palabra1 AND palabra2 AND NOT palabra3): ")
    
    results = boolean_query(documents, keywords, query)
    
    print("Documentos que cumplen con la consulta:")
    for result in results:
        print(result) 


