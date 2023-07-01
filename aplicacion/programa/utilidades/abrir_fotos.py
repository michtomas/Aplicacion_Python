import PySimpleGUI as sg
import io
from PIL import Image
#Se crea esta función para poder abrir las fotos en formatos diferentes al png convirtiendolos en bytes.
def abrir(ruta_foto, tamano):
    """
    Se abre la foto desde la ruta (que debe ser pasada por parametro) solo para lectura en formato binario, de esa manera obteniendo los bytes respectivos de la imagen y 
    utilizando el PIL se lee y se la reacomoda en un tamaño de 400x400, guardandandola y enviando a traves del return los bytes de la imagen.
"""
    try:
        with open(ruta_foto, 'rb') as file:
            img_bytes = file.read()
            image = Image.open(io.BytesIO(img_bytes))
            image.thumbnail(tamano)
            bio = io.BytesIO()
            image.save(bio, format='PNG')
        return bio.getvalue()
    except FileNotFoundError:
        sg.popup ("Error: No se encontró la imagen en la ruta especificada")
    except Exception as e:
        sg.popup ("Error desconocido: ",str(e))
    return None  