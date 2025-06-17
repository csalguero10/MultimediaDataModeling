# compressor_tool.py
# Herramientas básicas de compresión multimedia y de datos en Python
# Autor: [Tu Nombre]
# Fecha: [Fecha Actual]

import zipfile
import zlib
from PIL import Image
import ffmpeg
import os


# 📌 1. Comprimir archivos en ZIP
def compress_to_zip(zip_name, files):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in files:
            zipf.write(file)
            print(f'Archivo añadido a {zip_name}: {file}')
    print(f'Archivo ZIP creado: {zip_name}')


# 📌 2. Comprimir texto en memoria usando zlib
def compress_text(data):
    compressed_data = zlib.compress(data.encode())
    print(f'Tamaño original: {len(data)} bytes')
    print(f'Tamaño comprimido: {len(compressed_data)} bytes')
    return compressed_data


# 📌 3. Comprimir imagen JPEG
def compress_image(input_image, output_image, quality=30):
    img = Image.open(input_image)
    img.save(output_image, quality=quality)
    print(f'Imagen comprimida guardada como {output_image} con calidad {quality}')


# 📌 4. Comprimir video con ffmpeg
def compress_video(input_video, output_video, crf=28):
    ffmpeg.input(input_video).output(output_video, vcodec='libx264', crf=crf).run(overwrite_output=True)
    print(f'Video comprimido guardado como {output_video} con CRF {crf}')


# 📌 Ejemplo de uso de todas las funciones
if __name__ == '__main__':
    # Crear archivo ZIP
    archivos_a_zip = ['documento.txt', 'imagen.png']
    compress_to_zip('archivo_comprimido.zip', archivos_a_zip)

    # Comprimir texto
    texto_original = "Este es un texto que quiero comprimir en memoria con zlib."
    texto_comprimido = compress_text(texto_original)

    # Comprimir imagen JPEG
    if os.path.exists('foto_original.jpg'):
        compress_image('foto_original.jpg', 'foto_comprimida.jpg', quality=30)

    # Comprimir video (requiere ffmpeg instalado)
    if os.path.exists('video_original.mp4'):
        compress_video('video_original.mp4', 'video_comprimido.mp4', crf=28)
