# Auth Login/Signup Service

A microservice built with FastAPI that handles user authentication and registration.

## Features

- User registration (signup)
- User authentication (login) with JWT
- Health check endpoint
- Password hashing with bcrypt
- Rate limiting for protection against brute force attacks
- Event-driven architecture (Kafka/RabbitMQ integration)
- Prometheus metrics for observability
- Structured logging

## Requirements

- Python 3.11+
- PostgreSQL database

## Environment Variables

Copy `.env.example` to `.env` and adjust the values:

```bash
# Database
DATABASE_URL=postgresql://auth_user:secret@localhost:5432/auth_db

# JWT
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# Message Broker
MESSAGE_BROKER_URL=kafka://localhost:9092
```

## Running Locally

### Using Docker

```bash
# Build and run the service with docker-compose
docker-compose up -d
```

### Without Docker

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate

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
