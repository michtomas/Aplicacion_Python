import streamlit as st
import pandas as pd
import calendar
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import utilidades.constantes as constante
import os

def porcentajes_genero(data_set_json):
    if data_set_json.empty:
        st.write("No se encontraron usuarios en el archivo json")
    else:
        st.write("Se tomaron todos los géneros de los usuarios y se hizo un gráfico de torta con los porcentajes de géneros")
        generos = data_set_json["Genero"].value_counts().sort_values(ascending=False)

        etiquetas = list(generos.index)
        data_dibujo = list(generos.values)

        plt.pie(data_dibujo, labels=etiquetas, autopct='%1.1f%%',
                shadow=True, startangle=120, labeldistance=1.1)
        plt.axis('equal')
        plt.legend(etiquetas)

        plt.title("Uso por género")
        plt.show()

def dias_semana(data_set_csv):
    st.write("Grafico que muestra los dias en los que se realizaron operaciones")
    data_set_csv["Timestamp"] = pd.to_datetime(data_set_csv["Timestamp"], unit='s', origin='unix')
    data_set_csv['Timestamp'] = data_set_csv['Timestamp'].dt.tz_localize('UTC')  # Establecer la zona horaria como UTC
    data_set_csv['Día de la semana'] = data_set_csv['Timestamp'].dt.day_name()

    # Obtener el recuento de registros para cada día
    conteo_dias = data_set_csv['Día de la semana'].value_counts()

    # Obtener los nombres de los días en español
    dias_semana_es = list(calendar.day_name)

    # Crear la gráfica de barras
    conteo_dias = conteo_dias.reindex(index=dias_semana_es)  # Reordenar los datos según los nombres en español
    conteo_dias.plot(kind='bar')

    # Personalizar la gráfica
    plt.xlabel('Día de la semana')
    plt.ylabel('Cantidad')
    plt.title('Cantidad de operaciones por día de la semana')

def cantidad_operaciones(data):
    st.write("Se tomaron todas las operaciones hechas por los usuarios y se hizo un grafico comparando las mismas")
    operaciones = data["Operacion"].value_counts().sort_values(ascending=False)#ordena segun cant. operaciones
    if(len(operaciones)>0):
        operaciones.plot(kind='bar')
        plt.xlabel('Operaciones')
        plt.ylabel('Cantidad')
        plt.title('Grafico de operaciones')
    else:
        st.write("No se encontraron operaciones hechas por los usuarios")
    

def cant_operaciones_usuarios(data):
    st.write("Grafico que informa la cantidad de operaciones hechas por cada usuario")
    #groupby en la columna "Nick" del DataFrame data para agrupar los datos por usuario.
    #Luego, utilizamos el método size() para contar el número de filas correspondiente a cada grupo.
    operaciones_por_usuario = data.groupby("Nick").size()
    operaciones_por_usuario = operaciones_por_usuario.sort_values(ascending=False)#ordenar por cant. operaciones
    
    categorias = operaciones_por_usuario.index #tiene cargado los alias

    operaciones = operaciones_por_usuario.values.T #tiene la cantidad de operaciones

    fig, ax = plt.subplots()
    ax.barh(categorias, operaciones, label=f'Operaciones')
    ax.invert_yaxis()
    # Configurar el gráfico
    ax.set_xlabel('Nombres')
    ax.set_ylabel('Total de Operaciones')
    ax.set_title('Gráfico de Barras Apilado')
    ax.legend()
    if(len(operaciones) > 0):
        plt.show()
    else:
        st.write("No se encontraron operaciones hechas por usuarios")

def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off")
    

def generar_nube_memes(data):
    st.write("Se tomaron los textos de los memes creados y se creo una nube con estas palabras")
    info = data.loc[data['Operacion'] == 'nuevo_meme']
    texto = info["Textos"]
    if(len(texto)>0):
        # Reiniciar el índice
        texto = texto.reset_index(drop=True)
        
        # Filtrar los caracteres numéricos
        texto_sin_numeros = texto.str.replace('\d+', '')
        
        text = texto_sin_numeros.to_string(index=False) #textos sin los numeros
        text = str(text.split(';'))
        text = str(text.replace("'",''))
        # Generate wordcloud
        wordcloud = WordCloud(width = 300, height = 200, random_state=1, background_color='white', colormap='Set2', collocations=False, stopwords = STOPWORDS).generate(text)
        # Plot
        plot_cloud(wordcloud)
    else:
        st.write("No se encontraron textos utilizados en memes")

def generar_nube_collage(data):
    st.write("Se tomaron los titulos de los collages creados y se creo una nube con estas palabras")
    info = data.loc[data['Operacion'] == 'nuevo_collage']
    texto = info["Textos"]
    if(len(texto) > 0):
        # Reiniciar el índice
        texto = texto.reset_index(drop=True)
        
        # Filtrar los caracteres numéricos
        texto_sin_numeros = texto.str.replace('\d+', '')
        
        text = texto_sin_numeros.to_string(index=False) #textos sin los numeros
        # Generate wordcloud
        wordcloud = WordCloud(width = 300, height = 200, random_state=1, background_color='white', colormap='Set2', collocations=False, stopwords = STOPWORDS).generate(text)
        # Plot
        plot_cloud(wordcloud)
    else:
        st.write("No se encontraron textos usados en collages")

def ranking_imagenes_memes(data):
    st.write("Se tomaron las imagenes usadas por los usuarios para generar memes y se hizo un ranking de estas")
    info = data.loc[data['Operacion'] == 'nuevo_meme', ['Operacion', 'Valores']]
    cant = info["Valores"].value_counts().sort_values(ascending=False)
    cant = cant.reset_index()
    if(len(cant)>0):
        st.write(cant)
    else:
        st.write("No se encontraron imagenes usadas en memes")

def ranking_imagenes_collage(data):
    st.write("Se tomaron las imagenes usadas por los usuarios para generar collages y se hizo un ranking de estas")
    info = data.loc[data['Operacion'] == 'nuevo_collage', ['Operacion', 'Valores']]
    cant = info["Valores"].str.split(';').explode().reset_index(drop=True).value_counts()
    cant = cant.reset_index()
    if(len(cant)>0):
        st.write(cant)
    else:
        st.write("No se encontraron imagenes usadas en collages")
    
def porcentaje_operaciones_por_genero(df_csv, json_data):
    if data_set_json.empty:
        st.write("No se encontraron usuarios en el archivo json")
    else:
        st.write("Se genero un grafico con los porcentajes de genero, segun las personas que clasificiaron una nueva imagen, o modificaron imagenes etiquetadas")
        # Combinar los datos del archivo CSV y JSON basándose en el campo 'Nick' y 'Alias'
        merged_data = pd.merge(df_csv,json_data, left_on='Nick', right_on='Alias')

        #La operación de fusión combinará los datos de ambos DataFrames en función de los valores de las columnas especificadas como claves de fusión.
        # En este caso, la fusión se realizará utilizando los valores de las columnas "Nick" y "Alias" para encontrar las coincidencias.
        # Filtrar las operaciones deseadas
        operaciones_deseadas = ['Nueva imagen clasificada', 'Modificación de imagen previamente clasificada']
        filtered_data = merged_data[merged_data['Operacion'].isin(operaciones_deseadas)]

        # Calcular los porcentajes por género
        porcentajes = filtered_data['Genero'].value_counts(normalize=True) * 100

        # Crear gráfico de torta con los porcentajes
        plt.pie(porcentajes, labels=porcentajes.index, autopct='%1.1f%%')
        plt.title('Operaciones por género')

if __name__ == "__main__":
    ruta_csv = os.path.join(constante.ROOT_PATH,'archivos','perfiles.csv') 
    ruta_json = os.path.join(constante.ROOT_PATH,'archivos','perfiles.json')
    try:
        data_set_csv = pd.read_csv(ruta_csv)#carga el csv
    except FileNotFoundError:
        print("Error al cargar el archivo 'perfiles.csv'")
    try:
        data_set_json = pd.read_json(ruta_json)#carga el json
    except FileNotFoundError:
        print("Error al cargar el archivo 'perfiles.json'")
    except ValueError:
        print("Error al cargar el archivo 'perfiles.json'")
        data_set_json = pd.DataFrame()

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.header('Logs de UNLP Image')

    if st.button("Porcentajes por genero"):
        #grafico porcentajes
        st.subheader("Se calculo el porcentaje del genero de los usuarios y en base a esto se hizo el grafico")
        st.pyplot(porcentajes_genero(data_set_json))

    if st.button("Operaciones hechas por dia"):

        #grafico cantidad de operaciones por dia
        st.subheader("Grafico que compara los dias de la semana en los que se realizaron operaciones")
        st.pyplot(dias_semana(data_set_csv))

    if st.button("Operaciones por usuarios"):
        #grafico que ordena segun el uso de cada operacion
        st.subheader("Grafico que compara entre las operaciones hechas por los usuarios")
        st.pyplot(cantidad_operaciones(data_set_csv))

    if st.button("Cantidad de operaciones de cada usuario"):
        st.pyplot(cant_operaciones_usuarios(data_set_csv))

    if st.button("Nube de palabras con textos de Generar Meme"):
        st.pyplot(generar_nube_memes(data_set_csv))

    if st.button("Nube de palabras con textos de Generar Collage"):
        st.pyplot(generar_nube_collage(data_set_csv))

    if st.button("Ranking de las imagenes mas usadas para los memes"):
        st.pyplot(ranking_imagenes_memes(data_set_csv))

    if st.button("Ranking de las imagenes mas usadas para los collages"):
        st.pyplot(ranking_imagenes_collage(data_set_csv))

    if st.button("Porcentaje segun genero de las personas que crearon imagen clasificada ó modificaron imagen previamente clasificada"):
        st.pyplot(porcentaje_operaciones_por_genero(data_set_csv,data_set_json))