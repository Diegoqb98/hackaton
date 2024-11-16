import os

from src.infrastructure.formatter.precio_marginal_i import PrecioMarginalIFormatter
from src.infrastructure.formatter.precio_marginal_txt import PrecioMarginalTxTFormatter


class FileHandler:
    """
    Clase para manejar la lectura, formateo y escritura de archivos.
    """
    api_format_map = {
        "precio_marginal_txt": PrecioMarginalTxTFormatter,
        "precio_marginal_i": PrecioMarginalIFormatter,
    }

    def __init__(self, input_file, output_file):
        """
        Inicializa la clase con las rutas de archivo.
        :param input_file: Ruta del archivo de entrada.
        :param output_file: Ruta del archivo de salida.
        """
        self.input_file = os.path.abspath(input_file)
        self.output_file = os.path.abspath(output_file)

    def process_and_write(self, api_type, **kwargs):
        """
        Procesa el archivo de entrada según el tipo de API y guarda los resultados.
        :param api_type: Tipo de API que determina el formateo.
        :param kwargs: Argumentos adicionales para el formateador.
        """
        try:
            # Verificar si el tipo de API está soportado
            if api_type not in self.api_format_map:
                raise ValueError(f"Tipo de API no soportado: {api_type}")

            # Obtener el formateador correspondiente
            formatter = self.api_format_map[api_type]

            # Leer y procesar el archivo
            with open(self.input_file, 'r') as file:
                formatter.format(file, self.output_file,**kwargs)
    
        except Exception as e:
            print(f"\nOcurrió un error al procesar el archivo: {e}")


# Ejemplo de uso
if __name__ == "__main__":
    # Definir las rutas de los archivos de entrada y salida
    input_file = './files/marginal.1'  # Sustituye con la ruta correcta del archivo de entrada
    output_file = './files/output.csv'  # Sustituye con la ruta del archivo de salida

    # Crear instancia de FileHandler
    handler = FileHandler(input_file, output_file)

    # Llamar al método `process_and_write` para procesar el archivo de acuerdo con el tipo de API (por ejemplo, 'precio_marginal')
    # Si necesitas pasar parámetros adicionales, puedes hacerlo como kwargs (por ejemplo, pasando parámetros como coeficientes)
    handler.process_and_write('precio_marginal', coef_apuntamiento={'1': 1.1, '2': 1.2, '3': 1.3})  # Pasa parámetros según sea necesario
