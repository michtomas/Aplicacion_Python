from PIL import Image
from PIL import ImageDraw
import os
from PIL import ImageFont
from utilidades.constantes import ROOT_PATH

def ajustar_tamano_tipografia(texto, max_tamano, font_path, tamano_textbox):
    """
    Ajusta el tamaño de la tipografía pasada por parametro de acuerdo al texto, tamaño maximo, ancho y alto del recuadro.
    """

    font_size = 1
    font = ImageFont.truetype(font_path, font_size)

    #Obtenemos la cadena de texto de largo maximo.
    tamano_texto = max(texto.split('\n'), key=len)

    #Obtenemos la altura del texto multiplicando la cantidad de cadenas por el tamaño de tipografía.
    altura_texto = len(texto.split('\n'))

    # Ajusta gradualmente el tamaño de la tipografía hasta el ancho máximo multiplicado por 0.9 (obtenemos el 90 % de la foto como margen de seguridad). El bucle se realiza mientras la linea mas larga sea menor al tamaño de la imagen o hasta que se haya alcanzado el tamaño de tipografia maximo.
    while ((font.getsize(tamano_texto)[0] < tamano_textbox[0] * 0.9) and 
           (font_size < max_tamano) and
           (altura_texto * font.getsize(tamano_texto)[1]  < tamano_textbox[1] * 0.9)):
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)

    # Reduce el tamaño de la tipografía en una unidad para que se ajuste completamente
    font_size -= 1
    font = ImageFont.truetype(font_path, font_size)

    return font

# Función para agregar texto a una imagen
def obtener(foto, text1, text2, fuente, textbox):
    """
    Retora en bytes la imagen (pasada por parametros) "dibujada" con los textos y tipografía pasados por parametro.
    """ 
    
    imagen = Image.open(os.path.join(ROOT_PATH,"fotos",foto)).convert("RGB")
    
    draw = ImageDraw.Draw(imagen)

    for posicion in range (1,3):
        #Inicializamos el lugar donde se posiciona el recuadro. 
        pos_x = textbox[posicion-1]["top_left_x"]
        pos_y = textbox[posicion-1]["top_left_y"]
        pos_x_abajo = textbox[posicion-1]["bottom_right_x"]
        pos_y_abajo = textbox[posicion-1]["bottom_right_y"]
        coordenadas= (pos_x, pos_y)

        tamano_textbox = (pos_x_abajo - pos_x, pos_y_abajo - pos_y)
        
        #Inicializamos la letra
        font = ajustar_tamano_tipografia(eval(f"text{posicion}"), 25, fuente, tamano_textbox)

        # Crea una nueva imagen con el texto ajustado
        draw.text(coordenadas, eval(f"text{posicion}"), font=font, fill="black")
    
    return imagen

def obtener_collage(foto, titulo, fuente):
    """
    Retora en bytes la imagen (pasada por parametros) "dibujada" con los textos y tipografía pasados por parametro.
    """ 
    
    #imagen = Image.open(os.path.join(ROOT_PATH(),"fotos",foto)).convert("RGB")
    
    draw = ImageDraw.Draw(foto)


    #Inicializamos el lugar donde se posiciona el recuadro. Como es igual en todas las plantillas se lo manda estandarizado
    pos_x = 46
    pos_y = 855
    pos_x_abajo = 694
    pos_y_abajo = 922
    coordenadas= (pos_x, pos_y)

    tamano_textbox = (pos_x_abajo - pos_x, pos_y_abajo - pos_y)
        
    #Inicializamos la letra
    font = ajustar_tamano_tipografia(titulo, 25, fuente, tamano_textbox)
    # Crea una nueva imagen con el texto ajustado
    draw.text(coordenadas,titulo, font=font, fill="black")
    
    return foto    