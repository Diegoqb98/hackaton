python -m venv venv


.\venv\Scripts\activate

pip install requests
pip install pvlib


pip install requests python-dotenv pandas


pip freeze > requirements.txt

docker compose up -d --build   


env example

# .env example
input_file=./files/precio_marginal.txt
output_file=./files/output.csv
energy_file=./files/energy.txt
config_file=configuracion.json
base_url=https://www.omie.es/sites/default/files/dados
download_folder=/app/files
date_str=2024-11-16
api_type=precio_marginal

si se quiere nueva api

implementar nuevo formatter y agregar linea a formatters