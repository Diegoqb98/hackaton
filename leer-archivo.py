# Nombre del archivo a leer
file_name = "marginal.1"

# Inicializar lista para almacenar los precios
precios = []

try:
    # Abrir y leer el archivo
    with open(file_name, 'r') as file:
        for line in file:
            # Ignorar líneas que no contienen datos útiles
            if line.startswith("*") or line.strip() == "" or "MARGINALPDBC" in line:
                continue
            
            # Dividir la línea en partes separadas por ';'
            partes = line.strip().split(';')
            
            # El último valor de interés está antes del último separador ';'
            precio = float(partes[-2])  # Segundo valor desde el final
            precios.append(precio)
    
    # Imprimir los precios extraídos
    print("Precios extraídos:", precios)

except FileNotFoundError:
    print(f"El archivo '{file_name}' no se encuentra.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
