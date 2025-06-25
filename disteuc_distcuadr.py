import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from numpy.linalg import inv

# Simulación de dos histogramas de color (8 bins)
hist1 = np.array([0.1, 0.2, 0.3, 0.15, 0.05, 0.1, 0.05, 0.05])
hist2 = np.array([0.1, 0.25, 0.25, 0.1, 0.1, 0.1, 0.05, 0.05])

# Distancia Euclidiana
dist_euclid = euclidean(hist1, hist2)

# Función para crear una matriz de similitud gaussiana entre bins
def gaussian_similarity_matrix(n_bins, sigma=1.0):
    A = np.zeros((n_bins, n_bins))
    for i in range(n_bins):
        for j in range(n_bins):
            A[i, j] = np.exp(-((i - j) ** 2) / (2 * sigma ** 2))
    return A

# Matriz de similitud (entre bins cercanos hay más similitud)
A = gaussian_similarity_matrix(len(hist1), sigma=1.5)

# Distancia Cuadrática (forma cuadrática general)
diff = hist1 - hist2
dist_quadratic = diff.T @ A @ diff

# Resultados
print(f"Distancia Euclidiana: {dist_euclid:.4f}")
print(f"Distancia Cuadrática: {dist_quadratic:.6f}")

# Visualización de los histogramas
plt.figure(figsize=(10, 4))
plt.bar(np.arange(8) - 0.15, hist1, width=0.3, label='Histograma 1', color='blue')
plt.bar(np.arange(8) + 0.15, hist2, width=0.3, label='Histograma 2', color='orange')
plt.title("Comparación de Histogramas de Color")
plt.xlabel("Bin")
plt.ylabel("Frecuencia")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
# Visualización de la matriz de similitud
plt.figure(figsize=(6, 6))
plt.imshow(A, cmap='hot', interpolation='nearest')
plt.title("Matriz de Similitud Gaussiana entre Bins")
plt.colorbar(label='Similitud')
plt.xlabel("Bin j")
plt.ylabel("Bin i")
plt.tight_layout()
plt.show()  
# Visualización de la diferencia entre histogramas
plt.figure(figsize=(10, 4))
plt.bar(np.arange(8), hist1 - hist2, color='purple', alpha=0.7)
plt.title("Diferencia entre Histogramas de Color")
plt.xlabel("Bin")
plt.ylabel("Diferencia de Frecuencia")
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.grid(True)
plt.tight_layout()
plt.show()  
