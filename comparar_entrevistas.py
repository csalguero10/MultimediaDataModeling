import librosa
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

# Cargar las entrevistas (ajusta las rutas a tus archivos reales)
y1, sr1 = librosa.load("entrevistas/persona1_respuesta.wav", sr=16000)
y2, sr2 = librosa.load("entrevistas/persona2_respuesta.wav", sr=16000)

# Extraer MFCCs
mfcc1 = librosa.feature.mfcc(y=y1, sr=sr1, n_mfcc=13).T  # shape: (frames, 13)
mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2, n_mfcc=13).T

# Calcular distancia DTW
distance, path = fastdtw(mfcc1, mfcc2, dist=euclidean)
print(f"Distancia DTW entre las respuestas: {distance:.2f}")

# Visualizar alineamiento
plt.figure(figsize=(10, 4))
plt.plot([i for i, j in path], label='Respuesta 1 (persona1)')
plt.plot([j for i, j in path], label='Respuesta 2 (persona2)')
plt.title("Alineamiento DTW entre entrevistas")
plt.xlabel("Paso DTW")
plt.ylabel("Índice de frame")
plt.legend()
plt.grid(True)
plt.show()

