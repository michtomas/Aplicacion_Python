import PySimpleGUI as sg
import os.path
from PySimpleGUI.PySimpleGUI import FolderBrowse, Listbox
import io
from PIL import Image
import csv
import datetime
import imghdr
import json
import configuracion as configuracion
from utilidades import cargar_csv_json
from utilidades import constantes as constante
from utilidades import abrir_fotos
from layouts import etiquetas as layout
import shutil

sg.theme('LightGrey4')

"""La siguiente funcion se hace con el fin listar las imagenes en la listbox"""
def desplegar_lista(ruta_carpeta,window):
    try:
        lista_archivos = os.listdir(ruta_carpeta)
    except:
        lista_archivos =[]
    #desplegamos la lista de archivos que podemos abrir que se encuentren en la carpeta seleccionada    
    nombres_archivos = [
        arc #archivo de la carpeta
        for arc in lista_archivos
        if os.path.isfile(os.path.join(ruta_carpeta, arc))
        and arc.lower().endswith((".png",".gif",".jpg"))
        ]
    window["-ARCHIVOS-"].update(nombres_archivos)


"""La siguiente funcion se hace con el fin de guardar o editar los datos de las imagenes en un csv  """
def guardar_datos(nombre_foto,descripcion,etiquetas,alias):
    try:
        with open(os.path.join(constante.ROOT_PATH,"archivos",'imagenes.csv'), 'r+') as archivo:
            lector = csv.reader(archivo)
            contenido_csv = list(lector)
            imagen = Image.open(nombre_foto)
        #Una vez abierto el archivo procedemos a buscar la foto
        exito =False     
        for i, sublista in enumerate(contenido_csv):
            if nombre_foto in sublista:
                #editamos la fila si se encontro la foto
                fecha = datetime.date.today().strftime("%d/%m/%Y") #actualizamos antes la variable temporal
                contenido_csv[i]=[nombre_foto,descripcion,imagen.size,os.stat(nombre_foto).st_size,imghdr.what(nombre_foto),etiquetas,alias,fecha] #No se porque pero no actualiza el contenido
                cargar_csv_json.sobreescribir_csv(contenido_csv)
                nombre_foto = os.path.basename(nombre_foto)
                cargar_csv_json.cargar_csv(alias,'Modificacion de imagen clasificada',nombre_foto)
                sg.Popup('Imagen actualizada!')
                exito = True
                break
        #Si la foto no se encontro entonces debemos guardar los datos en una nueva linea
        if not exito: 
            cargar_csv_json.guardar_linea_csv(nombre_foto, descripcion, etiquetas,alias)
            nombre_foto = os.path.basename(nombre_foto)
            cargar_csv_json.cargar_csv(alias,'Nueva imagen clasificada',nombre_foto)
    except:
        sg.Popup('Ups! Ha ocurrido un error!')

"""La siguiente funcion se hace con el fin de verificar si la foto seleccionada ya tiene etiquetas, descripcion y metadatos almacenados, y devolverlos """
def buscar_foto(nombre_foto):
    datos_imagen = None
    try:
        with open(os.path.join(constante.ROOT_PATH,"archivos",'imagenes.csv'), 'r') as archivo:
            lector = csv.reader(archivo)
            contenido_csv = list(lector)
        #Una vez abierto el archivo procedemos a buscar la foto
        for i, sublista in enumerate(contenido_csv):
            if nombre_foto in sublista:
                datos_imagen = sublista #Informacion de la imagen que buscamos
                break
    except FileNotFoundError:
        sg.Popup('No se encontro el archivo de imagenes')
    return datos_imagen

""" Esta funcion verifica si las rutas fueron cargadas previamente en la configuracion """            
def cargar_ruta_repositorio(alias):
    #Verifica si el archivo directorio existe, sino lo informa 
    r=''
    if os.path.exists(os.path.join(constante.ROOT_PATH,"archivos",'directorios.json')):
        with open(os.path.join(constante.ROOT_PATH,"archivos",'directorios.json')) as archivo:
            try:
                #cargar rutas cargadas en configuracion
                contenido_archivo = json.load(archivo)
                rutas = list(filter(lambda a: a['Alias']==alias, contenido_archivo))
                r=rutas[0]['R_Imagenes']
            except:
                sg.popup('No se cargo ninguna ruta en configuracion')
    return r
    
#funcion general de la interfaz
def eti(alias):

    #variables editables
    etiquetas = [] 
    descripcion = ''
    ruta_repositorio=cargar_ruta_repositorio(alias)

    #fondo para la zona de la imagen previo a cargar una imagen de la carpeta
    ruta_foto = os.path.join(constante.ROOT_PATH,"fotos","fondo_meme.png")
    cargar_csv_json.crear_csv_imagenes()

    window = sg.Window("Etiquetas", layout.layout(ruta_repositorio,ruta_foto), element_justification= 'c', size=(1366,768), resizable=True)

    while True:
        event, values = window.read(timeout=0)
        if event == "volver" or event == sg.WIN_CLOSED:
            break
        if event == sg.TIMEOUT_EVENT:
            if (ruta_repositorio != ''):
                desplegar_lista(ruta_repositorio,window)    
        if event == "-CARPETA-":
            ruta_carpeta = values["-CARPETA-"]
            desplegar_lista(ruta_carpeta,window)
        elif event == "-ARCHIVOS-":
            #si seleccionamos un archivo de la lista
            try:
                nombre_foto = os.path.join(values["-CARPETA-"], values["-ARCHIVOS-"][0]) #traemos la foto seleccionada
                window["-IMAGEN-"].update(data=abrir_fotos.abrir(nombre_foto,(300, 300)))
                imagen = Image.open(nombre_foto)
                #extraemos los metadatos de la foto cargada en la variable imagen
                window["-METADATOS-"].update("| " + "x".join(map(str, imagen.size))  + " | " + str(os.stat(nombre_foto).st_size) + " | " + imghdr.what(nombre_foto) + " | ")
                #en caso de que la foto seleccionada ya tuviese datos cargados previamente los traemos y visualizamos
                if buscar_foto(nombre_foto) != None:
                    datos_imagen = buscar_foto(nombre_foto)
                    window["-DESCRIPCION-"].update(datos_imagen[1])
                    etiquetas=datos_imagen[5]
                    window["-ETIQUETAS-"].update(etiquetas)
                    etiquetas=[etiquetas] #Como traje un string del csv lo vuelvo a convertir a lista
                else:
                    #resetemos las variables principales, listas para su posterior carga
                    etiquetas = []
                    descripcion = ''
                    window["-DESCRIPCION-"].update(descripcion)
                    window["-ETIQUETAS-"].update(" ".join(map(str, etiquetas)))
            except:
                pass
        if event=='-DESCRIBIR-':
            descripcion = values['-DESCRIBIR TEXT-']
            window["-DESCRIPCION-"].update(descripcion)
        if event=='-ETIQUETAR-':
            #guardamos una etiqueta y la agreamos a la lista de etiquetas
            if isinstance(etiquetas,list):
                etiqueta = "#" + values['-ETIQUETAR TEXT-']
                etiquetas.append(etiqueta)
                window["-ETIQUETAS-"].update(" ".join(map(str, etiquetas)))
                window["-ETIQUETAR TEXT-"].update("")
            else:
                etiqueta = "#" + values['-ETIQUETAR TEXT-']
                etiquetas = etiquetas + ' ' + etiqueta
                etiquetas = etiquetas.replace(' ', '').replace('#', ' #')
                window["-ETIQUETAS-"].update(etiquetas)
                window["-ETIQUETAR TEXT-"].update("")
        if event=='-ELIMINAR-':
            etiqueta = "#" + values['-ELIMINAR TEXT-']
            try:
                etiquetas.remove(etiqueta)
                window["-ETIQUETAS-"].update(" ".join(map(str, etiquetas)))
                window["-ETIQUETAR TEXT-"].update("")
            except(ValueError, AttributeError):
                if etiqueta in etiquetas:
                    etiquetas=etiquetas.replace(etiqueta,"")
                    window["-ETIQUETAS-"].update("".join(map(str, etiquetas)))
                    window["-ETIQUETAR TEXT-"].update("")
                else:
                    if (etiqueta + ' ' in etiquetas[0] + ' '):
                        etiquetas[0]=etiquetas[0].replace(etiqueta,"")
                        window["-ETIQUETAS-"].update("".join(map(str, etiquetas)))
                        window["-ETIQUETAR TEXT-"].update("")
                    else:
                        sg.popup('No exisste la etiqueta')
        if event =='guardar':
            if not values ["-CARPETA-"]:
                sg.popup('Por favor complete todos los campos.')
            else:
                etiquetas = " ".join(map(str, etiquetas)) #convertimos la lista de etiquetas a una cadena para almacenarla en el csv
                etiquetas = etiquetas.replace(' ', '').replace('#', ' #') #eliminamos los espacios que se generan en la conversion
                guardar_datos(nombre_foto,descripcion,etiquetas,alias)
                carpeta_destino = 'fotos'

                if not os.path.exists(carpeta_destino):
                    os.makedirs(carpeta_destino)

                nombre_archivo = os.path.basename(nombre_foto)  # Obtiene solo el nombre del archivo
                ruta_destino = os.path.join(constante.ROOT_PATH, carpeta_destino, nombre_archivo)
                if not os.path.exists(ruta_destino):
                    shutil.copy(nombre_foto, ruta_destino)
    window.close()
