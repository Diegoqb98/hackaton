class BaseFormatter:
    """
    Clase base para los formateadores. Todas las clases específicas deben heredar de esta.
    """
    @staticmethod
    def format(file, **kwargs):
        """
        Método que debe ser implementado por las clases hijas.
        :param file: Archivo abierto para lectura.
        :param kwargs: Argumentos adicionales necesarios para el formateo.
        :return: Resultado del formateo.
        """
        raise NotImplementedError("Este método debe ser implementado en la clase hija.")
