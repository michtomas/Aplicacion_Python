import PySimpleGUI as sg
import os
import io
import configuracion as modulo_configuracion
import utilidades.obtener_imagen_con_texto as obtener_imagen_con_texto
from layouts import generar_meme as layout_generar_meme
import utilidades.cargar_csv_json as cargar_csv_json
from utilidades.constantes import ROOT_PATH

sg.theme ('LightGrey4')

def window_generar_meme(alias, foto, textbox):
    """
    Retorna la ventana de Generar meme.
    """
    
    text1 = ""
    text2 = ""
    fuente = os.path.join(ROOT_PATH,"tipografias","arial.ttf")

    window = sg.Window('',layout_generar_meme.get_layout(foto), element_justification='c', size=(1366,768), resizable=True)

    while True:
        event,values = window.read()

        if event == ('-VOLVER-') or event == sg.WIN_CLOSED:
            break
        if event == ('-GUARDAR-') or event == sg.WIN_CLOSED: 
            repositorio_memes = ""
            ruta_directorios = os.path.join(ROOT_PATH,"archivos","directorios.json")
            datos_json = cargar_csv_json.cargar_lista_json(ruta_directorios)
            for dato in datos_json:
                if (dato["Alias"] == alias):
                    repositorio_memes = dato["R_Memes"]
            
            while True:
                if (repositorio_memes == ""):
                    window.hide()
                    directorios = modulo_configuracion.conf(alias)
                    if (not directorios):
                        sg.popup("Se debe cargar el directorio donde se va a guardar el meme.")
                    else:
                        repositorio_memes = directorios["R_Memes"]
                        break
                    window.UnHide()
                else:
                    break
            imagen = obtener_imagen_con_texto.obtener(foto, text1, text2, fuente, textbox)
            imagen.save(os.path.join(repositorio_memes,foto), format='PNG')
            parametro = ";".join([text1, text2])
            cargar_csv_json.cargar_csv(alias, "nuevo_meme",foto,parametro)
            sg.popup("Se cargó el meme con éxito.")
            window.close()

        if event == ('-TIPOGRAFIA-'):
            fuente = os.path.join(ROOT_PATH,"tipografias",f"{values['-TIPOGRAFIA-']}.ttf")
        if event == ('-TEXTO1-'):
            text1 = values['-TEXTO1-']
        elif event == ('-TEXTO2-'):
            text2 = values['-TEXTO2-']
        if event == "-VISUALIZAR-":
            #Transformamos la imagen en bytes y la mostramos en pantalla.
            imagen = obtener_imagen_con_texto.obtener(foto, text1, text2, fuente, textbox)
            bio = io.BytesIO()
            imagen.save(bio, format="PNG")
            window["-IMAGE-"].update(size=(400,400),subsample=2 ,data=bio.getvalue())
    window.close()
