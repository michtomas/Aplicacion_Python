import PySimpleGUI as sg 
import os
import utilidades.abrir_fotos as abrir_fotos
from utilidades.constantes import ROOT_PATH

def get_layout(perfil):
    boton_volver = [[sg.Button("< Volver", size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12),key='volver')]]
    boton_guardar = [[sg.Button('Guardar', size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12))]]
    columna= [sg.Column(boton_volver, element_justification='left', expand_x=True),
              sg.Column(boton_guardar, element_justification='rigth', expand_x=True)]
    
    ruta_foto = os.path.join(ROOT_PATH,"fotos_usuarios",perfil['Foto'])
    #layout
    layout = [[sg.Text('Editar perfil', size=(20, 1), font=('Times New Roman', 75), text_color='Black', justification=("c"))],
          [sg.Text('Nick o alias', size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.Text(f'-{perfil["Alias"]}-',size=(20, 1), font=('Helvetica', 15), text_color='Black', justification=("c"))],
          [sg.Text('Nombre',size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.InputText(perfil["Nombre"],background_color='skyblue', size=(50,1), font=('Helvetica', 10))],
          [sg.Text('Edad',size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.Input(perfil["Edad"],background_color='skyblue', size=(50,1), font=('Helvetica', 10))],
          [sg.Text('Genero autopercibido',size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
          [sg.Combo(['Masculino','Femenino','Otro'],default_value=perfil["Genero"],key='Genero',size=(50,1),readonly=True,background_color='skyblue',font=('Helvetica', 10),button_arrow_color=('black'))], #combo es una lista desplegable
          [sg.Image(abrir_fotos.abrir(ruta_foto,(150,150)),key='-AVATAR_IMAGE-')],
          [sg.Button("Seleccionar avatar",key='-AVATAR-',button_color=('black', 'skyblue'), font=('Helvetica', 12))],
          [columna]]
    return layout
