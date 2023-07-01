import PySimpleGUI as sg
import os
import json
import utilidades.cargar_csv_json as cargar
from layouts import crear_perfil as layout
import utilidades.abrir_fotos as abrir_fotos
import utilidades.constantes as constante
import shutil

def agregar_perfil():
    """
    Se ejecuta una ventana con campos para llenar con informacion acerca del nuevo perfil que se creara y se carga
    este nuevo perfil en el perfiles.json, y tambien se actualiza la lista datos que contiene los perfiles cargados.
    """
    #imagen predeterminada
    ruta_imagen = os.path.join(constante.ROOT_PATH,"fotos","usuario.png")
    usuario_nuevo = {}

    ruta_completa = os.path.join(constante.ROOT_PATH,"archivos","perfiles.json") 
    if os.path.getsize(ruta_completa)>0:
        try:
            with open(ruta_completa,'r') as archivo:
                datos = json.load(archivo)
                ok = True
        except:
            print('')
    else:  
        datos = []
        ok = False

    window= sg.Window("Crear nuevo perfil",layout.layout(), element_justification='c', size=(1366,768), resizable=True )
    
    while True:
        event,values = window.read()

        #cambio de imagen de usuario
        if event == '-AVATAR-':
            ruta_imagen = sg.popup_get_file('Seleccionar avatar', no_window=True, file_types=(('Imagenes', '*.png *.jpg *.jpeg *.gif *.bmp *.tiff'),))
            if not ruta_imagen:
                ruta_imagen = os.path.join(os.getcwd(),"fotos","usuario.png")
            elif ruta_imagen:
                try:
                    window['-AVATAR_IMAGE-'].update(data=abrir_fotos.abrir(ruta_imagen,(150,150)))

                except Exception as e:
                    sg.popup_error(f'Error al cargar la imagen: {e}')
        #cerrado
        if event=="CANCELAR" or event== sg.WINDOW_CLOSED or event == "volver":
            break

        #guardado del perfil
        if event=='Guardar':

            #verificacion campos completos
            if any(len(values[key]) == 0 for key in values) or values['Genero'] == 'Selecciona una opcion':
                sg.popup('Por favor complete todos los campos.')
                continue
 
            alias = values[0]
            nombre = values[1]

            #verificacion edad sea un entero
            while True:
                try:
                    edad = int(values[2])
                    break
                except ValueError:
                    sg.popup('Por favor ingrese un número entero válido para la edad.')
                    event, values = window.read()#se declara de vuelta para que lea el nuevo valor de edad ingresado
                    continue
            foto = ruta_imagen

            #como guardar el genero
            if values['Genero'] == 'Otro':
                genero = sg.popup_get_text("Complete manualmente su genero")
                while genero is None or genero.strip() == '':
                    # Se ejecuta si el usuario presiona Cancelar o no ingresa ningún valor.
                    sg.popup('Debe ingresar un valor para su género')
                    genero = sg.popup_get_text("Complete manualmente su genero")
            else:
                genero = values['Genero']

            carpeta_destino = 'fotos_usuarios'
            
            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino)
            
            foto = os.path.basename(ruta_imagen)
            ruta_destino = os.path.join(carpeta_destino,foto)
            shutil.copy(ruta_imagen,ruta_destino)


            #guardado de datos
            usuario_nuevo = {"Nombre": nombre,"Edad": edad,"Alias":alias,"Genero":genero,"Foto":foto}

            #verificar alias unico
            if datos != []:
                alias_existente = any(map(lambda d: d["Alias"] == alias, datos))
                if alias_existente:
                    while True:
                        nuevo_alias = sg.popup_get_text("Ese alias ya existe, ingrese otro")
                        if nuevo_alias is None or nuevo_alias == '':
                            continue
                        elif nuevo_alias == alias or any(map(lambda d: d["Alias"] == nuevo_alias, datos)):
                            continue
                        else:
                            usuario_nuevo['Alias'] = nuevo_alias
                            break
                   
            cargar.cargar_json(usuario_nuevo,ok,datos)#llama al modulo para cargar json
            
            cargar.cargar_csv(usuario_nuevo["Alias"],"Creo perfil")#llama al modulo para cargar csv
            
            sg.popup('Perfil creado con exito')         
            break
    window.close()
    return usuario_nuevo

