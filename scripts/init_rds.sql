-- Script para inicializar la base de datos en RDS
-- Ejecutar como usuario con privilegios para crear tablas

-- Crear extensión para UUID si no existe
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR NOT NULL UNIQUE,
    username VARCHAR UNIQUE,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para búsquedas comunes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Comentarios para documentación
COMMENT ON TABLE users IS 'Tabla de usuarios para autenticación y autorización';
COMMENT ON COLUMN users.id IS 'Identificador único UUID';
COMMENT ON COLUMN users.email IS 'Email del usuario (único)';
COMMENT ON COLUMN users.username IS 'Nombre de usuario opcional (único)';
COMMENT ON COLUMN users.hashed_password IS 'Contraseña encriptada con bcrypt';
COMMENT ON COLUMN users.is_active IS 'Indica si el usuario está activo';
COMMENT ON COLUMN users.is_superuser IS 'Indica si el usuario tiene privilegios de administrador';

-- Crear usuario de aplicación con permisos limitados
-- IMPORTANTE: Reemplazar 'secure_password' con una contraseña segura
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'auth_app_user') THEN
        CREATE USER auth_app_user WITH PASSWORD 'secure_password';
    END IF;
END
$$;

-- Otorgar permisos al usuario de la aplicación
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO auth_app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO auth_app_user;
