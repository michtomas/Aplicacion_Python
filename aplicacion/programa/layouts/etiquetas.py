import PySimpleGUI as sg 
from utilidades.abrir_fotos import abrir

def layout(ruta_repositorio,ruta_foto):
    columna_izquierda = [
        [sg.Text("Directorio de imágenes",size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
         [sg.In(ruta_repositorio, size=(50, 1), enable_events=True, key="-CARPETA-",background_color='skyblue',text_color='black'),
         sg.FolderBrowse('Buscar',button_color='skyblue')],
        [sg.Text("Etiquetar imagen",size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
         [sg.In(size=(50, 1), enable_events=True, key="-ETIQUETAR TEXT-",background_color='skyblue',text_color='black'),
         sg.Button('Etiquetar', key="-ETIQUETAR-",button_color='skyblue')],
        [sg.Text("Agregar descripcion",size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
         [sg.In(size=(50, 1), enable_events=True, key="-DESCRIBIR TEXT-",background_color='skyblue',text_color='black'),
         sg.Button('Modificar', key="-DESCRIBIR-",button_color='skyblue')],
        [sg.Text("Eliminar etiqueta",size=(20, 1), font=('Times New Roman', 25), text_color='Black', justification=("c"))],
         [sg.In(size=(50, 1), enable_events=True, key="-ELIMINAR TEXT-",background_color='skyblue',text_color='black'),
         sg.Button('Eliminar', key="-ELIMINAR-",button_color='skyblue')]
    ]

    columna_derecha = [
        [sg.Text(size=(100,1), key="-DESCRIPCION-")],
        [sg.Image(data=abrir(ruta_foto,(300,300)),key="-IMAGEN-")],
        [sg.Text(size=(200,2), key='-METADATOS-')],
        [sg.Text(size=(200,2), key="-ETIQUETAS-")],
        [sg.Text('')]
    ]

    boton_volver = [[sg.Button("< Volver", size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12),key='volver')]]
    boton_guardar = [[sg.Button('Guardar', size=(20, 2), button_color=('black', 'skyblue'), font=('Helvetica', 12), key='guardar')]]

    columna= [sg.Column(boton_volver, element_justification='left', expand_x=True),
            sg.Column(boton_guardar, element_justification='rigth', expand_x=True)]
    
    layout = [
        [sg.Text("Etiquetar imagenes", font=('Times New Roman', 50), text_color='Black', justification=("c"),size=(20, 1))], 
        [sg.Column(columna_izquierda, justification='right'),
        sg.Text('', size=(10,20)),
        sg.Listbox(values=[], enable_events=True, size=(40, 20),key="-ARCHIVOS-",background_color='skyblue',text_color='black',sbar_arrow_color='black', sbar_background_color='skyblue', highlight_background_color='steelblue',highlight_text_color='white'),
        sg.Text('', size=(10,20)),   
        sg.Column(columna_derecha,justification='left')],
        [columna]
    ]

    return layout