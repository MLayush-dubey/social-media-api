# Social Media API

A robustful and basic RESTful API built with FastAPI for a social media platform featuring user authentication, posts management, and voting system.

## Features

- **User Authentication & Authorization**
  - JWT token-based authentication
  - Secure password hashing with pwdlib
  - OAuth2 with Password flow

- **Posts Management**
  - Create, read, update, and delete posts
  - Search and filter posts by title
  - Pagination support (limit and skip)
  - Post ownership validation

- **Voting System**
  - Like/unlike posts
  - Vote count aggregation
  - Duplicate vote prevention

- **Database Management**
  - PostgreSQL database
  - SQLAlchemy ORM
  - Alembic for database migrations

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migration Tool**: Alembic
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: pwdlib
- **Validation**: Pydantic
- **CORS**: Enabled for cross-origin requests

## Main Project Structure

```
social-media-api/
├── alembic/
│   └── versions/          # Database migration files
├── app/
│   ├── routers/
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── post.py        # Post CRUD operations
│   │   ├── user.py        # User management
│   │   └── votes.py       # Voting system
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection
│   ├── main.py            # Application entry point
│   ├── models.py          # SQLAlchemy models
│   ├── oauth2.py          # JWT token handling
│   ├── schemas.py         # Pydantic schemas
│   └── utils.py           # Utility functions
├── alembic.ini            # Alembic configuration
└── .env                   # Environment variables (not included)
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/MLayush-dubey/social-media-api.git
cd social-media-api
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic pydantic-settings python-jose pwdlib python-multipart
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_database_name
DATABASE_USERNAME=your_username
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the server**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /login` - User login (returns JWT token)

### Users
- `POST /users/` - Create a new user
- `GET /users/{id}` - Get user by ID

### Posts
- `GET /posts/` - Get all posts (with pagination and search)
- `POST /posts/` - Create a new post
- `GET /posts/{id}` - Get a specific post
- `PUT /posts/{id}` - Update a post
- `DELETE /posts/{id}` - Delete a post
- `GET /posts/latest` - Get the latest post

### Votes
- `POST /votes/` - Vote on a post (dir: 1 for like, 0 for unlike)

## Database Schema

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `password` (Hashed)
- `created_at`

### Posts Table
- `id` (Primary Key)
- `title`
- `content`
- `published`
- `created_at`
- `owner_id` (Foreign Key → Users)

### Votes Table
- `user_id` (Foreign Key → Users, Primary Key)
- `post_id` (Foreign Key → Posts, Primary Key)

## Authentication

All protected endpoints require a JWT token. Include it in the request header:
```
Authorization: Bearer <your_token>
```

## Key Features Implementation

### Security
- Passwords are hashed using pwdlib before storage
- JWT tokens expire after a configurable time period
- Foreign key constraints with CASCADE delete

### Authorization
- Users can only update or delete their own posts
- Vote validation prevents duplicate votes
- Post ownership verification on sensitive operations

### Query Optimization
- Posts include vote counts using SQL aggregation
- Efficient JOIN queries for related data
- Pagination to handle large datasets

## Development

### Running Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "migration message"
```

Apply latest migrations:
```bash
alembic upgrade head
```

Rollback migrations:
```bash
alembic downgrade -1
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
