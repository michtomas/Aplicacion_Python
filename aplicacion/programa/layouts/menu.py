from utilidades.constantes import ROOT_PATH
import utilidades.abrir_fotos as abrir_fotos
import os
import PySimpleGUI as sg

def get_layout(perfil):
    # Rutas de las fotos predeterminadas para el uso de la interfaz
    ruta_fotos1 = os.path.join(ROOT_PATH,"fotos","configuracion.png")
    ruta_fotos2 = os.path.join(ROOT_PATH,"fotos","signo.png")
    ruta_perfil = os.path.join(ROOT_PATH,"fotos_usuarios",perfil['Foto'])
    # Declaracion de los botones de configuracion y ayuda, se declaran de esta manera para poder acomodarlos correctamente en la pantalla
    boton_ayuda=[[sg.Button(key ='configuracion', button_color=('LightGrey', 'grey'),image_data=abrir_fotos.abrir(ruta_fotos1,(200,200)),border_width=0, image_subsample=2),
                 sg.Button(key ='ayuda', button_color=('LightGrey', 'grey'), image_data=abrir_fotos.abrir(ruta_fotos2,(200,200)),border_width=0,image_subsample=2)]]
    # Se declara la manera en la que aparece el perfil seleccionado en el menu principal, este es importado desde el inicio y aparece la foto y el alias del usuario
    boton_imagen=[[sg.Button(image_data=abrir_fotos.abrir(ruta_perfil,(200,200)),image_subsample=2,key='editar_perfil')],
        [sg.Text((f"-{perfil['Alias']}-"),justification='center', size=(10, 1), font=('Helvetica', 12), border_width=2, text_color='black')]]
    # Se utiliza para acomodar los botones previamente declarado es una misma linea y con sus respectivas justificaciones
    barra_principal = [[sg.Column(boton_imagen, element_justification='left', expand_x=True),
                        sg.Column(boton_ayuda, element_justification='rigth', expand_x=True)]]
    
    # Declaracion del Layout, se utiliza la "barra_principal" previamente declarada y se ubican debajo de esta los botones para llamar a las distintas interfaces
    layout = [[barra_principal],
        [sg.Button("Etiquetar Imagenes", size=(40, 4), button_color=('Black', 'mediumpurple'), font=('Helvetica', 17), border_width=2, key='etiquetar')], 
        [sg.Button("Generar Meme", size=(40, 4), button_color=('Black', 'LightBlue'), font=('Helvetica', 17), border_width=2,key='generar_meme')],
        [sg.Button("Generar Collage", size=(40, 4), button_color=('Black', 'skyblue'), font=('Helvetica', 17), border_width=2,key='generar_collage')],
        [sg.Button("Salir", size=(40, 4), button_color=('Black', 'steelblue'), font=('Helvetica', 17), border_width=2)]
    ]
    return layout
