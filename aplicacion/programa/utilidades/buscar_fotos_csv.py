from utilidades.constantes import ROOT_PATH 
import os
import pandas as pd


def buscar_csv(alias):
    ruta_csv = os.path.join(ROOT_PATH, 'archivos', 'perfiles.csv') 
    try:
        data_csv = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        print("Error al cargar el archivo 'perfiles.json'")
    except ValueError:
        print("Error al cargar el archivo 'perfiles.json'")
    operaciones = ['Nueva imagen clasificada', 'Modificacion de imagen clasificada']
    fotos = data_csv[data_csv['Operacion'].isin(operaciones) & (data_csv['Nick'] == alias)]
    fotos = fotos["Valores"].unique()
    return fotos
