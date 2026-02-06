# ACCOUNT MANAGER

## Objectives

Create a Python web GUI running on Flask. <br>
postgreSQL server to manage account entries.
Validate inputted data
Security measures: CSRF (Cross-Site Request Forgery)

## Requisites

- Python 3.12
- Flask
- postgreSQL

## FILE STRUCTURE

### A professional Flask layout is app package + blueprints + config + models.

Example:

account-manager/ <br>
├── app/ <br>
│ ├── **init**.py # create_app(), extensions <br>
│ ├── config.py # settings (env, secrets) <br>
│ ├── models.py # SQLAlchemy models <br>
│ ├── db.py # engine/session setup <br>
│ ├── forms.py # WTForms classes <br>
│ ├── routes/ <br>
│ │ └── main.py # blueprint routes <br>
│ └── templates/ <br>
├── wsgi.py # entrypoint <br>
└── server.py # legacy launcher or removed <br>

### Result: Cleaner structure, easier testing, and production-ready for WSGI (wsgi.py).

### Typical routes/ folder structure:

app/routes/
├── **init**.py # optional: export all blueprints
├── main.py # homepage, general pages
├── auth.py # login, logout, register, password reset
├── users.py # user profile, settings, admin user management
├── api.py # REST API endpoints
├── admin.py # admin dashboard, management tools
└── errors.py # custom error handlers (404, 500)
