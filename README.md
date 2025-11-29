# 🚀 Social Media API

A production-ready RESTful API built with FastAPI, PostgreSQL, and Docker. This API powers a social media platform with features including user authentication, post management, and a voting system.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Postman](https://img.shields.io/badge/Postman-Tested-FF6C37.svg)](https://www.postman.com/)

## ✨ Features

### Core Functionality
- **User Management**: Secure user registration and authentication
- **JWT Authentication**: Token-based authentication with OAuth2
- **Post CRUD Operations**: Create, read, update, and delete posts
- **Voting System**: Like/unlike functionality for posts
- **Advanced Querying**: Search, pagination, and filtering capabilities
- **Owner-based Authorization**: Users can only modify their own content

### Technical Features
- **Fully Dockerized**: Development and production environments
- **Database Migrations**: Managed with Alembic
- **CORS Support**: Cross-origin resource sharing enabled
- **RESTful Design**: Clean and intuitive API endpoints
- **Type Safety**: Pydantic models for request/response validation
- **Production Ready**: Optimized for deployment on cloud platforms

## 🛠 Tech Stack

**Backend Framework:**
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server

**Database:**
- [PostgreSQL](https://www.postgresql.org/) - Powerful, open-source relational database
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool

**Authentication & Security:**
- [PyJWT](https://pyjwt.readthedocs.io/) - JSON Web Token implementation
- [Pwdlib](https://github.com/frankie567/pwdlib) - Password hashing library
- OAuth2 with Password Bearer flow

**DevOps:**
- [Docker](https://www.docker.com/) - Containerization platform
- Docker Compose - Multi-container orchestration

**Testing & Development:**
- [Postman](https://www.postman.com/) - API testing and development platform

## 🏗 Architecture

```
social-media-api/
├── app/
│   ├── routers/          # API route handlers
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── post.py       # Post management endpoints
│   │   ├── user.py       # User management endpoints
│   │   └── votes.py      # Voting system endpoints
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic validation schemas
│   ├── database.py       # Database connection & session
│   ├── oauth2.py         # JWT token handling
│   ├── utils.py          # Utility functions (hashing, etc.)
│   ├── config.py         # Environment configuration
│   └── main.py           # FastAPI application entry point
├── alembic/              # Database migrations
├── Dockerfile            # Docker image configuration
├── compose.yaml          # Development Docker Compose
├── compose-prod.yaml     # Production Docker Compose
└── requirements.txt      # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- PostgreSQL (if running locally without Docker)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/MLayush-dubey/social-media-api.git
cd social-media-api
```

2. **Create environment file**
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_HOSTNAME=postgres
DATABASE_PORT=5432
DATABASE_PASSWORD=your_secure_password
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=fastapi
```

3. **Run with Docker Compose (Recommended)**

For development:
```bash
docker-compose up -d
```

For production:
```bash
docker-compose -f compose-prod.yaml up -d
```

4. **Or run locally**
```bash
# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` (YOUR LOCAL MACHINE)

### 📚 API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
```http
POST /login
```
Login with email and password to receive JWT token

#### Users
```http
POST /users/          # Create new user
GET  /users/{id}      # Get user by ID
```

#### Posts
```http
GET    /posts/           # Get all posts (with search, pagination)
POST   /posts/           # Create new post
GET    /posts/{id}       # Get specific post
PUT    /posts/{id}       # Update post (owner only)
DELETE /posts/{id}       # Delete post (owner only)
GET    /posts/latest     # Get latest post
```

#### Votes
```http
POST /votes/             # Vote on a post (dir: 1=like, 0=unlike)
```


## 🗄 Database Schema

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `password` (Hashed)
- `created_at`

### Posts Table
- `id` (Primary Key)
- `title`
- `content`
- `published` (Boolean)
- `created_at`
- `owner_id` (Foreign Key → Users)

### Votes Table
- `user_id` (Primary Key, Foreign Key → Users)
- `post_id` (Primary Key, Foreign Key → Posts)

Composite primary key ensures one vote per user per post.

## 🚢 Deployment

### Docker Production Deployment

The project includes a production-ready Docker configuration:

```bash
# Pull the production image
docker pull ayushdubeyyy/fastapi:420

# Run with production compose file
docker-compose -f compose-prod.yaml up -d
```

### Environment Variables

Ensure all required environment variables are set in your production environment:
- Database credentials
- Secret key for JWT signing
- Token expiration settings

### Database Migrations

Run migrations on production:
```bash
docker-compose exec api alembic upgrade head
```

## 🔒 Security Features

- **Password Hashing**: All passwords are hashed using modern algorithms
- **JWT Tokens**: Secure authentication with expiring tokens
- **SQL Injection Prevention**: Parameterized queries via SQLAlchemy
- **CORS Configuration**: Controlled cross-origin access
- **Owner Authorization**: Users can only modify their own content
- **Environment Variables**: Sensitive data stored securely

## 🔧 Troubleshooting & Common Issues

If you are forking or running this project locally, here are some common issues you might encounter and how to resolve them.

### 1. `pg_config` executable not found
**Issue:** When building the Docker image, the build fails during `pip install psycopg2` with an error about missing `pg_config`.
**Cause:** The `python:slim` Docker image lacks the required build tools (`gcc`, `libpq-dev`) to compile `psycopg2` from source.
**Fix:** This project uses `psycopg2-binary` instead of `psycopg2` in `requirements.txt` to avoid compiling C-extensions. If you strictly need the source version, you must install build-essentials in your Dockerfile.

### 2. Hot-Reload Not Working (Windows Docker Desktop)
**Issue:** Changing code in `main.py` or other files does not trigger a server reload when running `docker-compose up`, even though the volume is mounted correctly.
**Cause:** Docker on Windows (using WSL2) sometimes fails to propagate file system change events to the Linux container.
**Fix:** The `compose.yaml` file includes the environment variable `WATCHFILES_FORCE_POLLING=true`. This forces Uvicorn to poll for file changes instead of relying on broken file system events.

### 3. Pydantic "Extra inputs not permitted" Error
**Issue:** The application crashes on startup with a `ValidationError` pointing to `POSTGRES_PASSWORD` or `POSTGRES_DB`.
**Cause:** Docker passes all variables from `.env` to the container. If your Pydantic `Settings` model doesn't define fields for these extra Docker-specific variables, it throws an error by default.
**Fix:** The `app/config.py` uses `extra="ignore"` in the `model_config`-->model_config = SettingsConfigDict(env_file=".env", extra="ignore")

### 4. Connection Refused to Database
**Issue:** Application fails to connect to the database with `Connection refused`.
**Fix:**
- **Docker Mode:** Ensure your `.env` sets `DATABASE_HOSTNAME=postgres` (matches the service name in `compose.yaml`).
- **Local Mode:** Ensure your `.env` sets `DATABASE_HOSTNAME=localhost` and your local Postgres server is running.

## 📝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 👤 Author

**Ayush Dubey**
- GitHub: [@MLayush-dubey](https://github.com/MLayush-dubey)
- Docker Hub: [ayushdubeyyy](https://hub.docker.com/u/ayushdubeyyy)


⭐ If you find this project helpful, please consider giving it a star on GitHub!
