import psycopg2
import sys

def test_connection(host, port, dbname, user, password):
    """Test connection to PostgreSQL database"""
    try:
        # Construct connection string
        conn_string = f"host={host} port={port} dbname={dbname} user={user} password={password}"
        print(f"Connecting to database: {host}:{port}/{dbname} as {user}")
        
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(conn_string)
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute a test query
        cur.execute("SELECT version();")
        
        # Get the result
        version = cur.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        print("Connection successful!")
        return True
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    # Database connection parameters
    host = "auth-db.cyllotifqg8b.us-east-1.rds.amazonaws.com"
    port = "5432"
    dbname = "users_db"  # Nombre correcto de la base de datos según la captura
    user = "postgres"
    password = "Uzumymw260916_"
    
    # Test the connection
    success = test_connection(host, port, dbname, user, password)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
