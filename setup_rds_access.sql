-- Script para configurar acceso a RDS y crear tablas
-- Este script debe ejecutarse directamente en la base de datos RDS

-- Permitir conexiones desde cualquier dirección IP (para desarrollo)
-- En producción, deberías restringir esto a las IPs específicas de tus servidores
CREATE OR REPLACE FUNCTION public.allow_all_connections()
RETURNS void AS $$
BEGIN
    -- Modificar pg_hba.conf para permitir conexiones desde cualquier IP
    -- Esto es equivalente a añadir una línea "host all all 0.0.0.0/0 md5" en pg_hba.conf
    PERFORM pg_reload_conf();
END;
$$ LANGUAGE plpgsql;

-- Crear la extensión UUID si no existe
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear la tabla de usuarios si no existe
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON public.users(username);

-- Verificar que la tabla se ha creado correctamente
DO $$
BEGIN
    RAISE NOTICE 'Tabla users creada o ya existente';
    
    -- Mostrar las columnas de la tabla users
    FOR r IN (SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users')
    LOOP
        RAISE NOTICE 'Columna: % (%)', r.column_name, r.data_type;
    END LOOP;
END $$;

-- Otorgar permisos al usuario postgres sobre todas las tablas
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;

-- Crear un usuario específico para la aplicación si es necesario
-- CREATE USER app_user WITH PASSWORD 'app_password';
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;
-- GRANT ALL PRIVILEGES ON SCHEMA public TO app_user;
