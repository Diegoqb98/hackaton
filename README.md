Overview
This project is designed to fetch and process energy data, specifically related to the "precio marginal" (marginal price) from the OMIE (Operador del Mercado Ibérico de Energía) website. It provides an API and utilities for fetching, parsing, and saving the energy data into structured files.

The project can be run in a Python virtual environment with Docker support for easy deployment.

Getting Started
1. Setting Up a Python Virtual Environment
First, create a virtual environment to manage dependencies:

bash
python -m venv venv
Activate the virtual environment:

On Windows:
bash
.\venv\Scripts\activate

2. Install Python Dependencies
With the virtual environment activated, install the necessary dependencies using pip:

bash
Copiar código
pip install requests pvlib python-dotenv pandas
This will install the libraries needed to interact with APIs, handle environmental variables, and work with data files.

3. Generate the requirements.txt File
After installing the dependencies, generate the requirements.txt file for the project:

bash
pip freeze > requirements.txt
This will save the list of installed Python packages into the requirements.txt file, which is necessary for Docker and sharing the environment.

Running the Application
4. Docker Setup
To run the application using Docker, use the following commands to build the Docker image and start the services in the background:

bash
docker compose up -d --build
This will:

Build the Docker image based on the Dockerfile.
Start the application and PostgreSQL service in detached mode.
You can check the status of the containers by running:

bash
docker ps
Configuration
5. Environment Variables
The project uses a .env file for configuration. Below is an example of how to set up the .env file:

.env example:
bash
# File Paths
input_file=./files/precio_marginal.txt
output_file=./files/output.csv
energy_file=./files/energy.txt
config_file=configuracion.json

# OMIE API Configuration
base_url=https://www.omie.es/sites/default/files/dados
download_folder=/app/files
date_str=2024-11-16
api_type=precio_marginal_i / precio_marginal_txt
Ensure that the directories referenced in the .env file (such as ./files) exist and are accessible by the application.

6. API Integration
If you wish to integrate a new API, follow these steps:

Implement a New Formatter: Create a new formatter class or function for the new API data. The formatter should handle parsing and extracting the necessary information from the API response.

Add the Formatter to the Formatters List: You will need to update the code where the formatters are listed, adding a reference to your newly implemented formatter.

Folder Structure
bash
Copiar código
/
├── Dockerfile                # Docker configuration file
├── docker-compose.yml        # Docker Compose configuration
├── .env                      # Environment configuration file
├── requirements.txt          # Python dependencies file
├── configuracion.json        # Configuration file for the application
├── files/                    # Folder to store input and output files
├── main.py                   # Entry point for the application
└── formatters/                # Directory for API formatters
└── formatter.py          # Example formatter file
Troubleshooting
1. Network Issues in Docker
If you encounter network issues while building or running Docker (e.g., unable to fetch packages), make sure Docker has internet access. You can test this by running:

bash
Copiar código
docker run -it --rm python:3.12-slim ping deb.debian.org
If the issue persists, consider using a different mirror in the Dockerfile or checking your local network configuration.

2. PostgreSQL Client Installation
If you're facing issues related to the psycopg2 library installation in Docker (e.g., missing pg_config), consider switching to psycopg2-binary or installing libpq-dev and postgresql-client dependencies in the Dockerfile.

Contributing
If you'd like to contribute to the project, feel free to fork it, create a branch, and submit a pull request. Make sure to test your changes and follow the project's coding conventions.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Additional Notes
To use a new API, implement a corresponding formatter and add it to the formatters list.
The project assumes that the input and output files are stored under the files/ directory, as configured in the .env file.