# SK Tours & Travels (Django)

Static-style, server-rendered Django website for cab bookings with:
- Public site: cars, drivers, enquiry/booking form
- Auth: user login + staff/admin login
- Admin dashboard (custom UI): CRUD for cars/drivers + manage bookings
- Django admin enabled at `/django-admin/`

## Tech
- Python + Django + Django ORM
- SQLite (default)
- Django templates + static CSS/JS (animations)

## Project structure
```
SK Tours&Travels/
  manage.py
  requirements.txt
  sktt/                     # Django project (settings/urls)
  booking/                  # Main app (models, views, dashboard)
  templates/                # Base + public + auth + dashboard templates
  static/                   # CSS + JS
  media/                    # Uploaded images (created at runtime)
  db.sqlite3                # Created after migrate
```

## Setup (Windows / PowerShell)
From `d:\SK Tours&Travels`:

### 1) Create & activate venv
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
Tip: always run `python manage.py ...` after activating the venv to avoid using a different global Python install.

### 2) Install dependencies
```powershell
pip install -r requirements.txt
```
`Pillow` is included because the project uses Django `ImageField` for car/driver photos.

### 3) (Optional) Environment variables
Copy `.env.example` to `.env` and set a strong key:
```powershell
copy .env.example .env
```

### 4) Migrate database
```powershell
python manage.py migrate
```

### 5) Create admin user
```powershell
python manage.py createsuperuser
```
This user will have access to:
- Custom dashboard: `http://127.0.0.1:8000/dashboard/`
- Django admin: `http://127.0.0.1:8000/django-admin/`

### 6) Seed demo data (cars/drivers + one enquiry)
```powershell
python manage.py seed_demo
```

### 7) Run the server
```powershell
python manage.py runserver
```

Open:
- Public site: `http://127.0.0.1:8000/`
- Cars: `http://127.0.0.1:8000/cars/`
- Drivers: `http://127.0.0.1:8000/drivers/`
- Enquiry form: `http://127.0.0.1:8000/book/`
- Admin dashboard: `http://127.0.0.1:8000/dashboard/`
- Django admin: `http://127.0.0.1:8000/django-admin/`

## How roles work
- **Users (normal login)**:
  - Can browse cars/drivers and submit enquiry (`/book/`).
  - They cannot access `/dashboard/`.
- **Admin/staff**:
  - Any user with `is_staff=True` can access `/dashboard/` and manage cars/drivers/bookings.
  - `createsuperuser` automatically creates a staff user.

## Admin operations (custom dashboard)
After logging in as staff:
- Go to `/dashboard/`
- Manage:
  - Cars: add/edit/delete
  - Drivers: add/edit/delete
  - Bookings: view and update status (New → Contacted → Confirmed/Cancelled)

## Notes
- Image uploads (car/driver photos) are saved to `media/` in development.
- The site is “static-style”: fast, template-rendered pages with CSS/JS animations (no SPA).

