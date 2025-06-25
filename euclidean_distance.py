import cv2
import numpy as np
import matplotlib.pyplot as plt

# --- FUNCIONES ---

# Calcular histograma normalizado RGB concatenado
def get_histogram(image):
    hist_r = cv2.calcHist([image], [0], None, [256], [0, 256]).flatten()
    hist_g = cv2.calcHist([image], [1], None, [256], [0, 256]).flatten()
    hist_b = cv2.calcHist([image], [2], None, [256], [0, 256]).flatten()
    hist = np.concatenate([hist_r, hist_g, hist_b])
    return hist / np.sum(hist)  # normalizar

# Calcular distancia Euclidiana
def euclidean_distance(h1, h2):
    return np.linalg.norm(h1 - h2)

# Calcular distancia Euclidiana ponderada
def weighted_euclidean_distance(h1, h2, weights):
    diff = h1 - h2
    return np.sqrt(np.sum(weights * diff**2))

# --- CARGAR IMÁGENES ---

# Cambia los nombres por tus imágenes
img1 = cv2.imread('imagen1.jpg')
img2 = cv2.imread('imagen2.jpg')

# Redimensionar para comparación justa
img1 = cv2.resize(img1, (256, 256))
img2 = cv2.resize(img2, (256, 256))

# Convertir a RGB
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

# --- CÁLCULO DE HISTOGRAMAS ---
hist1 = get_histogram(img1)
hist2 = get_histogram(img2)

# --- DISTANCIAS ---
# Euclidiana normal
d_euclidean = euclidean_distance(hist1, hist2)

# Ejemplo: pesos más altos en el canal rojo (primer tercio del histograma)
weights = np.ones_like(hist1)
weights[:256] = 2.0  # canal rojo más importante

# Euclidiana ponderada
d_weighted = weighted_euclidean_distance(hist1, hist2, weights)

# --- RESULTADOS ---
print(f"Euclidean Distance: {d_euclidean:.4f}")
print(f"Weighted Euclidean Distance: {d_weighted:.4f}")

# --- OPCIONAL: visualizar imágenes ---
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.imshow(img1)
plt.title("Imagen 1")
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(img2)
plt.title("Imagen 2")
plt.axis('off')
plt.show()

# --- OPCIONAL: visualizar histogramas --- 
def plot_histograms(hist1, hist2):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title('Histograma Imagen 1')
    plt.bar(range(len(hist1)), hist1, color='r', alpha=0.5, label='Rojo')
    plt.bar(range(len(hist1), len(hist1) + len(hist2)), hist2, color='g', alpha=0.5, label='Verde')
    plt.bar(range(len(hist1) + len(hist2), len(hist1) + 2 * len(hist2)), hist2, color='b', alpha=0.5, label='Azul')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title('Histograma Imagen 2')
    plt.bar(range(len(hist1)), hist1, color='r', alpha=0.5)
    plt.bar(range(len(hist1), len(hist1) + len(hist2)), hist2, color='g', alpha=0.5)
    plt.bar(range(len(hist1) + len(hist2), len(hist1) + 2 * len(hist2)), hist2, color='b', alpha=0.5)

    plt.tight_layout()
    plt.show()
plot_histograms(hist1, hist2)