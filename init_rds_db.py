#!/usr/bin/env python3
"""
Script para inicializar la base de datos RDS directamente con SQL.
Este script lee el archivo init_db.sql y lo ejecuta en la base de datos RDS.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de la base de datos RDS
DB_HOST = os.getenv("DB_HOST", "auth-db.cyllotifqg8b.us-east-1.rds.amazonaws.com")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "users_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Uzumymw260916_")

# Ruta al archivo SQL
SQL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "init_db.sql")

def execute_sql_file(connection_string, sql_file):
    """Ejecuta un archivo SQL en la base de datos."""
    try:
        # Conectar a la base de datos
        logger.info(f"Conectando a la base de datos: {connection_string}")
        conn = psycopg2.connect(connection_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Leer y ejecutar el archivo SQL
        logger.info(f"Ejecutando archivo SQL: {sql_file}")
        with open(sql_file, 'r') as f:
            sql = f.read()
            cursor.execute(sql)
        
        # Verificar las tablas creadas
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()
        logger.info(f"Tablas en la base de datos: {tables}")
        
        # Cerrar la conexión
        cursor.close()
        conn.close()
        logger.info("Inicialización de la base de datos completada con éxito!")
        return True
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        return False

def main():
    """Función principal."""
    try:
        # Construir la cadena de conexión
        connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        # Ejecutar el archivo SQL
        success = execute_sql_file(connection_string, SQL_FILE)
        
        # Salir con el código de estado apropiado
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
