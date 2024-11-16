import os
import requests
from datetime import datetime

class FileDownloaderProcessor:
    """
    Clase para descargar un archivo según una fecha proporcionada.
    """
    def __init__(self, base_url, download_folder, date_str):
        """
        Inicializa la clase con los parámetros necesarios.
        :param base_url: URL base donde se encuentran los archivos.
        :param download_folder: Carpeta local donde se guardará el archivo descargado.
        :param date_str: Fecha de la cual se construirá la URL del archivo (formato 'YYYY-MM-DD').
        """
        self.base_url = base_url
        self.download_folder = os.path.abspath(download_folder)
        self.date_str = date_str
        
        # Parseamos la fecha proporcionada para extraer el día, mes y año
        self.date = datetime.strptime(date_str, "%Y-%m-%d")
        self.day = self.date.day
        self.month = self.date.month
        self.year = self.date.year
        
        # Construir la URL con la fecha proporcionada
        self.url = self._build_url()

    def _build_url(self):
        """
        Construye la URL dinámica para el archivo basado en la fecha proporcionada.
        La URL se construye en el formato:
        'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'
        """
        return f"{self.base_url}/AGNO_{self.year}/MES_{self.month:02d}/TXT/INT_PBC_EV_H_1_{self.day:02d}_{self.month:02d}_{self.year}_{self.day:02d}_{self.month:02d}_{self.year}.TXT"

    def download_file(self, file_path):
        """
        Descarga el archivo desde la URL construida.
        :return: True si el archivo se descarga correctamente, False si hay un error.
        """

        try:
            # Realizamos la solicitud GET para descargar el archivo
            response = requests.get(self.url)
            response.raise_for_status()  # Lanza un error si la solicitud falla

            # Crear la carpeta si no existe
            os.makedirs(self.download_folder, exist_ok=True)

            # Guardamos el archivo en la carpeta local
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            print(f"\nArchivo descargado y guardado en: {file_path}")
            return True
        except requests.RequestException as e:
            print(f"\nError al descargar el archivo: {e}")
            return False

    def process_file(self, file_path):
        """
        Procesa el archivo descargado. Esta función puede ser personalizada para cualquier tipo de procesamiento.
        En este ejemplo solo imprimimos un mensaje indicando que el archivo ha sido procesado.
        """
        if os.path.exists(file_path):
            print(f"\nProcesando el archivo: {file_path}")
            # Aquí puedes agregar el código para procesar el archivo (por ejemplo, leerlo, formatearlo, etc.)
        else:
            print("No se pudo encontrar el archivo descargado para procesarlo.")

# Ejemplo de uso
if __name__ == "__main__":
    # URL base donde se encuentran los archivos
    base_url = 'https://www.omie.es/sites/default/files/dados'

    # Carpeta local donde se guardará el archivo
    download_folder = 'C:/Users/didac/hackaton/files'

    # Fecha del archivo que queremos descargar (ejemplo: '2023-04-14')
    date_str = '2023-04-14'

    # Crear instancia de la clase
    downloader_processor = FileDownloaderProcessor(base_url, download_folder, date_str)
    
    # Descargar el archivo
    if downloader_processor.download_file():
        # Procesar el archivo descargado
        downloader_processor.process_file()
