import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar imágenes (usa tus propias rutas o imágenes)
img1 = cv2.imread('imagen1.jpg')
img2 = cv2.imread('imagen2.jpg')

# Redimensionar si son muy diferentes
img1 = cv2.resize(img1, (256, 256))
img2 = cv2.resize(img2, (256, 256))

# Convertir a espacio de color RGB (OpenCV usa BGR por defecto)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

# Calcular histogramas para cada canal (R, G, B) y concatenar
def get_histogram(image):
    hist_r = cv2.calcHist([image], [0], None, [256], [0, 256]).flatten()
    hist_g = cv2.calcHist([image], [1], None, [256], [0, 256]).flatten()
    hist_b = cv2.calcHist([image], [2], None, [256], [0, 256]).flatten()
    hist = np.concatenate([hist_r, hist_g, hist_b])
    return hist / hist.sum()  # normalización

hist1 = get_histogram(img1)
hist2 = get_histogram(img2)

# Calcular diferencias
diff = hist1 - hist2

# Normas
l1 = np.linalg.norm(diff, ord=1)
l2 = np.linalg.norm(diff, ord=2)
linf = np.linalg.norm(diff, ord=np.inf)

# Mostrar resultados
print(f"L1-norm: {l1:.4f}")
print(f"L2-norm: {l2:.4f}")
print(f"L∞-norm: {linf:.4f}")

# Visualizar histogramas
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
# Mostrar imágenes
cv2.imshow('Imagen 1', img1)
cv2.imshow('Imagen 2', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Guardar histogramas como imágenes
def save_histogram_image(hist, filename):
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(hist)), hist, color='gray', alpha=0.7)
    plt.title('Histograma')
    plt.xlabel('Intensidad de píxel')
    plt.ylabel('Frecuencia')
    plt.savefig(filename)
    plt.close()
save_histogram_image(hist1, 'histograma_imagen1.png')
save_histogram_image(hist2, 'histograma_imagen2.png')
# Guardar imágenes originales
cv2.imwrite('imagen1_guardada.jpg', cv2.cvtColor(img1, cv2.COLOR_RGB2BGR))
cv2.imwrite('imagen2_guardada.jpg', cv2.cvtColor(img2, cv2.COLOR_RGB2BGR))
# Guardar diferencias como imagen
def save_difference_image(diff, filename):
    diff_image = np.clip(diff * 255, 0, 255).astype(np.uint8)
    cv2.imwrite(filename, diff_image)
save_difference_image(diff, 'diferencia_imagenes.png')
# Guardar normas en un archivo de texto
def save_norms_to_file(filename, norms):
    with open(filename, 'w') as f:
        f.write(f"L1-norm: {norms[0]:.4f}\n")
        f.write(f"L2-norm: {norms[1]:.4f}\n")
        f.write(f"L∞-norm: {norms[2]:.4f}\n")
save_norms_to_file('normas.txt', (l1, l2, linf))
# Guardar imágenes originales y diferencias en un archivo ZIP
import zipfile
def save_images_to_zip(zip_filename, images):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for img in images:
            zipf.write(img)
            print(f'Imagen añadida al ZIP: {img}')
save_images_to_zip('imagenes_comprimidas.zip', ['imagen1_guardada.jpg', 'imagen2_guardada.jpg', 'diferencia_imagenes.png'])
# Guardar histogramas en un archivo ZIP
def save_histograms_to_zip(zip_filename, histograms):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for hist_file in histograms:
            zipf.write(hist_file)
            print(f'Histograma añadido al ZIP: {hist_file}')
save_histograms_to_zip('histogramas_comprimidos.zip', ['histograma_imagen1.png', 'histograma_imagen2.png'])
# Guardar normas en un archivo ZIP
def save_norms_to_zip(zip_filename, norms_file):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(norms_file)
        print(f'Archivo de normas añadido al ZIP: {norms_file}')
save_norms_to_zip('normas_comprimidas.zip', 'normas.txt')
# Guardar imágenes originales y diferencias en un archivo ZIP
def save_all_to_zip(zip_filename, images, histograms, norms_file):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for img in images:
            zipf.write(img)
            print(f'Imagen añadida al ZIP: {img}')
        for hist_file in histograms:
            zipf.write(hist_file)
            print(f'Histograma añadido al ZIP: {hist_file}')
        zipf.write(norms_file)
        print(f'Archivo de normas añadido al ZIP: {norms_file}')
save_all_to_zip('todo_comprimido.zip', 
                 ['imagen1_guardada.jpg', 'imagen2_guardada.jpg', 'diferencia_imagenes.png'], 
                 ['histograma_imagen1.png', 'histograma_imagen2.png'], 
                 'normas.txt')
# Este código compara dos imágenes, calcula sus histogramas, evalúa las diferencias y guarda los resultados en varios formatos.
# Asegúrate de tener las imágenes 'imagen1.jpg' y 'imagen2.jpg' en el mismo directorio que este script.
# Requiere las bibliotecas OpenCV, NumPy, Matplotlib y zipfile.
# Asegúrate de tener las imágenes 'imagen1.jpg' y 'imagen2.jpg' en el mismo directorio que este script.
# Requiere las bibliotecas OpenCV, NumPy, Matplotlib y zipfile.
# Asegúrate de tener las imágenes 'imagen1.jpg' y 'imagen2.jpg' en el mismo directorio que este script.