import PySimpleGUI as sg
import os
import utilidades.abrir_fotos as abrir_foto
from utilidades.constantes import ROOT_PATH

def get_layout(foto):
    """
    Se obtiene el layout de generar meme.
    """

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

    columna= [sg.Column(
            boton_volver, 
            element_justification='left', 
            expand_x=True),
            sg.Column(
            boton_guardar, 
            element_justification='rigth', 
            expand_x=True)]


    # Obtener la lista de nombres de tipografías disponibles eliminando el ".ttf" y poniendo la primer letra en mayuscula.
    directorio = os.listdir(os.path.join(ROOT_PATH,"Tipografias"))
    tipografias = [fichero.split(".")[0].title() for fichero in directorio]

    columna_izquierda = [
        [sg.Text('Seleccionar una tipografía',
                size=(20, 1), 
                font=('Times New Roman', 25), 
                text_color='Black', 
                justification=("c"))],
         [sg.Combo(tipografias,
                key='-TIPOGRAFIA-', 
                size=(30,1),
                default_value="Arial",
                enable_events=True,
                readonly=True,
                background_color='skyblue',
                font=('Helvetica', 15),
                text_color="black",
                button_arrow_color=('black'),
                button_background_color='skyblue')],
        [sg.Text("Texto 1",
                size=(20, 1), 
                font=('Times New Roman', 25), 
                text_color='Black', 
                justification=("c"))],        
         [sg.Multiline(size=(50, 5),
                no_scrollbar=True,
                enable_events=True, 
                key="-TEXTO1-",
                background_color='skyblue',
                text_color='black')],
         [sg.Text("Texto 2",
                size=(20, 1), 
                font=('Times New Roman', 25), 
                text_color='Black', 
                justification=("c"))],        
         [sg.Multiline(size=(50, 5), 
                no_scrollbar=True,
                enable_events=True, 
                key="-TEXTO2-",
                background_color='skyblue',
                text_color='black')],
        [sg.Button(
            "Visualizar",
            font=('Helvetica', 12),
            size=(20,2),
            key="-VISUALIZAR-",
            button_color='skyblue')]
         ]

    columna_derecha= [[sg.Text('Previsualización', 
        size=(30, 1), 
        font=('Times New Roman', 15), 
        text_color='Black', 
        justification=('c'))],
        [sg.Image(
        data= abrir_foto.abrir(os.path.join(ROOT_PATH,"Fotos",foto),(400,400)),
        key='-IMAGE-', 
        size=(400,400),
        subsample=0)]]

    layout = [
        [sg.Text('Generar Meme', 
        size=(20, 1), 
        font=('Times New Roman', 75), 
        text_color='Black', 
        justification=("c"))],
        [sg.Column(columna_izquierda, justification='c'),
        sg.Column(columna_derecha, justification='c')],
            [columna]]
    
    return layout