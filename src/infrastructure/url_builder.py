class URLBuilder:
    """
    Clase estática para construir la URL dinámica basada en la fecha proporcionada.
    """

    @staticmethod
    def build_url_v1(year, month, day, base_url):
        """
        Construye la URL en el formato:
        'https://www.omie.es/sites/default/files/dados/AGNO_YYYY/MES_MM/TXT/INT_PBC_EV_H_1_DD_MM_YYYY_DD_MM_YYYY.TXT'
        """
        return f"{base_url}/AGNO_{year}/MES_{month:02d}/TXT/INT_PBC_EV_H_1_{day:02d}_{month:02d}_{year}_{day:02d}_{month:02d}_{year}.TXT"

    @staticmethod
    def build_url_v2(year, month, day, base_url):
        """
        Construye la URL en el formato:
        'https://www.omie.es/es/file-download?parents%5B0%5D=marginalpdbc&filename=marginalpdbc_YYYYMMDD.1'
        """
        return f"{base_url}/es/file-download?parents%5B0%5D=marginalpdbc&filename=marginalpdbc_{year}{month:02d}{day:02d}.1"
