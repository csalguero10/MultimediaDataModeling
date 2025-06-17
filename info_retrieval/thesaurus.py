#Crear un índice invertido para una colección de documentos, Definir un thesaurus simple, Permitir al usuario ingresar una palabra para búsqueda, Expandir la consulta usando sinónimos del thesaurus, Mostrar los documentos donde aparece cualquiera de esos términos

# Documentos
documentos = {
    'D1': "cats dogs birds",
    'D2': "automobile drivers",
    'D3': "car transport sedan",
    'D4': "puppy leash",
    'D5': "vehicle engine sports car"
}

# Thesaurus simple
thesaurus = {
    "car": {
        "synonyms": ["automobile", "vehicle"]
    },
    "dog": {
        "synonyms": ["canine", "puppy"]
    }
}

# Crear índice invertido
inverted_index = {}

for doc_id, texto in documentos.items():
    for palabra in texto.lower().split():
        if palabra not in inverted_index:
            inverted_index[palabra] = []
        inverted_index[palabra].append(doc_id)

# Mostrar índice invertido
print("Índice invertido:")
for palabra, docs in inverted_index.items():
    print(f"{palabra}: {docs}")

print("\n---")

# Consulta con expansión
consulta = input("Ingrese una palabra para buscar: ").lower()

# Recuperar sinónimos desde el thesaurus
terminos_consulta = [consulta]
if consulta in thesaurus:
    terminos_consulta += thesaurus[consulta]["synonyms"]

print(f"Consulta expandida: {terminos_consulta}")

# Buscar documentos que contengan alguno de esos términos
documentos_resultado = set()
for termino in terminos_consulta:
    if termino in inverted_index:
        documentos_resultado.update(inverted_index[termino])

# Mostrar resultados
if documentos_resultado:
    print(f"Documentos encontrados: {sorted(documentos_resultado)}")
else:
    print("No se encontraron documentos.")