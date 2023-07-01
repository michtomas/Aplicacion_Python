import csv
import json
import datetime
import os
import datetime
from PIL import Image
import imghdr
from utilidades.constantes import ROOT_PATH
import PySimpleGUI as sg
#agregar al archivo CSV. Valores y texto sirven para Generar Meme y Generar Collage.
def cargar_csv(alias, accion, valores=',', texto=','):
    ruta_archivo = os.path.join('archivos', 'perfiles.csv')
    timestamp = int(datetime.datetime.now().timestamp())
    try:
        with open(ruta_archivo, 'a', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow([timestamp, alias, accion, valores, texto])
    except FileNotFoundError:
        print("No se pudo abrir el archivo 'perfiles.csv'")

#agregar al archivo JSON
def cargar_json(usuario_nuevo,ok,datos):
    ruta_archivo = os.path.join('archivos','perfiles.json')
    try:
        with open(ruta_archivo,'w') as archivo:
            datos.append(usuario_nuevo)
            if ok:
                json.dump(datos,archivo,indent= 2)
                archivo.write('\n') # se agrega un salto de línea para escribir la siguiente lista en la siguiente línea
            else:
                json.dump(datos,archivo,indent=2)
                archivo.write('\n')
    except FileNotFoundError:
        print("No se pudo abrir el archivo 'perfiles.json'")

def cargar_lista_json(nombre):
    """
    Esta función retorna la lista de datos. Puede devolverla vacia en caso de que el archivo no exista o en el caso de que sea vacío.
    """
    #Se verifica si el archivo existe, si es asi se lo abre en modo lectura. En el case de que el archivo no exista se lo abre en modo escritura y se crea la lista de imagenes vacia.

    if not os.path.exists('archivos'):
        os.makedirs('archivos')

    ruta_archivo = os.path.join('archivos',nombre)

    if os.path.exists(ruta_archivo):
        with open(ruta_archivo,'r') as archivo:
            #Se verifica si el archivo esta vacio, si es asi se crea la lista de imagenes vacia. Si el archivo no esta vacio se carga lista_imagenes con los datos.
            if (os.stat(ruta_archivo).st_size == 0):
                datos_json=[]
            else:
                datos = json.load(archivo)
                datos_json = list(map(lambda elem : elem,datos))
    else:
        with open(ruta_archivo,'w') as archivo:
            datos_json=[]

    return datos_json

def crear_csv_logs():
    """
    Esta función crea el archivo con el nombre se pasa por parametro, en el caso de que ya se haya creado se informa en pantalla.
    """

    if not os.path.exists('archivos'):
        os.makedirs('archivos')
    
    ruta_archivo = os.path.join('archivos','perfiles.csv')
    if not (os.path.exists(ruta_archivo)):
        try:
            with open(ruta_archivo,'w', newline='') as archivo_csv:
                writer = csv.writer(archivo_csv)
                writer.writerow(['Timestamp','Nick','Operacion','Valores','Textos'])
        except:
            print("Error con el archivo 'perfiles.csv'")    

def crear_csv_imagenes():
    """
    Esta función crea el archivo con el nombre se pasa por parametro, en el caso de que ya se haya creado se informa en pantalla.
    """

    if not os.path.exists('archivos'):
        os.makedirs('archivos')
    #creamos el archivo csv en caso de que no exista
    if not (os.path.exists(os.path.join(ROOT_PATH,"archivos",'imagenes.csv'))):
        with open(ROOT_PATH,"archivos",'imagenes.csv','w', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow(['Ubicación','Descripción','Resolución','Tamaño','Tipo','Etiquetas','Ultimo Perfil','Fecha'])

"""La siguiente funcion se hace con el fin de guardar una nueva foto que no tenia descripcion y eitquetas previamente cargadas  """
def guardar_linea_csv(nombre_foto,descripcion,etiquetas,alias):
    try: 
        fecha = datetime.date.today().strftime("%d/%m/%Y")
        with open (os.path.join(ROOT_PATH,"archivos",'imagenes.csv'),'a',newline='') as archivo:
            imagen = Image.open(nombre_foto)
            writer = csv.writer(archivo)
            writer.writerow([nombre_foto,descripcion,imagen.size,os.stat(nombre_foto).st_size,imghdr.what(nombre_foto),etiquetas,alias,fecha])
            sg.Popup('¡Nueva foto guardada con éxito!')
    except:
        sg.popup('Por favor seleccione la imagen.')

"""Esta funcion sobreescribe el archivo imagenes csv con los datos editados"""
def sobreescribir_csv(contenido_csv):
    with open(os.path.join(ROOT_PATH,"archivos",'imagenes.csv'), 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        [writer.writerow(fila) for fila in contenido_csv]
