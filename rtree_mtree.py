from rtree import index
import Levenshtein

# Crear índice R-tree
idx = index.Index()

# Insertamos objetos (id, bounding box, metadata opcional)
idx.insert(0, (0, 0, 10, 10))   # Imagen 0: en posición (0,0) a (10,10)
idx.insert(1, (5, 5, 15, 15))   # Imagen 1
idx.insert(2, (20, 20, 30, 30)) # Imagen 2

# Buscar imágenes que intersectan con el rectángulo (7, 7, 12, 12)
results = list(idx.intersection((7, 7, 12, 12)))
print("IDs encontrados:", results)


class MTreeNode:
    def __init__(self, obj):
        self.obj = obj
        self.children = []

    def add(self, new_obj):
        dist = Levenshtein.distance(self.obj, new_obj)
        for child, radius in self.children:
            if Levenshtein.distance(child.obj, new_obj) <= radius:
                child.add(new_obj)
                return
        self.children.append((MTreeNode(new_obj), dist))

    def search(self, query, max_dist, results=None):
        if results is None:
            results = []
        dist = Levenshtein.distance(self.obj, query)
        if dist <= max_dist:
            results.append((self.obj, dist))
        for child, radius in self.children:
            if abs(Levenshtein.distance(child.obj, query) - radius) <= max_dist:
                child.search(query, max_dist, results)
        return results

# Crear árbol con textos
mtree = MTreeNode("casa")
mtree.add("caso")
mtree.add("cama")
mtree.add("masa")
mtree.add("caza")

# Búsqueda por similitud
resultado = mtree.search("caza", max_dist=1)
print("Resultados:", resultado)
