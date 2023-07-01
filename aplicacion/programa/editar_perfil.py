import PySimpleGUI as sg
import json
import utilidades.constantes as constante
import utilidades.cargar_csv_json as cargar
from layouts import editar_perfil as layout_editar
import utilidades.abrir_fotos as abrir_fotos
import os
import shutil


def editar_perfil(perfil):
    """
    Se ejecuta una ventana donde se muestra el alias del perfil, inmutable, y sus respectivos datos cargados anteriormente,
    estos datos se pueden cambiar con nuevos datos, editando la informacion de ese perfil, en el archivo perfiles.json se 
    reemplazara la informacion de ese usuario con la informacion nueva cargada, y en el archivo csv se informara en caso de 
    que el usuario haya cambiado su foto
    """

    cambio_foto = False
    datos_modificados = perfil
    foto = perfil['Foto']
    with open(os.path.join(constante.ROOT_PATH,"archivos","perfiles.json")) as archivo:
        contenido_archivo = json.load(archivo)

    #creacion ventana
    window = sg.Window("Editar perfil",layout_editar.get_layout(perfil),size=(1366,768), element_justification='c', resizable=True )
    #ejecucion ventana
    while True:
        event,values = window.read()
        #cerrado
        if event == sg.WINDOW_CLOSED or event == "volver":
            break
        
        #eleccion de imagen
        if event == '-AVATAR-':
            ruta_imagen = sg.popup_get_file('Seleccionar avatar', no_window=True, file_types=(('Imagenes', '*.png *.jpg *.jpeg *.gif *.bmp *.tiff'),))
            if ruta_imagen:
                try:
                    window['-AVATAR_IMAGE-'].update(data=abrir_fotos.abrir(ruta_imagen,(150,150)))
                    cambio_foto = True #asi no da error 
                except Exception as e:
                    sg.popup_error(f'Error al cargar la imagen: {e}')

        #guardado
        if event == 'Guardar':
            
            nombre = values[0]
            #verificacion edad sea un entero
            while True:
                try:
                    edad = int(values[1])
                    break
                except ValueError:
                    sg.popup('Por favor ingrese un número entero válido para la edad.')
                    event, values = window.read()#se declara de vuelta para que lea el nuevo valor de edad ingresado
                    continue

            #como guardar el genero
            if values['Genero'] == 'Otro':
                genero = sg.popup_get_text("Complete manualmente su genero")
                while genero is None or genero.strip() == '':
                    # Se ejecuta si el usuario presiona Cancelar o no ingresa ningún valor.
                    sg.popup('Debe ingresar un valor para su género')
                    genero = sg.popup_get_text("Complete manualmente su genero")
            else:
                genero = values['Genero']
            
            #verificacion para saber si hay que modificar la variable foto
            if cambio_foto:
                foto = ruta_imagen

                carpeta_destino = 'fotos_usuarios'

                if not os.path.exists(carpeta_destino):
                    os.makedirs(carpeta_destino)

                nombre_archivo = os.path.basename(foto)
                ruta_destino = os.path.join(constante.ROOT_PATH, carpeta_destino, nombre_archivo)
                shutil.copy(foto, ruta_destino)

            #nuevos datos
            datos_modificados = {"Nombre":nombre,"Edad":edad,"Alias":perfil["Alias"],"Genero":genero,"Foto":foto}
            if perfil!= datos_modificados:
                cargar.cargar_csv(perfil["Alias"],"Edito su perfil")
            #sobreescritura del JSON con nuevos datos si hubo, sino esta igual
            with open(os.path.join(constante.ROOT_PATH,"archivos",'perfiles.json'),'w') as archivo:
                for elem in contenido_archivo:
                    if elem["Alias"] == perfil["Alias"]:
                        elem.update(datos_modificados)
                json.dump(contenido_archivo,archivo,indent=2)

            sg.Popup("Perfil editado con exito")
            break
    window.close()
    return datos_modificados
