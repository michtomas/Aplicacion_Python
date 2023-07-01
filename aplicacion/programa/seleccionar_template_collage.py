import PySimpleGUI as sg
import os
import io
import json
import utilidades.cargar_csv_json as cargar_lista_json
from layouts import seleccionar_template_collage as layout_seleccionar_template
import utilidades.abrir_fotos as abrir_foto
from utilidades.constantes import ROOT_PATH
import generar_collage as generar_collage
from PIL import Image




def window_seleccionar_template(alias):

    #Cargamos los templates en una variable.
    templates = cargar_lista_json.cargar_lista_json("coordenadas.json")

    window = sg.Window('',layout_seleccionar_template.layout_seleccionar_template(templates), element_justification='c', size=(1366,768), resizable=True )

    while True:
        event,values = window.read()

        if event == ("-VOLVER-") or event == sg.WIN_CLOSED:
            break
        
        if event == "-ARCHIVOS-":
            #Seleccionamos un archivo de la lista y lo mostramos.
            try:
                #Buscamos la información de la foto en el archivo de templates.
                for arc in templates:
                    if (arc['name'] == values["-ARCHIVOS-"][0]):
                        datos = arc
                #Mostramos en panalla el meme seleccionado.
                collage_seleccionado = abrir_foto.abrir(os.path.join(ROOT_PATH,"fotos",datos["image"]),(400,400))
                window["-IMAGE-"].update(data=collage_seleccionado)
            except:
                pass
        if event == "-GENERAR-":
            if (values["-ARCHIVOS-"] != []):
                window.Hide()
                #Buscamos la información de la foto en el archivo de templates.
                for arc in templates:
                    if (arc['name'] == values["-ARCHIVOS-"][0]):
                        datos = arc
                #collage_seleccionado = os.path.join(ROOT_PATH,"fotos",datos["image"])
                textbox = (datos["text_boxes"])
                generar_collage.window_generar_collage(alias,datos)
                window.UnHide()
    window.close()