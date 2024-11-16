from src.infrastructure.execute import MainExecutor


if __name__ == "__main__":
    # Parámetros
    input_file = "./files/precio_marginal.txt"
    output_file = "./files/output.csv"
    energy_file = "./files/energy.txt"
    config_file = 'configuracion.json'
    base_url = 'https://www.omie.es/sites/default/files/dados'
    download_folder = 'C:/Users/didac/hackaton/files'
    date_str = '2024-11-16'

    # Crear instancia del ejecutor y ejecutar el flujo
    executor = MainExecutor(input_file, output_file, config_file, base_url, download_folder, date_str)
    executor.run('precio_marginal')
