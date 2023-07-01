import PySimpleGUI as sg
import os
import editar_perfil as perfil_editar
import configuracion as configuracion
import seleccionar_template_meme as seleccionar_template_meme
import seleccionar_template_collage as seleccionar_template_collage
import etiquetas as etiquetar
from utilidades.constantes import ROOT_PATH
import utilidades.abrir_fotos as abrir_fotos
from layouts import menu as menu_principal

sg.theme ('LightGrey4')

# Se define una funcion para poder llamar al menu principal desde el inicio
def window_menu (perfil):
    
    # Se define el tamaño de la pantalla y se utiliza la funcion resizable para que la pantalla sea redimensionable por el usuario
    window = sg.Window('',menu_principal.get_layout(perfil), element_justification='c', size=(1366,768), resizable=True ) 
    while True:
        event, values = window.read()
        if ((event == sg.WIN_CLOSED) or (event == "Salir")):
            break
        """
        Se llama a la interfaz configuracion y se le pasa el nombre de la funcion que vamos a utilizar, en este caso "conf". 
        Y tambien se pasa por parametro el perfil actual para poder guardar la informacion de este cuando utilize las funcionalidades de "configuracion".
    """
        if event == "configuracion": 
            window.hide()
            print(perfil["Alias"])
            configuracion.conf(perfil["Alias"])
            window.UnHide()
        """
        Cuando se selecciona el boton "ayuda" se hace el popup de una imagen en la cual se explican las funcionalidades que tiene el menu
    """
        if event == "ayuda":
            foto_ayuda = os.path.join(ROOT_PATH,"fotos","ayuda.png")
            sg.popup(image=foto_ayuda)
        """
        Los siguientes if son las llamadas a las demás iterfaces, utilizando las funciones declaradas en los respectivos archivos
    """
        if event == 'editar_perfil':
            perfil = perfil_editar.editar_perfil(perfil)
            #La siguiente linea se utiliza para que aparezcan los cambios realizados cuando se ejecutó editar perfil en el menu princiapl
            window['editar_perfil'].update(image_data=abrir_fotos.abrir(os.path.join(ROOT_PATH,"fotos_usuarios",perfil['Foto']),(200,200)),image_subsample=2)
        if event == 'generar_meme':
            seleccionar_template_meme.window_seleccionar_template(perfil["Alias"])
        if event == 'generar_collage':
            seleccionar_template_collage.window_seleccionar_template(perfil["Alias"])
        if event == 'etiquetar':
            etiquetar.eti(perfil['Alias'])
    window.close()
    return perfil
