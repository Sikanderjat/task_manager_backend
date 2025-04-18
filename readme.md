# Task Manager Backend Documentation

Project Structure

```
/flask_backend_project
│── /app
│   ├── /api
│   │   ├── __init__.py
│   │   ├── routes.py              # Defines API endpoints
│   ├── /models
│   │   ├── __init__.py
│   │   ├── user.py                # User model (RBAC)
│   │   ├── task_manager.py        # TaskManager model
│   │   ├── task_logger.py         # TaskLogger model
│   ├── /services
│   │   ├── __init__.py
│   │   ├── task_service.py        # Task processing logic
│   │   ├── user_service.py        # User management logic
│   ├── /repositories
│   │   ├── __init__.py
│   │   ├── task_repository.py     # DB queries for tasks
│   │   ├── user_repository.py     # DB queries for users
│   ├── /workers
│   │   ├── __init__.py
│   │   ├── celery_worker.py       # Celery worker setup
│   │   ├── daily_task_loader.py   # Celery task logic
│   ├── /utils
│   │   ├── __init__.py
│   │   ├── db.py                  # SQLAlchemy setup
│   │   ├── redis_cache.py         # Redis caching
│   │   ├── security.py            # JWT authentication & hashing
│   │   ├── rate_limiter.py        # API rate limiting
│   ├── __init__.py
│   ├── config.py                  # App configuration (ENV, DB)
│   ├── main.py                    # Flask app entry point
│
│── /migrations                    # Alembic migration scripts
│── /tests
│   ├── test_tasks.py              # Unit tests for task APIs
│   ├── test_auth.py               # Unit tests for authentication
│── /docs                          # API documentation
│── .env                           # Environment variables
│── .dockerignore
│── .gitignore
│── Dockerfile                     # Docker setup
│── docker-compose.yml             # Multi-container setup
│── requirements.txt               # Dependencies
│── README.md                      # Project documentation
```

## Prerequisites

Before setting up the project, ensure you have the following installed:

- [Python 3.11]
- [PostgreSQL]
- [Redis]
- [Docker]

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Sikanderjat/task_manager_backend.git
   cd task_manager_backend
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   Create a `.env` file in the project root and set the following variables:

   ```env
   FLASK_ENV=development
   DATABASE_URL=postgresql://username:password@localhost:5432/task_manager_db
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=your_secret_key
   ```

   Replace `username`, `password`, and `your_secret_key` with appropriate values.

5. **Initialize the Database:**

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Start Redis Server:**

   Ensure Redis is running on `localhost:6379`. If not, start the Redis server:

   ```bash
   redis-server
   ```

7. **Run the Flask Application:**

   ```bash
   python -m app.main
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

8. **Start the Celery Worker:**

   In a new terminal window, activate the virtual environment and run:

   ```bash
   celery -A app.workers.celery_worker.celery worker --loglevel=info
   ```

## API Endpoints

The application provides the following API endpoints:

- **User Management:**
  - `POST /api/users/register`: Register a new user.
  - `POST /api/users/login`: Authenticate a user and return a JWT.
  - `GET /api/users/profile`: Retrieve the authenticated user's profile.

- **Task Management:**
  - `POST /api/tasks/`: Create a new task.
  - `GET /api/tasks/`: Retrieve all tasks.
  - `GET /api/tasks/<task_id>`: Retrieve a specific task by ID.
  - `PUT /api/tasks/<task_id>`: Update a specific task.
  - `DELETE /api/tasks/<task_id>`: Delete a specific task.

## Running Tests

To run the test suite:

```bash
pytest tests/
```

Ensure that the test database is configured correctly in your `.env` file.

## Docker Deployment

To deploy the application using Docker:

1. **Build the Docker Image:**

   ```bash
   docker build -t task_manager_backend .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -p 5000:5000 --env-file .env task_manager_backend
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

## Troubleshooting

- **Import Errors:**

  Ensure that all modules are imported correctly. For example, in `app/__init__.py`, import models as:

  ```python
  from app.models.user import User
  from app.models.task_manager import TaskManager
  from app.models.task_logger import TaskLogger
  ```

- **Redis Connection Issues:**

  If you encounter errors connecting to Redis, ensure that the Redis server is running and accessible at the specified `REDIS_URL`.  
