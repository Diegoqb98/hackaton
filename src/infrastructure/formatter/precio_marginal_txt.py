import csv

class PrecioMarginalTxTFormatter:
    """
    Formateador para extraer precios marginales del archivo y escribirlos en un archivo CSV.
    """
    @staticmethod
    def format(file, output_csv, **kwargs):
        precios = []
        
        # Iterar sobre las líneas del archivo
        for line in file:
            # Saltar las líneas con comentarios, vacías o que contienen información irrelevante
            if line.startswith("*") or line.strip() == "" or "Precio marginal" not in line:
                continue
            
            # Encontramos la línea que contiene los precios de las 24 horas
            partes = line.strip().split(';')
            
            # El precio marginal está en las últimas 24 posiciones
            precios_str = partes[1:]  # Las primeras son etiquetas, los precios están a partir de la posición 1
            
            for precio_str in precios_str:
                try:
                    # Limpiar los espacios y la coma, luego convertir a float
                    precio_str = precio_str.strip().replace(',', '.')
                    precio = float(precio_str)
                    precios.append(precio)
                except ValueError:
                    continue

        # Escribir los precios en un archivo CSV
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Escribir los precios
            writer.writerow(precios)
        
        print(f"\nLos precios se han guardado correctamente en {output_csv}.\n")
