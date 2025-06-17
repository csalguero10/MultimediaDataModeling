from sklearn.metrics import precision_score, recall_score, f1_score

# 📌 Supongamos que tenemos 10 documentos numerados del 1 al 10
# Y sabemos cuáles son relevantes según el juicio humano:
relevant_docs = {1, 3, 4, 6, 7, 9}  # ground truth (6 relevantes en total)

# 📌 Ahora, documentos que recuperó el sistema:
retrieved_docs = {1, 2, 3, 5, 7, 8}  # recuperó 6 documentos

# 📌 Generar listas binarias para sklearn
# 1 si relevante, 0 si no relevante
y_true = [1 if doc in relevant_docs else 0 for doc in range(1, 11)]
y_pred = [1 if doc in retrieved_docs else 0 for doc in range(1, 11)]

# 📌 Calcular Precision, Recall y F1
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# 📌 Mostrar resultados
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1:.2f}")
