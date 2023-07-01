import PySimpleGUI as sg

def get_layout(repositorio, collages, memes):
    
    #Layout para acomodar el boton ed guardar
    boton_volver = [[sg.Button("< Volver", size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12),key='volver')]]
    boton_guardar = [[sg.Button('Guardar', size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12))]]
    columna= [sg.Column(boton_volver, element_justification='left', expand_x=True),
              sg.Column(boton_guardar, element_justification='rigth', expand_x=True)]

    #layout principal
    layout = [
        [sg.Text("Configuración", size=(50, 1), font=('Times New Roman', 75), text_color='Black', justification=("c"))],
        [sg.Text('',font=('Times New Roman', 30))],
        [sg.Text("Repositorio de Imagenes", key="-MOSTRAR TEXTO-", size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
        [sg.In(repositorio, key="-Repositorio-", background_color='skyblue', text_color='Black', border_width=1, enable_events=True, readonly=True), 
         sg.FolderBrowse('Seleccionar', button_color=('black', 'skyblue'), size=(10,1))],
        [sg.Text('')],
        [sg.Text("Directorio de collages", key="-MOSTRAR TEXTO-",  size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
        [sg.In(collages,key="-Collages-", background_color='skyblue', text_color='Black', border_width=1, enable_events=True, readonly=True), 
         sg.FolderBrowse('Seleccionar', button_color=('black', 'skyblue'), size=(10,1))],
        [sg.Text('')],
        [sg.Text("Directorio de memes", key="-MOSTRAR TEXTO-",  size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
        [sg.Input(memes, key="-Memes-", background_color='skyblue', text_color='Black', border_width=1, enable_events=True, readonly=True), 
         sg.FolderBrowse('Seleccionar', button_color=('black', 'skyblue'), size=(10,1))],
        [sg.Text('')],
        [(columna)]
    ]
    return layout
