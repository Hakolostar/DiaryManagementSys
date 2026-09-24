# 🥛 Dairy Management System

A modern, professional dairy farm management system built with **Django**, **Tailwind CSS** and
**HTMX**. This is a full rewrite of the legacy `DigitalDairy` project with a clean, modular
architecture and a contemporary user interface.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## ✨ Features

| Module           | What it covers |
|------------------|----------------|
| **Dashboard**    | KPIs, 14-day milk trend chart, herd composition, income vs expense chart, due-heat / calving / vaccination alerts, low stock |
| **Herd**         | Animal Master, Breeds, Animal Movement, Animal History (lifetime activity timeline) |
| **Milk Production** | Morning Milk, Evening Milk, Cow Yield (vs targets), Lactation, Milk Quality |
| **Breeding**     | Heat detection, AI / Insemination, Pregnancy checks, Calving |
| **Health**       | Veterinary Visits, Vaccination (with due-date tracking), Treatment, Medicine stock |
| **Feed**         | Feed Items, Feed Consumption, Feed Purchase, Feed Cost analysis |
| **Inventory**    | Stock items, stock value, low-stock alerts, stock In / Out / Adjustment |
| **Sales**        | Milk / animal / product sales, customers, payment tracking |
| **Purchases**    | Purchases and suppliers with balance tracking |
| **Finance**      | Income & expense transactions, categories |
| **Employees**    | Staff, salary payments, salary advances |
| **Reports**      | Printable reports for every domain with date-range filters |

## 🛠 Technology Stack

- **Backend:** Python 3.14, Django 6.x, SQLite (switchable to PostgreSQL/MySQL)
- **Frontend:** Tailwind CSS 3.x, HTMX 1.9, Chart.js
- **Assets:** WhiteNoise for static files, `django-filter` for filtering

## 🚀 Quick Start

> ⚠️ **Windows / OneDrive note:** `python -m venv` can fail inside OneDrive-synced folders.
> If you hit `WinError 2`, create the virtual environment outside the project (e.g.
> `C:\Users\<you>\.venvs\dairy_mgmt`) and use its `python.exe` in the steps below.

```bash
# 1. Create & activate a virtual environment
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # macOS / Linux

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install the Tailwind CLI (Node.js required)
npm install

# 4. Build the Tailwind stylesheet
npm run css:build

# 5. Run database migrations
python manage.py migrate

# 6. Create an admin user
python manage.py createsuperuser

# 7. (Optional) Load realistic demo data
python manage.py seed_data

# 8. Start the development server
python manage.py runserver
```

Open <http://127.0.0.1:8000> and sign in.

### Rebuilding styles while developing

```bash
npm run css:watch
```

### Production-ish static serving

```bash
python manage.py collectstatic --noinput
python manage.py runserver    # WhiteNoise serves /static/ for you
```

## 📂 Project Structure

```
dairy_management/
├── config/            # Settings, root URLconf, WSGI/ASGI
├── core/              # Shared form helpers, template filters, seed command
├── accounts/          # Login / registration / farm profile
├── herd/              # Animals, breeds, movements, history
├── milk/              # Milk production, lactation, quality, yield targets
├── breeding/          # Heat, AI, pregnancy, calving
├── health/            # Vet visits, vaccination, treatment, medicine
├── feed/              # Feed items, consumption, purchases, cost
├── inventory/         # Stock items and movements
├── sales/  purchases/ # Customers/sales and suppliers/purchases
├── finance/           # Transactions and categories
├── employees/         # Staff, salaries, advances
├── reports/           # Dashboard + printable reports
├── templates/         # base layout, sidebar menu, per-app pages
└── static/            # Tailwind build output + vendored HTMX
```

## 🔑 Demo Credentials

After running `seed_data`, the following account works (created automatically):

```
username: admin
password: admin123
```

The seed command populates a farm ("Green Valley Dairy") with ~18 animals, 21 days of milk
records, breeding / health / feed / sales / finance / employee data — enough to explore every
screen immediately.

## 🧪 Validation

```bash
python _smoke.py        # Hits every page, prints HTTP status for each
```

All 77 routes (dashboard + full CRUD + reports + admin) return `200 OK`.

---

## ☁️ Deploying to Render

The repo ships with a [Render Blueprint](render.yaml) so the entire stack — web service,
PostgreSQL database, environment variables and health checks — is provisioned automatically.

### Option A — One-click (recommended)

1. Push this project to your GitHub account.
2. Open the [Render dashboard](https://dashboard.render.com/) → **New → Blueprint**.
3. Select the `dairy_management` repository. Render reads `render.yaml` and creates:
   - a **web service** (gunicorn on Django),
   - a **free PostgreSQL database** (persistent — replaces the dev SQLite file),
   - a generated `DJANGO_SECRET_KEY`.
4. Click **Apply**. Migration runs automatically on first deploy.

### Option B — Manual

1. In Render: **New → Web Service**, connect the repo.
2. Build command:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```
3. Start command:
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```
4. Add a **PostgreSQL** database and set its `internal connection string` to the
   `DATABASE_URL` env var.
5. Set env vars: `DJANGO_SECRET_KEY` (long random string), `DJANGO_DEBUG=0`,
   `DJANGO_ALLOWED_HOSTS=.onrender.com`, `PYTHON_VERSION=3.14.7`.
6. In **Settings → Health Check Path** enter `/ok` and save.

> **Static files** are served by WhiteNoise after the build runs `collectstatic`.
> **Database migrations** are handled by the Django `release` phase — run
> `python manage.py migrate` once. To populate demo data on Render, run
> `python manage.py seed_data` from the Render shell (optional).

The app is live at `https://<service-name>.onrender.com` — open it and log in with the
admin credentials you created (`python manage.py createsuperuser`), or the seeded
`admin` / `admin123` demo account.