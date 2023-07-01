import os
import PySimpleGUI as sg 

def layout():
    #imagen predeterminada
    ruta_imagen = os.path.join(os.getcwd(),"fotos","usuario.png")

    boton_volver = [[sg.Button("< Volver", size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12),key='volver')]]
    boton_guardar = [[sg.Button('Guardar', size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12))]]
    columna= [sg.Column(boton_volver, element_justification='left', expand_x=True),
              sg.Column(boton_guardar, element_justification='rigth', expand_x=True)]
                                  

    #layout
    layout = [[sg.Text('Nuevo Perfil', size=(20, 1), font=('Times New Roman', 75), text_color='Black', justification=("c"))],
          [sg.Text('Nick o alias', size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.InputText(background_color='skyblue', size=(50,1), font=('Helvetica', 10))],
          [sg.Text('Nombre',size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.InputText(background_color='skyblue', size=(50,1), font=('Helvetica', 10))],
          [sg.Text('Edad',size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.Input(background_color='skyblue', size=(50,1), font=('Helvetica', 10))],
          [sg.Text('Genero autopercibido',size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.Combo(['Masculino','Femenino','Otro'],default_value='Selecciona una opcion',key='Genero',size=(50,1),readonly=True,background_color='skyblue',font=('Helvetica', 10),button_arrow_color=('black'))], #combo es una lista desplegable
          [sg.Image(ruta_imagen,size=(150,150), key='-AVATAR_IMAGE-',subsample=10)],
          [sg.Button("Seleccionar avatar",key='-AVATAR-',button_color=('black', 'skyblue'), font=('Helvetica', 12))],
          [columna]]
    return layout
