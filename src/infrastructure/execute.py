from src.application.calcular_prod_fotovoltaica import EnergyProductionCalculator
from src.application.calculo_precio_kw_h import PriceCalculatorFromFile
from src.infrastructure.benefition_calculator import BeneficioEstimation
from src.infrastructure.config.config import Configuracion
from src.infrastructure.db import DatabaseConnector
from src.infrastructure.descargar_archivo import FileDownloaderProcessor
from src.infrastructure.leer_archivo import FileHandler


class MainExecutor:
    """
    Clase que ejecuta el flujo completo de cálculo, descarga, procesamiento de archivos y cálculo de precios.
    """
    def __init__(self, input_file, output_file, config_file, base_url, download_folder, date_str,api_type):
        """
        Inicializa la clase con los parámetros necesarios.
        :param input_file: Ruta al archivo de entrada (por ejemplo, precios marginales).
        :param output_file: Ruta al archivo de salida (donde se escriben los resultados).
        :param config_file: Ruta al archivo de configuración JSON.
        :param base_url: URL base para descargar archivos.
        :param download_folder: Carpeta local donde se descargarán los archivos.
        :param date_str: Fecha específica para los cálculos y las descargas.
        :param api_type: Tipo de api
        """
        self.input_file = input_file
        self.output_file = output_file
        self.config_file = config_file
        self.base_url = base_url
        self.download_folder = download_folder
        self.date_str = date_str
        self.api_type = api_type

    def run(self, api_type):
        """
        Ejecuta el flujo completo: descarga de archivos, cálculo de energía, procesamiento de precios y escritura de resultados.
        """
        # Crear la instancia de la clase Configuracion
        config = Configuracion(self.config_file)
        
        # Crear la instancia de la clase EnergyProductionCalculator
        calculator = EnergyProductionCalculator(config, 1) # 100% efectividad
        
        # Calcular la energía para la fecha proporcionada
        produccion_energia = calculator.calculate_energy(self.date_str)
        
        print(produccion_energia)

        # Crear instancia de FileDownloaderProcessor para descargar el archivo
        downloader_processor = FileDownloaderProcessor(self.base_url, self.download_folder, self.date_str, self.api_type)
        
        # Descargar y procesar el archivo
        if downloader_processor.download_file(self.input_file):
            downloader_processor.process_file(self.input_file)

        # Crear instancia de FileHandler y procesar el archivo
        handler = FileHandler(self.input_file, self.output_file)
        handler.process_and_write(api_type)

        # Crear la instancia de PriceCalculatorFromFile y mostrar los precios
        price_calculator = PriceCalculatorFromFile(self.config_file, self.output_file)
        
        # Precios energia KW/h calculado
        precios_peninsula, precios_baleares = price_calculator.calculate_prices()

        price_calculator.display_prices()

        # Crear la instancia de la clase
        beneficio_estimator = BeneficioEstimation(produccion_energia, precios_peninsula, precios_baleares,config)

        # Calcular el beneficio estimado
        beneficio = beneficio_estimator.calcular_beneficio()

        # Mostrar el resultado
        print(f"Beneficio en la Península: {beneficio} €")


        beneficio = beneficio_estimator.calcular_beneficio(False)
        print(f"Beneficio en Baleares: {beneficio} €")

        # db = DatabaseConnector(
        #     db_name="mi_base_datos",
        #     user="mi_usuario",
        #     password="mi_contraseña",
        #     host="localhost",
        #     port=5432
        # )

        # db.insert_produccion_energia(data_produccion)
        # db.insert_precios_peninsula(data_precios_peninsula)
        # db.insert_precios_baleares(data_precios_baleares)
        # db.insert_produccion_energia(data_produccion)

