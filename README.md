# Financial Monitor

A web application for monitoring finances. It allows tracking upcoming transactions, past history, and adding new ones, including recurring ones that repeat automatically. It can display balance charts of income and expenses for the current month, as well as expenses broken down by category.

## Technologies

- **FRONTEND:** React, TypeScript, Vite, TailwindCSS, Bun
- **BACKEND:** FastAPI, SQLAlchemy, Alembic, APScheduler
- **DATABASE:** PostgreSQL
- **DEPLOYMENT:** Docker, Nginx

## Requirements

- Docker
  or locally:
- Python 3.14, Bun, PostgreSQL 16

## Environment variables:

### `.env` - Database (Docker)

| Variable            | Description           |
| ------------------- | --------------------- |
| `POSTGRES_DB`       | Database name         |
| `POSTGRES_USER`     | Database user         |
| `POSTGRES_PASSWORD` | User password         |

### `backend/.env`

| Variable            | Description                                  |
| ------------------- | -------------------------------------------- |
| `DB_USER`           | Database user                                |
| `DB_PASS`           | Database user password                       |
| `DB_HOST`           | Database server for local development        |
| `DB_PORT`           | Database server port                         |
| `DB_NAME`           | Database name                                |
| `SECRET_KEY`        | Key used for JWT tokens                      |
| `TOKEN_EXPIRE_MINS` | JWT token lifetime in minutes                |

### `frontend/.env` (local server) | `frontend/.env.production` (Docker)

| Variable       | Description         |
| -------------- | ------------------- |
| `VITE_API_URL` | Backend API address |

Create both files following `.env.example`.

**.env** for the local server (e.g. `http://127.0.0.1:8000`) and **.env.production** for Docker (e.g. `http://localhost/api`)

## Running with Docker

Create and fill in the `.env` files according to the examples and descriptions above

Database migrations (Alembic) run automatically when the backend starts.

First run:

```bash
docker-compose up --build
```

Subsequent runs:

```bash
docker-compose up
```

## Running locally

Create and fill in the `.env` files according to the examples and descriptions above

### FRONTEND

First run:

```bash
bun install
bun run dev
```

Subsequent runs:

```bash
bun run dev
```

### BACKEND

First run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Subsequent runs:

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

### DATABASE

Start a PostgreSQL server, create the database, and run the migrations:

```bash
alembic upgrade head
```

### TESTS

Run the backend tests (pytest) from the `backend` directory:

```bash
pytest
```

The API request collection is located in `backend/postman`.

## Project structure

```bash
fin_cal/
├── backend          # FastAPI
│   ├── alembic      # Database migrations
│   ├── models       # SQLAlchemy models
│   ├── routers      # API endpoints
│   ├── schemas      # Pydantic schemas
│   ├── services     # Business logic
│   ├── security     # Authorization and passwords
│   ├── scheduler    # Recurring jobs (APScheduler)
│   ├── tests        # pytest tests
│   └── postman      # Postman collection
├── frontend         # React
└── docker-compose.yaml
```