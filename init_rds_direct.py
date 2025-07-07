#!/usr/bin/env python3
"""
Script para inicializar directamente la base de datos RDS desde la instancia EC2.
Este script se conecta directamente a la base de datos RDS y ejecuta el script SQL
para crear las tablas necesarias.
"""

import os
import sys
import time
import socket
import logging
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("RDS-Initializer")

# Configuración de la base de datos RDS
DB_HOST = os.getenv("DB_HOST", "auth-db.cyllotifqg8b.us-east-1.rds.amazonaws.com")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "users_db")
DB_USER = os.getenv("DB_USER", "postgres")
# Usar la contraseña correcta según la documentación
DB_PASSWORD = os.getenv("DB_PASSWORD", "Uzumymw260916_")

# Ruta al archivo SQL
SQL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "init_db.sql")

# Obtener la dirección IP local para diagnóstico
def get_local_ip():
    try:
        # Crear un socket para determinar qué IP se usaría para conectar al host externo
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Error obteniendo IP local: {str(e)}"

def main():
    local_ip = get_local_ip()
    logger.info(f"Inicializando base de datos RDS desde {local_ip}")
    logger.info(f"Intentando conectar a {DB_HOST}:{DB_PORT} con usuario {DB_USER}")
    logger.info(f"Nombre de la base de datos: {DB_NAME}")
    
    # Verificar si el host es alcanzable
    try:
        logger.info(f"Verificando conectividad con {DB_HOST}:{DB_PORT}...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex((DB_HOST, int(DB_PORT)))
        if result == 0:
            logger.info(f"Puerto {DB_PORT} en {DB_HOST} está abierto y accesible")
        else:
            logger.warning(f"ADVERTENCIA: Puerto {DB_PORT} en {DB_HOST} NO es accesible (código {result})")
            logger.warning("Esto puede indicar un problema de grupo de seguridad en AWS")
        s.close()
    except Exception as e:
        logger.error(f"Error verificando conectividad: {e}")
    
    # Intentar conectar a la base de datos
    try:
        logger.info("Intentando establecer conexión a PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
            connect_timeout=10
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        logger.info("✅ Conexión exitosa a la base de datos RDS")
        
        # Obtener información de la versión de PostgreSQL
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            logger.info(f"Versión de PostgreSQL: {version}")
    except Exception as e:
        logger.error(f"❌ Error al conectar a la base de datos RDS: {e}")
        logger.error("\nPosibles causas:")
        logger.error("1. La contraseña es incorrecta")
        logger.error("2. El grupo de seguridad de RDS no permite conexiones desde esta IP")
        logger.error("3. La instancia RDS no está en ejecución")
        logger.error("4. La configuración pg_hba.conf no permite conexiones desde esta IP")
        sys.exit(1)
    
    # Leer el archivo SQL
    try:
        with open(SQL_FILE, 'r') as f:
            sql_script = f.read()
        logger.info(f"Archivo SQL leído correctamente: {SQL_FILE}")
    except Exception as e:
        logger.error(f"Error al leer el archivo SQL: {e}")
        conn.close()
        sys.exit(1)
    
    # Ejecutar el script SQL
    try:
        logger.info("Ejecutando script SQL...")
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
        logger.info("✅ Script SQL ejecutado correctamente")
    except Exception as e:
        logger.error(f"❌ Error al ejecutar el script SQL: {e}")
        conn.close()
        sys.exit(1)
    
    # Verificar que la tabla users existe
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'users'
                );
            """)
            table_exists = cursor.fetchone()[0]
            if table_exists:
                logger.info("✅ La tabla 'users' existe en la base de datos")
                
                # Contar registros en la tabla users
                cursor.execute("SELECT COUNT(*) FROM users;")
                count = cursor.fetchone()[0]
                logger.info(f"Número de registros en la tabla users: {count}")
                
                # Mostrar estructura de la tabla
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'users';
                """)
                columns = cursor.fetchall()
                logger.info("Estructura de la tabla users:")
                for column in columns:
                    logger.info(f"  - {column[0]}: {column[1]}")
            else:
                logger.warning("⚠️ ¡ADVERTENCIA! La tabla 'users' NO existe en la base de datos")
    except Exception as e:
        logger.error(f"Error al verificar la existencia de la tabla: {e}")
    
    # Cerrar la conexión
    conn.close()
    logger.info("\nInicialización de la base de datos RDS completada")
    logger.info("Si hubo errores de conexión, verifique la configuración de seguridad de RDS")
    logger.info("y asegúrese de que la instancia EC2 tenga permiso para conectarse.")
    logger.info("\nPara verificar manualmente la conexión, puede usar:")
    logger.info(f"psql -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -W")

if __name__ == "__main__":
    logger.info("Iniciando script de inicialización de la base de datos RDS")
    try:
        main()
        logger.info("✅ Script ejecutado correctamente")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error durante la ejecución del script: {e}")
        sys.exit(1)
