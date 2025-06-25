import cv2
import pytesseract
import pandas as pd
from PIL import Image
import re
import os

# --- Configuración ---
INPUT_IMAGE = "catalogo.png"  # Asegúrate de usar la imagen ORIGINAL, no la preprocesada
OUTPUT_CSV = "lotes_estructurados.csv"

# Indicar idiomas italiano y francés para Tesseract
TESSERACT_LANG = 'ita+fra'

# --- Paso 1: Preprocesamiento de imagen (MEJORADO) ---
def preprocess_image(image_path):
    """
    Realiza el preprocesamiento de la imagen para mejorar la precisión del OCR.
    Ahora usa un enfoque más suave para preservar el texto.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Opción 1: Sin binarización fuerte, solo escala de grises
    # Esto es a menudo suficiente y preserva más información.
    processed_img = gray

    # Opción 2 (Descomentar si la Opción 1 no funciona bien): Binarización adaptativa
    # La binarización adaptativa es mejor para imágenes con iluminación variable
    # block_size: tamaño de la vecindad para calcular el umbral
    # C: constante restada del promedio ponderado (puede ser 0 o un pequeño número negativo)
    # processed_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Opción 3 (Descomentar si el texto es muy fino): Dilatación para engrosar el texto
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1)) # Ajusta el tamaño del kernel si es necesario
    # processed_img = cv2.dilate(processed_img, kernel, iterations=1)
    
    # Opcional: Eliminar ruido si es necesario (aplicar después de cualquier binarización)
    # processed_img = cv2.medianBlur(processed_img, 3)

    return processed_img

# --- Paso 2: OCR estructurado con pytesseract ---
def ocr_image(image_data):
    """
    Realiza el OCR en la imagen preprocesada y devuelve un DataFrame
    con la información detallada del texto.
    """
    # Convertir array de NumPy a imagen PIL para pytesseract
    pil_img = Image.fromarray(image_data)
    
    # Usar una configuración de Tesseract más específica si es necesario.
    # Por ejemplo, para un modo de segmentación de página (psm)
    # --psm 3 (Default, para texto en una sola columna)
    # --psm 6 (Asume un bloque de texto uniforme)
    # Puedes probar con diferentes PSM si los resultados no son buenos.
    custom_config = r'--oem 3 --psm 6' 
    data = pytesseract.image_to_data(pil_img, lang=TESSERACT_LANG, output_type=pytesseract.Output.DATAFRAME, config=custom_config)
    
    # Filtrar palabras con texto y confianza válida
    data = data[data.text.notnull() & (data.conf != -1)]
    return data

# --- Paso 3: Agrupar líneas y parsear lotes ---
def parse_lotes(data):
    """
    Agrupa las líneas de texto del OCR y las parsea para extraer
    el título, descripción y dimensiones de cada lote.
    """
    lotes = []
    lote_actual = {}
    
    # Ordenar los datos para asegurar que las líneas estén en orden de lectura
    # Importante: Agrupar por 'page_num', 'block_num', 'par_num', 'line_num'
    # Esto asegura el orden correcto de lectura, incluso si Tesseract detecta múltiples bloques.
    data = data.sort_values(by=['page_num', 'block_num', 'par_num', 'line_num', 'word_num']).reset_index(drop=True)

    # Reconstruir líneas de texto
    lines = []
    current_line_text = []
    current_block = -1
    current_par = -1
    current_line = -1

    for index, row in data.iterrows():
        # Comprobar si estamos en una nueva línea lógica
        if row['block_num'] != current_block or \
           row['par_num'] != current_par or \
           row['line_num'] != current_line:
            
            if current_line_text: # Si hay texto en la línea anterior, añadirla a la lista
                lines.append(' '.join(current_line_text).strip())
            
            current_line_text = [str(row['text'])] # Iniciar una nueva línea con el texto actual
            current_block = row['block_num']
            current_par = row['par_num']
            current_line = row['line_num']
        else:
            current_line_text.append(str(row['text'])) # Añadir palabra a la línea actual
    
    if current_line_text: # Añadir la última línea si existe
        lines.append(' '.join(current_line_text).strip())

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detectar número de lote (ej: "1.", "23.", etc.)
        # El patrón se ha hecho más robusto para capturar números seguidos de un punto y espacio o fin de línea.
        # Solo consideramos líneas que empiezan con un número seguido de un punto.
        if re.match(r"^\d+\.\s*.*", line):
            if lote_actual:
                lotes.append(lote_actual)
            
            # Extraer el número de lote y el resto de la línea como título
            # Captura el número. y el resto de la línea
            match = re.match(r"^(\d+\.)\s*(.*)", line)
            if match:
                # Usar toda la línea como título del lote
                lote_actual = {'titulo': line, 'descripcion': '', 'dimensiones': None}
            else: # Fallback si no coincide perfectamente, pero sigue siendo un posible inicio de lote
                lote_actual = {'titulo': line, 'descripcion': '', 'dimensiones': None}
            continue

        # Detectar dimensiones (ej: "M. 0.12 × 0.10", "H. 30 cm", etc.)
        # Un patrón más flexible para capturar "M.", "H.", "W." seguido de números y posibles "x" o "×"
        # y opcionalmente "cm" o "m".
        dim_match = re.search(r"(M\.|H\.|W\.)\s*\d[\d.,]*\s*(?:[xX×]\s*\d[\d.,]*)*\s*(?:cm|m)?", line, re.IGNORECASE)
        
        if dim_match:
            # Si se encuentra una dimensión, la asignamos al lote actual y la eliminamos de la línea
            if lote_actual: # Asegurarse de que hay un lote_actual antes de asignar dimensiones
                lote_actual['dimensiones'] = dim_match.group(0).strip()
                line = line.replace(dim_match.group(0), '').strip() # Eliminar la dimensión de la descripción
            
            # Si la línea solo contenía la dimensión, no hay más descripción
            if not line and lote_actual:
                continue # Pasa a la siguiente línea si la actual solo era la dimensión

        # Si no es un nuevo lote y hay un lote_actual, añadir a la descripción
        if lote_actual:
            # Si la descripción ya tiene contenido, añadir un espacio antes de la nueva línea
            if lote_actual['descripcion']:
                lote_actual['descripcion'] += ' ' + line
            else:
                lote_actual['descripcion'] = line

    # Añadir el último lote si existe
    if lote_actual:
        lotes.append(lote_actual)

    # Limpiar espacios extra y caracteres no deseados en la descripción y título
    for lote in lotes:
        lote['titulo'] = re.sub(r'\s+', ' ', lote['titulo']).strip()
        lote['descripcion'] = re.sub(r'\s+', ' ', lote['descripcion']).strip()
        if lote['dimensiones']:
            lote['dimensiones'] = re.sub(r'\s+', ' ', lote['dimensiones']).strip()

    return lotes

# --- Paso 4: Guardar resultado estructurado ---
def save_to_csv(lotes, output_path):
    """
    Guarda la lista de lotes en un archivo CSV.
    """
    if not lotes:
        print("[!] No se detectaron lotes. El CSV estará vacío.")
    df = pd.DataFrame(lotes)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"[+] Datos guardados en {output_path}")

# --- Main ---
def main():
    try:
        # Paso 1: Preprocesar la imagen
        # Asegúrate de pasar la imagen ORIGINAL aquí, no la preprocesada fallida.
        preprocessed_image_data = preprocess_image(INPUT_IMAGE) 
        
        # Opcional: guardar la imagen preprocesada para inspección
        # cv2.imwrite("catalogo_reprocessed_for_inspection.png", preprocessed_image_data)
        # print("[*] Imagen preprocesada y guardada para inspección como 'catalogo_reprocessed_for_inspection.png'")

        print("[*] Imagen preprocesada.")
        
        # Paso 2: Realizar OCR
        data = ocr_image(preprocessed_image_data)
        
        # Imprimir las primeras filas del DataFrame para depuración
        if not data.empty:
            print("[*] OCR realizado. Primeras filas del DataFrame de OCR:")
            print(data.head())
        else:
            print("[!] OCR realizado, pero no se detectó ningún texto. Verifique el preprocesamiento y la calidad de la imagen.")
            # Si no hay texto, salimos para evitar procesar un DataFrame vacío
            return
            
        print("[*] Parseando texto...")
        
        # Paso 3: Parsear los lotes
        lotes = parse_lotes(data)
        
        # Paso 4: Guardar en CSV
        save_to_csv(lotes, OUTPUT_CSV)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()