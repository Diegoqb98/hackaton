import psycopg2
from psycopg2.extras import execute_batch

class DatabaseConnector:
    def __init__(self, db_name, user, password, host='localhost', port=5432):
        """
        Inicializa la conexión con la base de datos.

        :param db_name: Nombre de la base de datos.
        :param user: Usuario de la base de datos.
        :param password: Contraseña del usuario.
        :param host: Dirección del servidor (por defecto localhost).
        :param port: Puerto del servidor (por defecto 5432).
        """
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def insert_produccion_energia(self, data):
        """
        Inserta datos en la tabla 'produccion_energia'.

        :param data: Array de valores de energía producida en kWh.
        """
        # Crear una lista de tuplas a partir de los datos (se necesita para execute_batch)
        data_tuples = [(valor,) for valor in data]
        
        # Query de inserción
        query = """
        INSERT INTO produccion_energia (energia_producida_kwh)
        VALUES (%s)
        """
        
        # Ejecuta el batch de inserciones
        execute_batch(self.cursor, query, data_tuples)
        
        # Realiza el commit para guardar los cambios en la base de datos
        self.connection.commit()

    def insert_precios_peninsula(self, data):
        """
        Inserta datos en la tabla 'precios_peninsula'.

        :param data: Lista de tuplas (hora, precio_eur_kwh).
        """
        query = """
        INSERT INTO precios_peninsula (hora, precio_eur_kwh)
        VALUES (%s, %s)
        """
        execute_batch(self.cursor, query, data)
        self.connection.commit()

    def insert_precios_baleares(self, data):
        """
        Inserta datos en la tabla 'precios_baleares'.

        :param data: Lista de tuplas (hora, precio_eur_kwh).
        """
        query = """
        INSERT INTO precios_baleares (hora, precio_eur_kwh)
        VALUES (%s, %s)
        """
        execute_batch(self.cursor, query, data)
        self.connection.commit()

    def insert_beneficios(self, data):
        """
        Inserta datos en la tabla 'beneficios'.

        :param data: Lista de tuplas (hora, beneficio_peninsula_eur, beneficio_baleares_eur).
        """
        query = """
        INSERT INTO beneficios (hora, beneficio_peninsula_eur, beneficio_baleares_eur)
        VALUES (%s, %s, %s)
        """
        execute_batch(self.cursor, query, data)
        self.connection.commit()

    def insert_precio_medio_diario(self, fecha, precio_medio_peninsula, precio_medio_baleares):
        """
        Inserta un precio medio diario en la tabla 'precio_medio_diario'.

        :param fecha: Fecha del precio medio.
        :param precio_medio_peninsula: Precio medio de la península en €/kWh.
        :param precio_medio_baleares: Precio medio de Baleares en €/kWh.
        """
        query = """
        INSERT INTO precio_medio_diario (fecha, precio_medio_peninsula, precio_medio_baleares)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (fecha, precio_medio_peninsula, precio_medio_baleares))
        self.connection.commit()

    def close_connection(self):
        """
        Cierra la conexión con la base de datos.
        """
        self.cursor.close()
        self.connection.close()
