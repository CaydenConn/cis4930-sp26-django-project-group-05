# Project 3

This Django project now includes the 2.6 deployment-readiness updates:

- Settings split into `config/settings/base.py`, `config/settings/dev.py`, and `config/settings/prod.py`
- `python-decouple` used for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and `DATABASE_URL`
- `.env` kept out of version control through the repo-level `.gitignore`
- `requirements.txt` refreshed from the active environment
- `Procfile` and `runtime.txt` added for deployment on Railway or Render
- Production settings configured with `gunicorn` and `whitenoise`

## Local Setup

```powershell
C:/Users/Judah/AppData/Local/Microsoft/WindowsApps/python3.13.exe -m pip install -r requirements.txt
C:/Users/Judah/AppData/Local/Microsoft/WindowsApps/python3.13.exe manage.py migrate
C:/Users/Judah/AppData/Local/Microsoft/WindowsApps/python3.13.exe manage.py seed_data
C:/Users/Judah/AppData/Local/Microsoft/WindowsApps/python3.13.exe manage.py runserver
```

Open the app at `http://127.0.0.1:8000/`.

## Deployment Check

I verified the production settings with Django's deploy check:

```powershell
$env:DEBUG='False'; $env:ALLOWED_HOSTS='localhost,127.0.0.1'; C:/Users/Judah/AppData/Local/Microsoft/WindowsApps/python3.13.exe manage.py check --settings=config.settings.prod --deploy
```

Output:

```text
System check identified no issues (0 silenced).
```

## Deployment Notes

- `manage.py` uses `config.settings.dev` for local development.
- `mysite/wsgi.py` and `mysite/asgi.py` use `config.settings.prod` for deployment.
- The `Procfile` entry is:

```text
web: gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT
```

