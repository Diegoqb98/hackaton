# import requests
# import os

# # URL del archivo a descargar
# # url = 'https://www.omie.es/es/file-download?parents%5B0%5D=marginalpdbc&filename=marginalpdbc_20241116.1'
# url = 'https://www.omie.es/sites/default/files/dados/AGNO_2020/MES_04/TXT/INT_PBC_EV_H_1_11_04_2020_11_04_2020.TXT'

# # Carpeta local donde se guardará el archivo
# download_folder = 'C:/Users/didac/hackaton/files'  # Cambia esta ruta según lo necesites

# # Nombre del archivo a guardar
# filename = url.split('=')[-1]

# # Obtener la ruta completa donde se guardará el archivo
# file_path = os.path.join(download_folder, filename)

# # Hacer la solicitud GET para descargar el archivo
# response = requests.get(url)

# # Verificar si la solicitud fue exitosa (código de estado 200)
# if response.status_code == 200:
#     # Crear la carpeta si no existe
#     os.makedirs(download_folder, exist_ok=True)

#     # Guardar el archivo en la carpeta local
#     with open(file_path, 'wb') as file:
#         file.write(response.content)
    
#     print(f"El archivo se ha descargado y guardado en: {file_path}")
# else:
#     print(f"Error al descargar el archivo. Código de estado: {response.status_code}")
from datetime import date, datetime
import requests
import os
import lib.convertirArchivo as conv

# URL del archivo a descargar
url = 'https://www.omie.es/sites/default/files/dados/AGNO_2023/MES_04/TXT/INT_PBC_EV_H_1_14_04_2023_14_04_2023.TXT'

# Carpeta local donde se guardará el archivo
download_folder = 'C:/Users/didac/hackaton/files'  # Cambia esta ruta según lo necesites

# Obtener el nombre del archivo desde la URL (última parte de la URL después del último '/')
filename = url.split('/')[-1]

# Obtener la ruta completa donde se guardará el archivo
file_path = os.path.join(download_folder, filename)

# Obtener la fecha y hora actual
today = date.today()
now = datetime.now()

# Hacer la solicitud GET para descargar el archivo
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Crear la carpeta si no existe
    os.makedirs(download_folder, exist_ok=True)
    
    # Guardar el archivo descargado
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    print(f"El archivo se ha descargado y guardado en: {file_path}")

    # Obtener los precios del archivo descargado
    precios = conv.obtener_precios_esp(file_path)

    print(precios)
    # Guardar los precios en un nuevo archivo de texto
    # file_path_with_timestamp = file_path.replace('.TXT', f_{now.strftime("%Y%m%d_%H%M%S")}.txt')
    file_path_with_timestamp = 'hola'
    
    with open(file_path_with_timestamp, 'w', encoding='utf-8') as f:
        # Escribir los precios extraídos en el archivo de salida
        f.write("Precios Marginales del Sistema Español (EUR/MWh)\n")
        f.write(",".join(map(str, precios)))  # Convertir los precios a una cadena separada por comas
    print(f"Los precios se han guardado en: {file_path_with_timestamp}")
else:
    print(f"Error al descargar el archivo. Código de estado: {response.status_code}")
