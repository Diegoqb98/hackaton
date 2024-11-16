import json
import csv

class PriceCalculatorFromFile:
    """
    Clase para calcular los precios marginales de la península y los precios estimados para Baleares
    basados en un archivo de precios marginales (output.csv) y un coeficiente de apuntamiento horario.
    """

    def __init__(self, config_file, input_file, coef_apuntamiento_key="hora_coef_apuntamiento"):
        """
        Inicializa la clase con los parámetros necesarios.
        :param config_file: Ruta al archivo JSON con la configuración.
        :param input_file: Ruta al archivo de precios marginales (output.csv).
        :param coef_apuntamiento_key: Clave para acceder al coeficiente de apuntamiento en el JSON.
        """
        self.config_file = config_file
        self.input_file = input_file
        self.coef_apuntamiento_key = coef_apuntamiento_key
        self.config = self.load_config(config_file)
        self.coef_apuntamiento = self.extract_coef_apuntamiento()
        
        # Cargamos los precios desde el archivo CSV
        self.precios_marginales = self.load_precios_from_file(input_file)

    def load_config(self, config_file):
        """
        Carga la configuración desde el archivo JSON.
        :param config_file: Ruta al archivo JSON.
        :return: Diccionario con los datos de configuración.
        """
        with open(config_file, 'r') as file:
            return json.load(file)

    def extract_coef_apuntamiento(self):
        """
        Extrae el coeficiente de apuntamiento horario desde el archivo de configuración.
        :return: Diccionario con coeficientes de apuntamiento.
        """
        return self.config.get(self.coef_apuntamiento_key, {})

    def load_precios_from_file(self, input_file):
        """
        Lee el archivo CSV de precios marginales y extrae los valores de precios.
        :param input_file: Ruta al archivo de precios marginales (output.csv).
        :return: Lista de precios marginales de la península.
        """
        precios_marginales = []

        with open(input_file, 'r') as file:
            reader = csv.reader(file, delimiter=',')  # Usar coma como delimitador si los precios están separados por comas

            # Leer la única fila con los precios
            for i, row in enumerate(reader):
                if i == 0:  # Solo procesamos la primera fila
                    precios_marginales = [float(precio.strip().replace(',', '.')) for precio in row]
                    break  # No es necesario seguir buscando
        return precios_marginales

    def calculate_prices(self):
        """
        Calcula los precios marginales de la península en €/kWh y los precios estimados para Baleares.
        :return: Una tupla con dos listas: precios de la península y precios estimados para Baleares.
        """
        # Convertir los precios marginales de la península de €/MWh a €/kWh
        precios_peninsula = [precio / 1000 for precio in self.precios_marginales]

        # Calcular los precios estimados para Baleares aplicando el coeficiente de apuntamiento
        precios_baleares = []
        for hora in range(24):
            # Obtener el coeficiente para esta hora
            coef = float(self.coef_apuntamiento.get(str(hora), 1))  # Valor por defecto 1 si no existe el coef
            precio_baleares_hora = self.precios_marginales[hora] * coef / 1000  # Convertir a €/kWh
            precios_baleares.append(precio_baleares_hora)

        return precios_peninsula, precios_baleares

    def display_prices(self):
        """
        Muestra los precios marginales calculados para la península y Baleares.
        """
        precios_peninsula, precios_baleares = self.calculate_prices()

        # Mostrar los resultados
        print("\nPrecios marginales de la península por hora (€/kWh):")
        print(precios_peninsula)

        print("\nPrecios estimados para Baleares por hora (€/kWh):")
        print(precios_baleares)


# Ejemplo de uso
if __name__ == "__main__":
    # Ruta al archivo de configuración JSON
    config_file = 'configuracion.json'
    
    # Ruta al archivo de precios marginales (output.csv)
    input_file = 'output.csv'
    
    # Crear la instancia de la clase PriceCalculatorFromFile
    calculator = PriceCalculatorFromFile(config_file, input_file)
    
    # Mostrar los precios
    calculator.display_prices()
