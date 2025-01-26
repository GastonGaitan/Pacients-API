-- Eliminar las tablas si ya existen
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS pacients;

-- Crear la tabla "users"
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Crear la tabla "pacients"
CREATE TABLE pacients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(255),
    document_picture_source VARCHAR(255),
    email_verification_sent BOOLEAN DEFAULT FALSE,
    sms_verification_sent BOOLEAN DEFAULT FALSE
);
