# Setup: run this project on your machine

Project root: `/Users/wseyler/django/ikyoshi_project`

## One-command setup (recommended)

From the project folder, with ARM Homebrew available (`eval "$(/opt/homebrew/bin/brew shellenv)"` if needed):

```bash
cd /Users/wseyler/django/ikyoshi_project
./setup.sh
```

Then start the app:

```bash
source venv/bin/activate
python manage.py runserver
```

Open **http://127.0.0.1:8000/** when it’s running.

---

## Manual setup

Use these steps if you prefer to run each part yourself.

### 1. Use ARM Homebrew (Apple Silicon)

```bash
eval "$(/opt/homebrew/bin/brew shellenv)"
```

(Skip if you already did this in your terminal or in `~/.zprofile`.)

## 2. Recreate the virtual environment

The existing `venv` was created in another directory. Recreate it for this machine:

```bash
cd /Users/wseyler/django/ikyoshi_project
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements-local.txt
```

(Use `requirements-local.txt` for SQLite-only local dev; it omits `mysqlclient`. Use `requirements.txt` if you use MySQL.)

## 4. Run database migrations

(Uses SQLite by default; `db.sqlite3` already exists and will be updated if needed.)

```bash
python manage.py migrate
```

## 5. (Optional) Collect static files

Only needed if you use `DEBUG = False` or serve static files via a real web server:

```bash
python manage.py collectstatic --noinput
```

## 6. Run the development server

```bash
python manage.py runserver
```

Then open: **http://127.0.0.1:8000/**

---

## Quick reference

| Task              | Command                                      |
|-------------------|----------------------------------------------|
| Activate venv     | `source venv/bin/activate`                   |
| Deactivate venv   | `deactivate`                                 |
| Run server        | `python manage.py runserver`                 |
| Run migrations    | `python manage.py migrate`                   |
| Create superuser  | `python manage.py createsuperuser`           |

## Notes

- **Database:** Default is SQLite (`db.sqlite3`). No extra DB setup needed.
- **local_settings.py:** If you add `ikyoshi/local_settings.py`, it will override settings (e.g. `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, or MySQL). Optional for local dev.
- **requirements-local.txt** is for SQLite-only local dev (no `mysqlclient`). **requirements.txt** includes `mysqlclient` for MySQL; use that if you use MySQL.
