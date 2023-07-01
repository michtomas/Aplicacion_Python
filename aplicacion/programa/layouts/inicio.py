import PySimpleGUI as sg
import utilidades.botones as operaciones_botones

def get_layout(datos_json):
    """
    Esta función retorna el layout del inicio con todos sus botones.
    """
    
    boton_cerrar = [[sg.Button(
        'Cerrar',
        size=(20, 2),
        button_color=('black', 'skyblue'), 
        font=('Comis Sans MS', 12)
        )]]

    #Se verifica que la lista_imagenes sea menor a 4. Si esto es verdadero se crea el texto con la pagina correcta y con el boton "Ver más" desactivado. En el caso de que sea mayor a 4 se habilita el boton "Ver más" y se crea el texto con la pagina correcta. 
    if (len(datos_json) > 4):
        boton_ver_mas = [[sg.Button(
            "Ver más",
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='ver_mas',
            disabled=False),
                sg.Button(
            "Agregar perfil",
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='agregar_perfil')]]
    else:
        boton_ver_mas = [[sg.Button(
            "Ver más",
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='ver_mas',
            disabled=True),
                sg.Button(
            "Agregar perfil",
            size=(20, 2), 
            button_color=('black', 'skyblue'), 
            font=('Helvetica', 12),
            key='agregar_perfil')]]
    
    botones = operaciones_botones.mostrar(datos_json)

    layout = [[sg.Text(
        'UNLP-Image', 
        size=(50, 2), 
        font=('Times New Roman', 75), 
        text_color='Black', 
        justification=("c"))],
            [sg.Text(
        f'Pagina n° 1', 
        key='num_pagina', 
        text_color='Black',
        font=('Times New Roman', 15))],
            [botones],
            [boton_ver_mas],
            [sg.Text('')], 
            [sg.Column(boton_cerrar, element_justification='rigth', expand_x=True)]]
    
    return layout