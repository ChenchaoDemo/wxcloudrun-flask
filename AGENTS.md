# AGENTS.md

## Project Overview

This repository is a Python Flask application designed for deployment on WeChat Cloud Run.
It uses Flask-SQLAlchemy and PyMySQL to connect to the `flask_demo` MySQL database.

Main endpoints:

- `GET /` renders the home page.
- `GET /api/count` reads the counter.
- `POST /api/count` increments or clears the counter.
- `/api/orders` provides order CRUD operations.

## Project Structure

- `run.py`: local application entry point.
- `config.py`: application and database configuration.
- `wxcloudrun/__init__.py`: Flask and SQLAlchemy initialization.
- `wxcloudrun/views.py`: HTTP routes and request handling.
- `wxcloudrun/model.py`: SQLAlchemy models.
- `wxcloudrun/dao.py`: database access functions.
- `wxcloudrun/response.py`: JSON response helpers.
- `wxcloudrun/templates/`: HTML templates.
- `container.config.json`: WeChat Cloud Run deployment and database initialization settings.

## Local Development

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Set database credentials through environment variables when possible:

```powershell
$env:MYSQL_USERNAME="root"
$env:MYSQL_PASSWORD="<password>"
$env:MYSQL_ADDRESS="<host>:<port>"
```

Run the application:

```powershell
python run.py 127.0.0.1 8080
```

## Validation

Run syntax checks for changed Python files:

```powershell
python -m py_compile config.py run.py wxcloudrun\*.py
```

Smoke-test the main endpoints after starting the application:

```powershell
Invoke-RestMethod http://127.0.0.1:8080/api/count
Invoke-RestMethod http://127.0.0.1:8080/api/orders
```

When database behavior changes, test create, read, update, and delete operations. Remove any temporary test data after verification.

## Coding Guidelines

- Keep route handlers focused on validation and response construction.
- Put database models in `model.py` and reusable database operations in `dao.py`.
- Preserve the existing response format: `{"code": 0, "data": ...}` for success and `{"code": -1, "errorMsg": ...}` for errors.
- Roll back the SQLAlchemy session after failed write operations.
- Avoid unrelated formatting or encoding changes in legacy files.
- Use ASCII for new code comments and documentation unless Chinese text is required.

## Database And Security

- Do not add new plaintext passwords, tokens, or credentials to tracked files.
- Prefer `MYSQL_USERNAME`, `MYSQL_PASSWORD`, and `MYSQL_ADDRESS` environment variables.
- Do not log database passwords or include them in test output.
- Do not drop tables, truncate data, or run destructive migrations unless explicitly requested.
- Keep SQL in `container.config.json` compatible with the deployed MySQL version.

## Git Workflow

- Inspect `git status` before editing because the worktree may contain user changes.
- Do not revert or overwrite changes that are unrelated to the current task.
- Run syntax checks and relevant endpoint tests before committing.
- Do not commit or push unless explicitly requested.
