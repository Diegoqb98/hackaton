import json
import numpy as np
import pvlib
import pandas as pd
from datetime import datetime

from src.infrastructure.config.config import Configuracion


class EnergyProductionCalculator:
    """
    Clase para calcular la energía producida por un sistema fotovoltaico en base a la configuración proporcionada.
    """

    def __init__(self, config, eficiencia_sistema=0.85):
        """
        Inicializa la clase con los parámetros de configuración y otros valores relevantes.
        :param config: Instancia de la clase Configuracion que contiene los parámetros de configuración.
        :param eficiencia_sistema: Eficiencia general del sistema (por defecto 85%).
        :param num_paneles: Número de paneles fotovoltaicos en el sistema (por defecto 6000).
        """
        self.config = config
        self.eficiencia_sistema = eficiencia_sistema
        self.num_paneles = self.config.get_modulo().get('NumTotal')
        
        # Extraer los parámetros de configuración
        self.Isc = self.config.get_modulo().get('Isc')
        self.Voc = self.config.get_modulo().get('Voc')
        self.Imp = self.config.get_modulo().get('Imp')
        self.Vmp = self.config.get_modulo().get('Vmp')
        self.BifacialityFactor = self.config.get_modulo().get('BifacialityFactor')
        self.GRef = self.config.get_modulo().get('GRef')
        self.P_nom = self.config.get_modulo().get('PNom')
        
        # Ubicación
        self.latitud = self.config.get_ubicacion().get('latitud')
        self.longitud = self.config.get_ubicacion().get('longitud')
        self.altitud = self.config.get_ubicacion().get('altitud')

        # Crear objeto de ubicación usando pvlib
        self.location = pvlib.location.Location(self.latitud, self.longitud, altitude=self.altitud)

    def calculate_energy(self, date):
        """
        Calcula la energía producida por el sistema fotovoltaico para una fecha dada.
        :param date: Fecha para la cual se calculará la producción de energía.
        :return: Listado de energía producida por hora en kWh.
        """
        # Generar un rango de horas del día en la zona horaria de España (Europe/Madrid)
        times = pd.date_range(datetime.strptime(date, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0), 
                              periods=24, freq='h', tz='Europe/Madrid')

        # Obtener la posición solar
        solar_position = self.location.get_solarposition(times)

        # Calcular la irradiancia global utilizando el modelo de cielo claro
        cs = self.location.get_clearsky(times)
        dni = cs['dni']
        ghi = cs['ghi']
        dhi = cs['dhi']

        # Calcular la potencia producida por el panel
        irradiance_at_panel = ghi  # Usamos la irradiancia global como la que llega al panel
        P_panel = self.P_nom * (irradiance_at_panel / self.GRef) * self.BifacialityFactor

        # Aplicar la eficiencia del sistema
        P_panel_adjusted = P_panel * self.eficiencia_sistema

        # Convertir la potencia de W a kWh y multiplicar por el número de paneles
        energy_produced_kWh = (P_panel_adjusted / 1000) * self.num_paneles  # Dividido por 1000 para convertir a kWh

        # Guardamos la energía producida por hora en una lista
        energy_list = []
        for i, hora in enumerate(times):
            energy_list.append(energy_produced_kWh.iloc[i])
            
            print(f"Hora {hora.strftime('%H:%M')} - Energía producida: {energy_produced_kWh.iloc[i]:.3f} kWh")

        return [float(num) for num in energy_list]



# Ejemplo de uso
if __name__ == "__main__":
    # Ruta al archivo de configuración JSON
    config_file = 'configuracion.json'
    
    # Crear la instancia de la clase Configuracion
    config = Configuracion(config_file)
    
    # Crear la instancia de la clase EnergyProductionCalculator
    calculator = EnergyProductionCalculator(config)
    
    # Calcular la energía para una fecha específica (por ejemplo, 2024-11-16)
    date = '2024-11-16'
    energy_list = calculator.calculate_energy(date)
    
    # Imprimir los resultados (lista de energía producida por hora)
    print("\n, ".join(map(str, energy_list)))
