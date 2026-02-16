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

## TO DO LIST
- [ ] Password hashing
- [ ] Add ROLES to database: 

    - <b><u>ADMINISTRATIVE ROLES("The Staff")</b></u>
    - - <b>Super / Owner (Level 1) </b><br>
    <u>Capabilities:</u> Has catastrophic power. Can delete the database, manage billing/revenue settings, view sensitive financial data, and creating/deleting other Admins.
    <u>Use Case:</u> This is me. There should usually be only one or two of these.
    -  - <b>Admin (Level 2)</b> <br>
    <u>Capabilities:</u> Day-to-day management. Can ban users, refund payments, view user data for support, and manage content. Cannot access system-wide keys or delete the Owner.       

    - - <b>Mod & Support (Level 3)</b><br>
    <u>Capabilities:</u> "Read-only" access to user profiles to help debug issues. Can reset passwords or mute detailed logs. Cannot delete data or authorize payments.
    <u>Use Case:</u> Customer support staff you might hire later.
    - -<b><u>USER MEMBERSHIP TIERS</b></u>
    - - <b>Enterprise (Tier 2)</b>
    - - <b>Pro (Tier 1)</b>
    - - <b>Free (Tier 0)</b>
    - - <b>Guest (no account)</b>


- [ ] Github Actions
- [ ] Login & Authentication