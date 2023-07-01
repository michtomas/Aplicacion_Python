import PySimpleGUI as sg
from PIL import Image 
from layouts import generar_collage as generar_collage 
import os
import configuracion as modulo_configuracion
from utilidades import cargar_csv_json 
import utilidades.abrir_fotos as abrir
import tempfile
import etiquetas as etiquetar
import utilidades.buscar_fotos_csv as buscar_csv
from utilidades.constantes import ROOT_PATH
import io
import utilidades.obtener_imagen_con_texto  as obtener_collage 
sg.theme ('LightGrey4')



def window_generar_collage(alias,datos):
    fotos = buscar_csv.buscar_csv(alias) 
    plantilla = datos["image"] #Se toma de "datos" (que son los datos de la plantilla seleccionada) el nombre de la plantilla
    """Se toma de "datos" la text_boxes que figuran para la plantilla. Las cuales son utilizadas para leer las posiciones
    en las cuales hay que poner las imagenes"""
    textbox = datos["text_boxes"] 
    """Se declara una variable espacios_ocupados que se utilizará luego en el programa para comparar con la cantidad de text_boxes"""
    espacios_ocupados = 0 
    fotos_elegidas = []
    imagenes_seleccionadas = []
    texto_ingresado_titulo = ""
    window = sg.Window('',generar_collage.layout_collage(fotos,alias,plantilla), element_justification='c', size=(1366,768), resizable=True )
    while True:
        event, values = window.read()
        if event == ("-VOLVER-") or event == (sg.WINDOW_CLOSED):
            break
        coordenadas=[]
        """Esta variable indica la cantidad total de coordenadas presentes  en la plantilla seleccionada y por ende la cantidad de 
        veces que se va a iterar para colocar las imagenes seleccionadas. """
        cantidad_textboxes = len(textbox)
        for i in range(cantidad_textboxes):
                coordenadas.append((textbox[i]["top_left_x"], textbox[i]["top_left_y"]))
            #variables que se pasan para poder hacer el resize de la imagen
        pos_x = textbox[0]["top_left_x"]
        pos_y = textbox[0]["top_left_y"]
        pos_x_abajo = textbox[0]["bottom_right_x"]
        pos_y_abajo = textbox[0]["bottom_right_y"]

        x = pos_x_abajo - pos_x
        y = pos_y_abajo - pos_y

            
        if event == '-AGREGAR-':
            """Se evalua que la variable de espacios_ocupados declarada previamente sea menor a la cantidad de text_boxes
            definidos para la plantilla seleccionada"""
            if espacios_ocupados < len(textbox):

                if values["-ARCHIVOS-"]:
            
                    imagen_seleccionada = values["-ARCHIVOS-"][0]
                    #se agregan a una lista previamente definida las imagenes elegidas por el usuario
                    fotos_elegidas.append(imagen_seleccionada)
                    ruta_imagen = os.path.join(ROOT_PATH, 'fotos', imagen_seleccionada)
                    #se abre la imagen para luego poder hacer el resize de la misma y que coincida con el espacio que tiene que ocupar en el collage
                    imagen = Image.open(ruta_imagen)
                    nueva_imagen = imagen.resize((x,y))

                    
                    # Pega la imagen seleccionada en el siguiente espacio libre del collage
                    coordenadas_siguiente = coordenadas[espacios_ocupados]
                    imagenes_seleccionadas.append((nueva_imagen, coordenadas_siguiente))

                    # Incrementa el contador de espacios ocupados
                    espacios_ocupados += 1

                    ruta = os.path.join(ROOT_PATH,'fotos',plantilla)
                    plantilla_modificada = Image.open(ruta)

                    # Crea una copia de la plantilla modificada
                    plantilla_modificada_copia = plantilla_modificada.copy()

                    # Itera sobre las imágenes seleccionadas y las pega en el collage
                    for nueva_imagen, coordenadas in imagenes_seleccionadas:
                        plantilla_modificada_copia.paste(nueva_imagen, coordenadas)
                    # Guarda la plantilla modificada en un archivo temporal
                    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                    temp_file_path = temp_file.name
                    plantilla_modificada_copia.save(temp_file_path)
                    temp_file.close()
                    temp_file_path = abrir.abrir(temp_file_path,(400,400))
                    # Actualiza el collage en la ventana
                    window['-IMAGE-'].update(temp_file_path)
        if event == "-ENTER-":
            texto_ingresado_titulo = values['-TEXTO-']
            #Se evalua que todas las fotos esten cargadas en el collage, de no ser asi no se puede poner un titulo al collage
            if espacios_ocupados < len(textbox):
                sg.popup('Complete el collage antes de ingresar un titulo')
            else: 
                #se evalua que se haya ingresado un texto
                if texto_ingresado_titulo:
                    #se settea por defecto una tipografia
                    fuente = os.path.join(ROOT_PATH,"tipografias","arial.ttf")
                    #se llama a la funcion obtener_collage
                    imagen = obtener_collage.obtener_collage(plantilla_modificada_copia, texto_ingresado_titulo, fuente) 
                    bio = io.BytesIO()
                    imagen.save(bio, format="PNG")
                    #Actualiza la imagen con el texto ingresado
                    window["-IMAGE-"].update(size=(400,400),subsample=2 ,data=bio.getvalue())
                else:
                    sg.popup("Ingrese un titulo.") 
        """El evento etiquetar se hace con el fin de que si el usuario no tiene ninguna foto etiquetada o quiere etiquetar alguna en el momento
        que esta generando el collage para agregarla en el mismo pueda ir directamente a la pantalla de etiquetar sin tener que perder la plantilla
        que habia seleccionado previamente"""
        if event == "-ETIQUETAR-":
            window.hide()
            etiquetar.eti(alias)
            window.UnHide()
            """Se busca en el csv las imagenes etiquetadas del usuario para poder listarlas en la listbox. Si se etiquetó alguna
            foto nueva va a aparecer como opcion para usarse en el collage"""
            fotos = buscar_csv.buscar_csv(alias) 
            #se actualiza la listbox para que aperzcan todas las fotos etiquetadas por el usuario
            window["-ARCHIVOS-"].update(fotos)
        if event == "-GUARDAR-":
            if  texto_ingresado_titulo == "":
                sg.popup('Antes de guardar ingrese un titulo en el collage')
            else:
                #Evalua que el collage esté terminado
                if espacios_ocupados < len(textbox):
                    sg.popup("Quedaron espacios vacios en el collage")
                else:
                    repositorio_collage = ""
                    ruta_directorios = os.path.join(ROOT_PATH,"archivos","directorios.json")
                    datos_json = cargar_csv_json.cargar_lista_json(ruta_directorios)
                    for dato in datos_json:
                        if (dato["Alias"] == alias):
                            repositorio_collage = dato["R_Collage"]
                    
                    while True:
                        if (repositorio_collage == ""):
                            window.hide()
                            directorios = modulo_configuracion.conf(alias)
                            if (not directorios):
                                sg.popup("Se debe cargar el directorio donde se va a guardar el collage.")
                            else:
                                repositorio_collage = directorios["R_Collage"]
                                break
                            window.UnHide()
                        else:
                            break

                    while True:
                        texto_ingresado = sg.popup_get_text('Ingrese el nombre de la foto:', 'Guardar foto')
                        
                        if not texto_ingresado:  # Verificar si el usuario ha cancelado la entrada
                            break
                        
                        parametro = f'{texto_ingresado}.png'  # Agrega la extensión ".png" al nombre
                        imagen = plantilla_modificada_copia
                        
                        try:
                            imagen.save(os.path.join(repositorio_collage, parametro), format='PNG')
                        except OSError:
                            sg.popup('El nombre ingresado no corresponde para el guardado de un archivo')
                        except Exception as e:
                            sg.popup(f"Ocurrió un error: {e}")
                        else:
                            nombres_fotos = ";".join(fotos_elegidas)
                            cargar_csv_json.cargar_csv(alias, "nuevo_collage", nombres_fotos, texto_ingresado_titulo)
                            sg.popup("El collage se guardó con éxito.")
                            break  # Sale del bucle while cuando se guarda con éxito

                    window.close()
        
    window.close()
