# Auth Login/Signup Service

Microservice built with FastAPI to manage user authentication and registration.

## Features

- User registration (signup)
- User authentication (login) with JWT
- Health check endpoint
- Password encryption with bcrypt
- Rate limiting to protect against brute-force attacks
- Event-driven architecture (integration with Kafka)
- Prometheus metrics for observability
- Structured logging
- Asynchronous database support with SQLAlchemy

## Requirements

- Python 3.11+
- PostgreSQL database (RDS in production)
- Kafka

## Preparing for Production on EC2

### 1. RDS Database Configuration

#### Structure of the `users` table

The `users` table must have the following structure in PostgreSQL:

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

> **Note**: The application can automatically create the tables on startup if you have the appropriate permissions.

### 2. Environment Variables

Copy `.env.example` to `.env` and adjust the values ​​for production:

```bash
# Database - Update with your RDS endpoint
DATABASE_URL=postgresql+asyncpg://auth_user:your-secure-password@your-rds-endpoint.region.rds.amazonaws.com:5432/auth_db

# JWT - Generate a secure key for production
JWT_SECRET=generate-a-secure-random-key-for-production

# Message Broker - Update with your Kafka broker
MESSAGE_BROKER_URL=kafka://your-kafka-broker:9092
```

### 3. Deploy to EC2

#### Option 1: Deploy with Docker

```bash
# 1. Clone the repository to your EC2 instance
git clone <your-repository> auth-service
cd auth-service

# 2. Create the .env file with your environment variables
cp .env.example .env
# Edit the .env file with your production values

# 3. Build and deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# 4. Verify that the containers are running
docker ps

# 5. Review the logs if necessary
docker-compose logs -f app
```

#### Option 2: Deployment without Docker

```bash
# 1. Clone the repository to your EC2 instance
git clone <your-repository> auth-service
cd auth-service

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the environment virtual
# On Linux/Mac
source venv/bin/activate
# On Windows
venv\Scripts\activate

# 4. Install Dependencies
pip install -r requirements.txt

# 5. Create the .env file with your environment variables
cp .env.example .env
# Edit the .env file with your production values

# 6. Run the application with Gunicorn (for production)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### 4. Security Configuration

- Make sure you configure EC2 security groups to allow traffic on port 8000
- Consider using a load balancer and HTTPS for production
- Set up a domain name and SSL with Let's Encrypt

### 5. Monitoring and Maintenance

- Configure CloudWatch to monitor the EC2 instance
- Implement a centralized logging system
- Configure alerts for errors and high resource usage

## API Endpoints

- `GET /health` - Check service status
- `POST /auth/signup` - Register a new user
- `POST /auth/login` - Authenticate the user and obtain a JWT token
- `GET /auth/me` - Obtain information about the current user (requires authentication)

## Database Structure

The application uses a single `users` table with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier (primary key) |
| email | VARCHAR | User email (unique) |
| username | VARCHAR | Username (unique, optional) |
| hashed_password | VARCHAR | Encrypted password |
| full_name | VARCHAR | Full name (optional) |
| is_active | BOOLEAN | If the user is active |
| is_superuser | BOOLEAN | If the user has administrator privileges |
| created_at | TIMESTAMP | Creation date |
| updated_at | TIMESTAMP | Last updated date |

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
