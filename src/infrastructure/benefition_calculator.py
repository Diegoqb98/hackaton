import numpy as np
import src.infrastructure.opi.opti_watt as ow

class BeneficioEstimation:
    """
    Clase para calcular el beneficio estimado basado en la producción de energía
    y los precios de la energía en la península y Baleares.
    """

    def __init__(self, produccion_energia, precio_peninsula, precio_baleares, config):
        """
        Inicializa la clase con los parámetros necesarios.
        
        :param produccion_energia: Array de producción de energía en kWh.
        :param precio_peninsula: Precio de la energía en la península (€/kWh).
        :param precio_baleares: Precio de la energía en Baleares (€/kWh).
        """
        self.produccion_energia = np.array(produccion_energia, dtype=np.float64)
        self.precio_peninsula = np.array(precio_peninsula, dtype=np.float64)
        self.precio_baleares = np.array(precio_baleares, dtype=np.float64)
        self.config = config

    # def calcular_beneficio(self):
    #     """
    #     Calcula el beneficio estimado total para la producción de energía en la península
    #     y Baleares.
        
    #     :return: Un diccionario con el beneficio en península y en Baleares.
    #     """
    #     # Beneficio para la península: multiplicamos cada valor de producción por el precio península
    #     beneficio_peninsula = sum([kwh * self.precio_peninsula for kwh in self.produccion_energia])
        
    #     # Beneficio para Baleares: multiplicamos cada valor de producción por el precio Baleares
    #     beneficio_baleares = sum([kwh * self.precio_baleares for kwh in self.produccion_energia])

    #     # Retornar los beneficios en un diccionario
    #     return {
    #         "beneficio_peninsula": beneficio_peninsula,
    #         "beneficio_baleares": beneficio_baleares
    #     }

    
    def calcular_beneficio(self):
        
        s_max= self.config.get_bateria().get('capacidad_maxima')
        b_max= self.config.get_bateria().get('energia_maxima_carga_descarga_por_hora')
        v_max= self.config.get_bateria().get('maxima_venta_a_red')
        s_init= self.config.get_bateria().get('soc_inicial') * s_max

        print("s_max: ", s_max)
        print("b_max: ", b_max)
        print("v_max: ", v_max)
        print("s_init: ", s_init)
        
        # print("precio: ", ow.maximize_cost(self.precio_peninsula, self.produccion_energia, False, s_max, b_max, v_max, s_init))


