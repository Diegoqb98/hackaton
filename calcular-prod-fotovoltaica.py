import json
import pandas as pd
import pvlib
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

# Cargar la configuración desde el archivo JSON
with open('config_completo.json', 'r') as file:
    config = json.load(file)

# Obtener los parámetros de la batería, panel, inversor, y la ubicación geográfica
panel_params = config["modulo"]
inversor_params = config["inversor"]
bateria_params = config["bateria"]
ubicacion_params = config["ubicacion"]
sistemaPV_params = config["sistemaPV"]
coste_desvio = config["hora_coef_apuntamiento"]

# Extraer parámetros de ubicación
latitude = ubicacion_params["latitud"]
longitude = ubicacion_params["longitud"]
altitude = ubicacion_params["altitud"]

# Usar la zona horaria como un string válido (por ejemplo, "Europe/Madrid" para UTC+1)
timezone = "Europe/Madrid"

# Crear la ubicación con la zona horaria correctamente definida
location = Location(latitude, longitude, timezone, altitude)

# Cambiar el rango de fechas al 16 de noviembre de 2024
times = pd.date_range('2024-11-16', '2024-11-17', freq='1H', tz=timezone)

# Obtener datos de cielo despejado (modelo claro)
clear_sky = location.get_clearsky(times)

# Configuración del sistema fotovoltaico usando los parámetros del JSON
system = PVSystem(
    surface_tilt=sistemaPV_params["inclinacion"],  # Inclinación del panel
    surface_azimuth=sistemaPV_params["azimut"],  # Orientación hacia el sur
    module_parameters={
        'pdc0': panel_params["PNom"],  # Potencia nominal del panel (W)
        'gamma_pdc': panel_params["Gamma"],  # Coeficiente de temperatura de potencia
        'Isc': panel_params["Isc"],  # Corriente de cortocircuito
        'Voc': panel_params["Voc"],  # Voltaje en circuito abierto
        'Imp': panel_params["Imp"],  # Corriente de punto máximo
        'Vmp': panel_params["Vmp"],  # Voltaje en punto máximo
    },
    inverter_parameters={
        'pdc0': inversor_params["PNomConv"],  # Potencia nominal del inversor (W)
        'VdcMax': inversor_params["VAbsMax"],  # Voltaje máximo de corriente continua
        'VdcMin': inversor_params["VMppMin"],  # Voltaje mínimo de corriente continua
        'VdcNom': inversor_params["VmppNom"],  # Voltaje nominal de corriente continua
        'PMaxAC': inversor_params["PMaxOUT"],  # Potencia máxima de salida del inversor (W)
    },
    temperature_model_parameters=TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']
)

# Crear el modelo de cadena (ModelChain), especificando el modelo de AOI y el modelo espectral
model_chain = ModelChain(system, location, aoi_model='physical', spectral_model='no_loss')

# Crear un dataframe con condiciones meteorológicas simuladas
weather = pd.DataFrame({
    'ghi': clear_sky['ghi'],  # Irradiancia horizontal global
    'dni': clear_sky['dni'],  # Irradiancia normal directa
    'dhi': clear_sky['dhi'],  # Irradiancia horizontal difusa
    'temp_air': pd.Series(20, index=times),  # Temperatura del aire (20°C por defecto)
    'wind_speed': pd.Series(2, index=times)  # Velocidad del viento (2 m/s por defecto)
})

# Ejecutar el modelo de simulación de producción fotovoltaica
model_chain.run_model(weather)

# Obtener la producción en AC (corriente alterna) desde el diccionario 'results'
ac_power = model_chain.results['ac']  # Producción AC del sistema fotovoltaico

# **Simulación del inversor**: Ajuste de la producción según las limitaciones del inversor
ac_power = ac_power.clip(upper=inversor_params["PMaxOUT"])

# Cálculo del coste de desvío en cada hora
costes_por_hora = []
for hour, power in enumerate(ac_power, start=1):
    # Obtener el coste de desvío de acuerdo con la hora
    coste_hora = coste_desvio[str(hour)] * power  # €/KWh * KWh producidos
    costes_por_hora.append(coste_hora)

# Mostrar la producción horaria y los costes
print("Producción horaria estimada (kW):")
print(ac_power)

print("\nCoste de desvío (€/hora):")
print(costes_por_hora)

# Producción total diaria del sistema fotovoltaico en AC
total_daily_production = ac_power.sum() / 1000  # Suma de la producción horaria en kWh
print(f"\nProducción total estimada para el día (kWh): {total_daily_production:.2f}")

# Cálculo del coste total de desvío para el día
total_coste_desvio = sum(costes_por_hora)
print(f"\nCoste total de desvío (€/día): {total_coste_desvio:.2f}")
