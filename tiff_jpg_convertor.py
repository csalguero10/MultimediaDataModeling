from PIL import Image
import os

# 📌 Convertir imagen TIFF a JPEG
def convert_tiff_to_jpg(input_image, output_image, quality=85):
    try:
        with Image.open(input_image) as img:
            rgb_img = img.convert('RGB')  # Convertir a RGB si no lo está
            rgb_img.save(output_image, 'JPEG', quality=quality)
            print(f'Imagen convertida y guardada como {output_image} con calidad {quality}')
    except Exception as e:
        print(f'Error al convertir imagen: {e}')

# 📌 Ejemplo de uso
if __name__ == '__main__':
    if os.path.exists('imagen_original.tiff'):
        convert_tiff_to_jpg('imagen_original.tiff', 'imagen_convertida.jpg', quality=85)
    else:
        print('No se encontró imagen_original.tiff en el directorio.')
