import csv

class PrecioMarginalIFormatter:
    """
    Formateador para extraer precios marginales del archivo y escribirlos en un archivo CSV de una sola línea.
    """
    @staticmethod
    def format(file, output_csv, **kwargs):
        precios = []
        
        # Iterar sobre las líneas del archivo
        for line in file:
            # Saltar las líneas con comentarios, vacías o que contienen información irrelevante
            if line.startswith("*") or line.strip() == "" or "MARGINALPDBC" in line:
                continue
            
            # Separar la línea por el delimitador ";"
            partes = line.strip().split(';')
            
            # Verificamos si la línea tiene la estructura correcta (fecha y precios)
            if len(partes) >= 3:
                # Extraer el precio de cada línea después de la fecha
                try:
                    # Extraemos las dos últimas columnas de la línea (precio)
                    precio = float(partes[4].strip().replace(',', '.'))
                    precios.append(precio)
                except ValueError:
                    continue
        
        # Escribir los precios en un archivo CSV
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Escribir los precios como una sola línea en el archivo CSV
            writer.writerow(precios)
        
        print(f"\nLos precios se han guardado correctamente en {output_csv}.\n")
