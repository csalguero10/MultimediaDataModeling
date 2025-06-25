import torch
import clip
from PIL import Image
import faiss
import numpy as np

# Cargar modelo CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Cargar imágenes y convertir a vectores
image_paths = ["imagen1.jpg", "imagen2.jpg"]  # Reemplaza con tus imágenes
image_vectors = []

for path in image_paths:
    image = preprocess(Image.open(path)).unsqueeze(0).to(device)
    with torch.no_grad():
        vec = model.encode_image(image)
        vec /= vec.norm(dim=-1, keepdim=True)  # Normalizar
        image_vectors.append(vec.cpu().numpy())

image_vectors = np.vstack(image_vectors).astype("float32")

# Crear índice FAISS
index = faiss.IndexFlatIP(image_vectors.shape[1])  # IP = dot product (con vectores normalizados = cosine)
index.add(image_vectors)

# Buscar imágenes similares a img1
D, I = index.search(image_vectors[0:1], 3)
print("IDs similares a img1:", I)
