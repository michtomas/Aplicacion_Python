import PySimpleGUI as sg
import crear_perfil as perfil
import menu_principal as menu
import utilidades.cargar_csv_json as cargar_csv_json
import utilidades.botones as operaciones_botones
from layouts import inicio as layout_inicio

def window_inicio():
    """
    Función que retorna la ventana del inicio.
    """

    i=4

    cargar_csv_json.crear_csv_logs()
    datos_json = cargar_csv_json.cargar_lista_json('perfiles.json')

    window = sg.Window('Inicio', layout_inicio.get_layout(datos_json), element_justification='c', size=(1366,768),resizable=True )

    while True:
        event,values = window.read()
        
        if event == ('Cerrar') or event == sg.WIN_CLOSED:
            break
        if event ==("agregar_perfil"):
            window.hide()
            perfil_cargado = perfil.agregar_perfil()
            #verifica si se uso el agregar perfil, porque puede entrar a crear perfil y no crear ningun perfil
            if (perfil_cargado):
                menu.window_menu(perfil_cargado)
                break
            window.UnHide()

        if event == ("ver_mas"):
            if len(datos_json) > i:
                i = operaciones_botones.actualizar(i, datos_json, window)
            else:
                i = operaciones_botones.actualizar(0, datos_json, window)

        
        #Se verifica por cada 1 de los 4 botones cual fue presionado (si así lo hizo) y una ves se sabe que botón se presionó, se calcula el resto de i (iterador) divido 4 (tamaño total del arreglo de botones) y con esto podemos saber si hay algún boton libre o si estan completos los lugares. Esto nos sirve para calcular cual botón fue presionado.
        for posicion in range(4):
            if event == f'boton{posicion}':
                inicio = i % 4
                if (inicio == 0):
                    inicio = i - 4
                else:
                    inicio = i - inicio

                window.hide()

                datos_json[inicio+posicion] = menu.window_menu(datos_json[inicio+posicion])
                window.close()
            
    window.close()
