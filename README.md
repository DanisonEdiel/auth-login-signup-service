# Auth Login/Signup Service

Microservicio construido con FastAPI para gestionar autenticación y registro de usuarios.

## Características

- Registro de usuarios (signup)
- Autenticación de usuarios (login) con JWT
- Endpoint de health check
- Encriptación de contraseñas con bcrypt
- Limitación de tasa para protección contra ataques de fuerza bruta
- Arquitectura basada en eventos (integración con Kafka)
- Métricas Prometheus para observabilidad
- Logging estructurado
- Soporte asíncrono para base de datos con SQLAlchemy

## Requisitos

- Python 3.11+
- PostgreSQL database (RDS en producción)
- Kafka

## Preparación para Producción en EC2

### 1. Configuración de Base de Datos RDS

#### Estructura de la tabla `users`

La tabla `users` debe tener la siguiente estructura en PostgreSQL:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR NOT NULL UNIQUE,
    username VARCHAR UNIQUE,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

> **Nota**: La aplicación puede crear automáticamente las tablas al iniciar si tiene los permisos adecuados.

### 2. Variables de Entorno

Copia `.env.example` a `.env` y ajusta los valores para producción:

```bash
# Database - Actualiza con tu endpoint de RDS
DATABASE_URL=postgresql+asyncpg://auth_user:your-secure-password@your-rds-endpoint.region.rds.amazonaws.com:5432/auth_db

# JWT - Genera una clave segura para producción
JWT_SECRET=generate-a-secure-random-key-for-production

# Message Broker - Actualiza con tu broker de Kafka
MESSAGE_BROKER_URL=kafka://your-kafka-broker:9092
```

### 3. Despliegue en EC2

#### Opción 1: Despliegue con Docker

```bash
# 1. Clona el repositorio en tu instancia EC2
git clone <tu-repositorio> auth-service
cd auth-service

# 2. Crea el archivo .env con tus variables de entorno
cp .env.example .env
# Edita el archivo .env con tus valores de producción

# 3. Construye y despliega con Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# 4. Verifica que los contenedores estén funcionando
docker ps

# 5. Revisa los logs si es necesario
docker-compose logs -f app
```

#### Opción 2: Despliegue sin Docker

```bash
# 1. Clona el repositorio en tu instancia EC2
git clone <tu-repositorio> auth-service
cd auth-service

# 2. Crea un entorno virtual
python -m venv venv

# 3. Activa el entorno virtual
# En Linux/Mac
source venv/bin/activate
# En Windows
venv\Scripts\activate

# 4. Instala las dependencias
pip install -r requirements.txt

# 5. Crea el archivo .env con tus variables de entorno
cp .env.example .env
# Edita el archivo .env con tus valores de producción

# 6. Ejecuta la aplicación con Gunicorn (para producción)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 4. Configuración de Seguridad

- Asegúrate de configurar los grupos de seguridad de EC2 para permitir tráfico en el puerto 8000
- Considera usar un balanceador de carga y HTTPS para producción
- Configura un nombre de dominio y SSL con Let's Encrypt

### 5. Monitoreo y Mantenimiento

- Configura CloudWatch para monitorear la instancia EC2
- Implementa un sistema de logs centralizado
- Configura alertas para errores y alto uso de recursos

## Endpoints API

- `GET /health` - Verificar estado del servicio
- `POST /auth/signup` - Registrar un nuevo usuario
- `POST /auth/login` - Autenticar usuario y obtener token JWT
- `GET /auth/me` - Obtener información del usuario actual (requiere autenticación)

## Estructura de la Base de Datos

La aplicación utiliza una única tabla `users` con los siguientes campos:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | Identificador único (clave primaria) |
| email | VARCHAR | Email del usuario (unique) |
| username | VARCHAR | Nombre de usuario (unique, opcional) |
| hashed_password | VARCHAR | Contraseña encriptada |
| full_name | VARCHAR | Nombre completo (opcional) |
| is_active | BOOLEAN | Si el usuario está activo |
| is_superuser | BOOLEAN | Si el usuario tiene privilegios de administrador |
| created_at | TIMESTAMP | Fecha de creación |
| updated_at | TIMESTAMP | Fecha de última actualización |

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Run the service
uvicorn app.main:app --reload
```

## API Documentation

Once the service is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
# Run tests
pytest

# Run linting
flake8
```

## Project Structure

```
auth-login-signup-service/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── auth.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── events.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth_service.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_auth.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── init_db.py
├── requirements.txt
└── README.md
```
