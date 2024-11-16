import os
from src.infrastructure.execute import MainExecutor

if __name__ == "__main__":
    input_file = os.getenv('input_file', './files/precio_marginal.txt')
    output_file = os.getenv('output_file', './files/output.csv')
    energy_file = os.getenv('energy_file', './files/energy.txt')
    config_file = os.getenv('config_file', 'configuracion.json')
    # base_url = os.getenv('base_url', 'https://www.omie.es/sites/default/files/dados')
    base_url = os.getenv('base_url', 'https://www.omie.es/')
    download_folder = os.getenv('download_folder', '/app/files') 
    date_str = os.getenv('date_str', '2024-11-16')
    api_type = os.getenv('api_type', 'precio_marginal_i')

    # Crear instancia del ejecutor y ejecutar el flujo
    executor = MainExecutor(input_file, output_file, config_file, base_url, download_folder, date_str,api_type)
    executor.run(api_type)
