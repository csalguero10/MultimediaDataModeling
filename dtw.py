import numpy as np
import matplotlib.pyplot as plt

# Secuencias desfasadas
seq1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
seq2 = np.array([0, 0.5, 1.5, 2.5, 3.5, 4.5, 6, 7.5, 8.5, 9])

# Crear matriz de distancias
n, m = len(seq1), len(seq2)
dtw_matrix = np.full((n + 1, m + 1), np.inf)
dtw_matrix[0, 0] = 0

# Rellenar la matriz con la distancia acumulada
for i in range(1, n + 1):
    for j in range(1, m + 1):
        cost = abs(seq1[i - 1] - seq2[j - 1])
        dtw_matrix[i, j] = cost + min(
            dtw_matrix[i - 1, j],    # inserción
            dtw_matrix[i, j - 1],    # eliminación
            dtw_matrix[i - 1, j - 1] # match
        )

# Backtracking para recuperar el camino óptimo
i, j = n, m
path = []
while i > 0 and j > 0:
    path.append((i - 1, j - 1))
    i_, j_ = i - 1, j - 1
    if dtw_matrix[i_, j] < dtw_matrix[i, j_] and dtw_matrix[i_, j] < dtw_matrix[i_, j_]:
        i -= 1
    elif dtw_matrix[i, j_] < dtw_matrix[i_, j_]:
        j -= 1
    else:
        i -= 1
        j -= 1
path.reverse()

# Visualización
plt.figure(figsize=(10, 6))
for i, j in path:
    plt.plot([i, j], [seq1[i], seq2[j]], 'k--', linewidth=0.5)
plt.plot(seq1, label="Secuencia 1", marker='o')
plt.plot(seq2, label="Secuencia 2", marker='x')
plt.title("Alineación con Dynamic Time Warping (DTW)")
plt.xlabel("Índice")
plt.ylabel("Valor")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Distancia DTW final
dtw_matrix[n, m]
