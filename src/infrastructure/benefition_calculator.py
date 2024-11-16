import numpy as np

class BeneficioEstimation:
    """
    Clase para calcular el beneficio estimado basado en la producción de energía
    y los precios de la energía en la península y Baleares.
    """

    def __init__(self, produccion_energia, precio_peninsula, precio_baleares):
        """
        Inicializa la clase con los parámetros necesarios.
        
        :param produccion_energia: Array de producción de energía en kWh.
        :param precio_peninsula: Precio de la energía en la península (€/kWh).
        :param precio_baleares: Precio de la energía en Baleares (€/kWh).
        """
        self.produccion_energia = np.array(produccion_energia, dtype=np.float64)
        self.precio_peninsula = np.array(precio_peninsula, dtype=np.float64)
        self.precio_baleares = np.array(precio_baleares, dtype=np.float64)

    def calcular_beneficio(self):
        """
        Calcula el beneficio estimado total para la producción de energía en la península
        y Baleares.
        
        :return: Un diccionario con el beneficio en península y en Baleares.
        """
        # Beneficio para la península: multiplicamos cada valor de producción por el precio península
        beneficio_peninsula = sum([kwh * self.precio_peninsula for kwh in self.produccion_energia])
        
        # Beneficio para Baleares: multiplicamos cada valor de producción por el precio Baleares
        beneficio_baleares = sum([kwh * self.precio_baleares for kwh in self.produccion_energia])

        # Retornar los beneficios en un diccionario
        return {
            "beneficio_peninsula": beneficio_peninsula,
            "beneficio_baleares": beneficio_baleares
        }
