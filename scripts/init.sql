-- Tabla para almacenar la producción de energía por hora
CREATE TABLE produccion_energia (
    id SERIAL PRIMARY KEY,
    hora TIME NOT NULL,
    energia_producida_kwh NUMERIC(10, 3) NOT NULL
);

-- Tabla para almacenar los precios marginales de la península por hora
CREATE TABLE precios_peninsula (
    id SERIAL PRIMARY KEY,
    hora TIME NOT NULL,
    precio_eur_kwh NUMERIC(10, 6) NOT NULL
);

-- Tabla para almacenar los precios estimados de Baleares por hora
CREATE TABLE precios_baleares (
    id SERIAL PRIMARY KEY,
    hora TIME NOT NULL,
    precio_eur_kwh NUMERIC(10, 6) NOT NULL
);

-- Tabla para almacenar los beneficios calculados
CREATE TABLE beneficios (
    id SERIAL PRIMARY KEY,
    hora TIME NOT NULL,
    beneficio_peninsula_eur NUMERIC(15, 2) NOT NULL,
    beneficio_baleares_eur NUMERIC(15, 2) NOT NULL
);

-- Tabla para almacenar información agregada del precio medio diario
CREATE TABLE precio_medio_diario (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    precio_medio_peninsula NUMERIC(10, 6) NOT NULL,
    precio_medio_baleares NUMERIC(10, 6) NOT NULL
);
