import json
import numpy as np

# Cargar la configuración desde el archivo JSON
with open('config_completo.json', 'r') as file:
    config = json.load(file)

# Obtener el coeficiente de apuntamiento horario desde la configuración
coef_apuntamiento = config["hora_coef_apuntamiento"]

# Recibir el array de precios marginales para 24 horas (ejemplo de precios marginales de la península)
precios_marginales = [
    30.5,  # Precio para la hora 1 (€/MWh)
    32.0,  # Precio para la hora 2 (€/MWh)
    31.8,  # Precio para la hora 3 (€/MWh)
    33.0,  # Precio para la hora 4 (€/MWh)
    34.5,  # Precio para la hora 5 (€/MWh)
    35.0,  # Precio para la hora 6 (€/MWh)
    34.8,  # Precio para la hora 7 (€/MWh)
    36.0,  # Precio para la hora 8 (€/MWh)
    37.0,  # Precio para la hora 9 (€/MWh)
    38.5,  # Precio para la hora 10 (€/MWh)
    40.0,  # Precio para la hora 11 (€/MWh)
    41.0,  # Precio para la hora 12 (€/MWh)
    39.5,  # Precio para la hora 13 (€/MWh)
    38.0,  # Precio para la hora 14 (€/MWh)
    37.5,  # Precio para la hora 15 (€/MWh)
    36.5,  # Precio para la hora 16 (€/MWh)
    35.5,  # Precio para la hora 17 (€/MWh)
    34.0,  # Precio para la hora 18 (€/MWh)
    33.0,  # Precio para la hora 19 (€/MWh)
    32.5,  # Precio para la hora 20 (€/MWh)
    31.0,  # Precio para la hora 21 (€/MWh)
    30.0,  # Precio para la hora 22 (€/MWh)
    29.5,  # Precio para la hora 23 (€/MWh)
    28.0   # Precio para la hora 24 (€/MWh)
]

# Arrays para almacenar los precios por hora de la península y de Baleares
precios_peninsula = [precio / 1000 for precio in precios_marginales]  # Convertir de €/MWh a €/kWh
precios_baleares = []

# Calcular los precios estimados para Baleares para cada hora aplicando el coeficiente de apuntamiento
for hora in range(1, 25):
    # Calcular el precio ajustado de Baleares multiplicando el precio de la península por el coeficiente de apuntamiento
    precio_baleares_hora = precios_marginales[hora - 1] * coef_apuntamiento[str(hora)] / 1000  # Convertir a €/kWh
    precios_baleares.append(precio_baleares_hora)

# Mostrar los resultados
print("Precios marginales de la península por hora (€/kWh):")
print(precios_peninsula)

print("\nPrecios estimados para Baleares por hora (€/kWh):")
print(precios_baleares)
