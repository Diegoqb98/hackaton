import json

class Configuracion:
    def __init__(self, archivo_configuracion):
        """
        Inicializa la clase cargando el archivo JSON de configuración.
        :param archivo_configuracion: Ruta al archivo JSON.
        """
        try:
            with open(archivo_configuracion, 'r') as file:
                self.config = json.load(file)
        except Exception as e:
            print(f"\nError al cargar el archivo de configuración: {e}")
            self.config = {}

    # Métodos get para acceder a las propiedades del JSON

    def get_hora_coef_apuntamiento(self):
        """Devuelve el coeficiente de apuntamiento por hora."""
        return self.config.get("hora_coef_apuntamiento", {})

    def get_modulo(self):
        """Devuelve los parámetros del módulo fotovoltaico."""
        return self.config.get("modulo", {})

    def get_inversor(self):
        """Devuelve los parámetros del inversor."""
        return self.config.get("inversor", {})

    def get_bateria(self):
        """Devuelve los parámetros de la batería."""
        return self.config.get("bateria", {})

    def get_ubicacion(self):
        """Devuelve la información de la ubicación."""
        return self.config.get("ubicacion", {})

    def get_sistema_pv(self):
        """Devuelve los parámetros del sistema fotovoltaico."""
        return self.config.get("sistemaPV", {})

    # Métodos get específicos para propiedades dentro de cada sección (si se necesita)

    # Parámetros del módulo fotovoltaico
    def get_modulo_width(self):
        return self.config.get("modulo", {}).get("Width", None)

    def get_modulo_height(self):
        return self.config.get("modulo", {}).get("Height", None)

    def get_modulo_pnom(self):
        return self.config.get("modulo", {}).get("PNom", None)

    # Parámetros de la batería
    def get_bateria_capacidad_maxima(self):
        return self.config.get("bateria", {}).get("capacidad_maxima", None)

    def get_bateria_soc_inicial(self):
        return self.config.get("bateria", {}).get("soc_inicial", None)

    # Parámetros de la ubicación
    def get_ubicacion_latitud(self):
        return self.config.get("ubicacion", {}).get("latitud", None)

    def get_ubicacion_longitud(self):
        return self.config.get("ubicacion", {}).get("longitud", None)

    # Y así sucesivamente para todas las propiedades que quieras

# Ejemplo de uso
if __name__ == "__main__":
    # Ruta al archivo JSON de configuración
    archivo_configuracion = 'configuracion.json'

    # Crear instancia de la clase Configuracion
    config = Configuracion(archivo_configuracion)

    # Obtener valores utilizando los métodos get
    print("Coeficiente de apuntamiento para la hora 1:", config.get_hora_coef_apuntamiento().get("1"))
    print("Dimensiones del módulo fotovoltaico:")
    print("Ancho:", config.get_modulo_width())
    print("Alto:", config.get_modulo_height())
    print("PNom del módulo:", config.get_modulo_pnom())

    print("Capacidad máxima de la batería:", config.get_bateria_capacidad_maxima())
    print("Latitud de la ubicación:", config.get_ubicacion_latitud())
