-- Tabla para almacenar la producción de energía por hora
CREATE TABLE produccion_energia (
    id SERIAL PRIMARY KEY,
    energia_producida_kwh NUMERIC(10, 3) NOT NULL
);

-- Tabla para almacenar los precios marginales de la península por hora
CREATE TABLE precios_peninsula (
    id SERIAL PRIMARY KEY,
    precio_eur_kwh NUMERIC(10, 6) NOT NULL
);

-- Tabla para almacenar los precios estimados de Baleares por hora
CREATE TABLE precios_baleares (
    id SERIAL PRIMARY KEY,
    precio_eur_kwh NUMERIC(10, 6) NOT NULL
);