import PySimpleGUI as sg
import utilidades.abrir_fotos as abrir
import os
from utilidades.constantes import ROOT_PATH
#import obtener_rutas as obtener_rutas

def layout_collage(fotos,alias,plantilla):
    plantilla = os.path.join(ROOT_PATH,"fotos",plantilla)
    #imagenes, _ = obtener_rutas.obtener(alias)
    boton_volver = [[sg.Button("< Volver", 
                size=(20, 2), 
                button_color=('black', 'skyblue'), 
                font=('Helvetica', 12),
                key='-VOLVER-')]]
    boton_guardar = [[sg.Button('Guardar', 
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='-GUARDAR-')]]
    boton_etiqueta = [[sg.Button(
            'Ir a etiquetar', 
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='-ETIQUETAR-')]]
    columna= [sg.Column(
        boton_volver, 
        element_justification='left', 
        expand_x=True),
        sg.Column(
        boton_etiqueta, 
        element_justification='left', 
        expand_x=True),
            sg.Column(
        boton_guardar, 
        element_justification='rigth', 
        expand_x=True)]
    columna_izquierda = [[sg.Text(
        'Seleccionar imagenes: ', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('left'))],
        [sg.Listbox(
        values=fotos, 
        enable_events=True, 
        size=(40, 20),
        key="-ARCHIVOS-",
        background_color='skyblue',
        text_color='black',
        sbar_arrow_color='black', 
        sbar_background_color='skyblue', 
        highlight_background_color='steelblue',
        highlight_text_color='white')],
        [sg.Button(
            'Agregar imagen',
            size=(20, 2),
            button_color=('black', 'skyblue'),
            font=('Helvetica', 12),
            key='-AGREGAR-'
        )],
        [sg.Text(
        'Agregar titulo: ', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('left'))],
        [sg.In(size=(50, 1), 
        enable_events=True, 
        key="-TEXTO-",
        background_color='skyblue',
        text_color='black'),
        sg.Button('Enter', 
        key="-ENTER-",
        button_color='skyblue')]
    ]
    columna_derecha =[
        [sg.Text(
        'Previsualización', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('right'))],
        [sg.Image(
        data=abrir.abrir(plantilla,(400,400)), 
        key='-IMAGE-',
        size=(400,400),
        subsample=0)]
    ]
    layout =[ 
        [sg.Text(
        'Generar Collage', 
        size=(20, 1), 
        font=('Times New Roman', 75), 
        text_color='Black', 
        justification=("c"))],
        [sg.Column(columna_izquierda,justification='c'),
        sg.Column(columna_derecha,justification='c')],  
        [columna]]
    
    return layout