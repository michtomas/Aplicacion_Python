import PySimpleGUI as sg
import json
from layouts import configuracion as layout
import utilidades.cargar_csv_json as cargar_json_csv
from utilidades.constantes import ROOT_PATH
import os

#Color de fondo
sg.theme('LightGrey')
def conf(alias):
    
    contenido_archivo = cargar_json_csv.cargar_lista_json('directorios.json')

    #Inicializo las tres variables y en el caso de que esten en el archivo se cargan.
    repositorio =  ""
    collages =  ""
    memes = ""
    for dato in contenido_archivo:
        if ([dato["Alias"]][0] == alias): #Se compara el alias en la posicion 0 ya que dato["alias"] es una lista con el alias pasado por parametro
            repositorio = dato["R_Imagenes"]
            collages = dato["R_Collage"]
            memes = dato["R_Memes"]

    #ventana
    window = sg.Window('Configuración', layout.get_layout(repositorio, collages, memes), element_justification='c', size=(1366,768), resizable=True)

    #eventos
    while True:
        event, values = window.read()
        if (event == sg.WIN_CLOSED):
            break
        if (event == 'volver'):
            #Nos movemos al menu principal
            break
        if (event == 'Guardar'):
            #Aca cargamos las rutas que se seleccionan con el browse
            if values['-Repositorio-']!='': 
                repositorio= values['-Repositorio-']
            if values['-Memes-']!='':
                memes= values['-Memes-']
            if values['-Collages-']!='':
                collages= values['-Collages-']

            #Verificamos que ninguno de los 3 campos no este vacio, ya sea por una carga actual o que recien lo estemos inicializando.
            if ((repositorio) and (memes) and (collages)):
                esta = False #La variable "esta" funciona para saber si tiene que sobreescribir o crear. 
                datos_modificados = ({"Alias":alias,"R_Imagenes": repositorio,"R_Collage": collages,"R_Memes":memes}) #Creamos el diccionario con los datos
                ruta_archivo= os.path.join(ROOT_PATH,"archivos",'directorios.json')
                with open(ruta_archivo,'w') as archivo:
                    for elem in contenido_archivo:
                        if elem["Alias"] == alias:
                            elem.update(datos_modificados)
                            esta = True
                    if not(esta):
                        contenido_archivo.append({"Alias":alias,"R_Imagenes": repositorio,"R_Collage": collages,"R_Memes":memes})
                    json.dump(contenido_archivo,archivo,indent=2)
                
                #Se carga en el archivo csv la modificación.
                cargar_json_csv.cargar_csv(alias,"Hizo cambios en la configuracion")

                sg.Popup('¡Rutas cargadas con éxito!')
                window.hide()
                return datos_modificados
            else:
                sg.popup('Por favor complete todos los campos.')
    window.close()