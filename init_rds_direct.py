#!/usr/bin/env python3
"""
Script para inicializar directamente la base de datos RDS desde la instancia EC2.
Este script se conecta directamente a la base de datos RDS y ejecuta el script SQL
para crear las tablas necesarias.
"""

import os
import sys
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
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Ruta al archivo SQL
SQL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "init_db.sql")

def create_tables():
    """Ejecuta el script SQL para crear las tablas en la base de datos RDS."""
    try:
        logger.info(f"Conectando a la base de datos RDS en {DB_HOST}:{DB_PORT}/{DB_NAME} con usuario {DB_USER}")
        
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Crear un cursor
        cursor = conn.cursor()
        
        # Leer el archivo SQL
        try:
            with open(SQL_FILE, 'r') as f:
                sql_script = f.read()
                logger.info(f"Archivo SQL leído correctamente: {SQL_FILE}")
        except Exception as e:
            logger.error(f"Error al leer el archivo SQL: {e}")
            return False
        
        # Ejecutar el script SQL
        logger.info("Ejecutando script SQL para crear tablas...")
        cursor.execute(sql_script)
        
        # Verificar que la tabla users existe
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users');")
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            logger.info("✅ La tabla 'users' se ha creado correctamente")
        else:
            logger.error("❌ La tabla 'users' no se ha creado")
            return False
        
        # Verificar las columnas de la tabla users
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'users';")
        columns = [col[0] for col in cursor.fetchall()]
        logger.info(f"Columnas en la tabla 'users': {columns}")
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        logger.info("Inicialización de la base de datos RDS completada con éxito")
        return True
        
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos RDS: {e}")
        return False

if __name__ == "__main__":
    logger.info("Iniciando script de inicialización de la base de datos RDS")
    success = create_tables()
    if success:
        logger.info("✅ Script ejecutado correctamente")
        sys.exit(0)
    else:
        logger.error("❌ Error al ejecutar el script")
        sys.exit(1)
