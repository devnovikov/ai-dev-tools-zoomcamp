# Django TODO Application

Homework 1 for [AI Dev Tools Zoomcamp 2025](https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/) by DataTalks.Club.

This TODO application was built entirely with AI assistance to demonstrate AI-assisted development workflows.

## Features

- Create, edit, and delete TODOs
- Assign due dates to tasks
- Mark TODOs as resolved/reopened
- Responsive Bootstrap 5 UI
- Comprehensive test coverage (16 tests)

## Project Structure

```
01-todo/
-> manage.py              # Django management script
-> pyproject.toml         # Python project config (uv/pip)
-> uv.lock                # Locked dependencies
-> db.sqlite3             # SQLite database
-> todoproject/           # Django project settings
---   -> __init__.py
---   -> settings.py        # Project configuration
---   -> urls.py            # Root URL routing
---   -> wsgi.py            # WSGI application
---   ---> asgi.py            # ASGI application
-> todos/                 # TODO app
---   -> __init__.py
---   -> models.py          # Todo model definition
---   -> views.py           # CRUD view functions
---   -> urls.py            # App URL patterns
---   -> forms.py           # TodoForm with Bootstrap
---   -> admin.py           # Admin panel config
---   -> tests.py           # 16 comprehensive tests
---   -> apps.py            # App configuration
---   ---> migrations/        # Database migrations
-> templates/             # HTML templates
---   -> base.html          # Base template with Bootstrap
---   -> home.html          # TODO list view
---   -> todo_form.html     # Create/Edit form
---   ---> todo_confirm_delete.html
-> .serena/               # Serena MCP config
---> CLAUDE.md              # Claude Code instructions
```

## File Descriptions

### Project Configuration

| File | Purpose |
|------|---------|
| `manage.py` | Django's command-line utility for administrative tasks |
| `pyproject.toml` | Python project metadata and dependencies (Django 5.2.8) |
| `uv.lock` | Locked dependency versions for reproducible builds |

### Django Project (`todoproject/`)

| File | Purpose |
|------|---------|
| `settings.py` | Django settings - database, installed apps, templates config |
| `urls.py` | Root URL configuration - includes admin and todos app URLs |
| `wsgi.py` | WSGI entry point for production deployment |
| `asgi.py` | ASGI entry point for async deployment |

### TODO Application (`todos/`)

| File | Purpose |
|------|---------|
| `models.py` | `Todo` model with fields: title, description, due_date, resolved, created_at, updated_at |
| `views.py` | View functions: list, create, edit, delete, toggle resolved status |
| `urls.py` | URL patterns mapping to views (list, create, edit, delete, toggle) |
| `forms.py` | `TodoForm` ModelForm with Bootstrap CSS classes |
| `admin.py` | Admin panel registration with list display, filters, search |
| `tests.py` | Test suite: 4 model tests, 10 view tests, 2 validation tests |
| `apps.py` | App configuration class |

### Templates (`templates/`)

| File | Purpose |
|------|---------|
| `base.html` | Base template with Bootstrap 5 CDN, navigation, CSS for resolved items |
| `home.html` | Main view showing TODO list with action buttons |
| `todo_form.html` | Reusable form template for create/edit operations |
| `todo_confirm_delete.html` | Delete confirmation page |

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd 01-todo

# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

## Running the Application

```bash
# Apply database migrations
uv run python manage.py migrate

# Start the development server
uv run python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Running Tests

```bash
uv run python manage.py test
```

All 16 tests should pass:
- `TodoModelTests` (4 tests): creation, string representation, defaults, ordering
- `TodoViewTests` (10 tests): list, create, edit, delete, toggle operations
- `TodoFormValidationTests` (2 tests): required fields, date validation

## Development Process

This application was built step-by-step with AI assistance:

1. **Project Setup**: Initialized with `uv init --python 3.13` and added Django
2. **Django Project**: Created with `django-admin startproject todoproject .`
3. **App Creation**: Created todos app with `python manage.py startapp todos`
4. **Configuration**: Added app to `INSTALLED_APPS`, configured template directory
5. **Model Design**: Created `Todo` model with all required fields
6. **Migrations**: Generated and applied database schema
7. **CRUD Views**: Implemented list, create, edit, delete, toggle views
8. **URL Routing**: Set up URL patterns for all operations
9. **Templates**: Created Bootstrap-styled templates with inheritance
10. **Admin Panel**: Registered model with enhanced display options
11. **Testing**: Wrote comprehensive test suite covering all functionality

## Homework Answers

| Question | Answer |
|----------|--------|
| Q1: Install Django command | `uv add django` |
| Q2: File to add app | `settings.py` (INSTALLED_APPS) |
| Q3: After creating models | Run migrations |
| Q4: Where to put logic | `views.py` |
| Q5: Register template dir | `TEMPLATES['DIRS']` in settings.py |
| Q6: Run tests command | `python manage.py test` |

## License

This project is for educational purposes