import PySimpleGUI as sg
import utilidades.abrir_fotos as abrir_foto
from utilidades.constantes import ROOT_PATH
import os

#Inicializamos los botones con los primeros elementos de la lista y/o elementos vacios. SE USA AL MOMENTO DEL INICIO. SE CREO POR EL CASO EN QUE EL TAMAÑO DE LA LISTA SEA MENOR O IGUAL A 4
def mostrar(datos_json):
    """
    Se cargan los botones con su respectiva foto y en caso de que haya menos de 4 botones para mostrar se invisibilizan las posiciones para la cual no hay cargados.
    """

    # Se inicializan los botones en vacío.
    botones = [0, 0, 0, 0]
    i=0

    #Recorre 4 posiciones verificando si la lista es menor que el puntero (osea si existe un botón cargado para esa posicion). Si es así carga la foto, sino hace invisible el botón.
    for j in range(4):
        if len(datos_json) > i:
            botones[j] = sg.Button(
                image_data=abrir_foto.abrir(os.path.join(ROOT_PATH,"fotos_usuarios",datos_json[i]['Foto']),(200,200)),
                image_size=(150, 150),
                border_width=0,
                key=f'boton{j}',
            )
            i += 1
        else:
            botones[j] = sg.Button(
                image_size=(150, 150),
                border_width=0,
                key=f'boton{j}',
                visible=False,
            )

    return botones

#Esta función es similar a mostrar_botones pero la diferencia que tiene es que en este se actualizan los botones creados en mostrar_botones.
def actualizar(i, datos_json, window):
    """
    Esta función actualiza con los proximos 4 datos cargados los botones. Se pasa el "i" como parametro para poder ir avanzando en la lista de datos.
    """
    
    window['num_pagina'].update(f'Pagina n° {(i // 4) + 1}')
    for j in range(4):
        if i < len(datos_json):
            window[f'boton{j}'].update(
                image_data=abrir_foto.abrir(os.path.join(ROOT_PATH,"fotos_usuarios",datos_json[i]['Foto']),(200,200)),
                image_size=(150, 150),
                visible=True
            )
            i+=1
        else:
            window[f'boton{j}'].update(visible=False)
    return i
