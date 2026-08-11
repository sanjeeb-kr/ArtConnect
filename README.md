# ArtConnect 🎨

**ArtConnect** is a full-stack creative marketplace web application built with Django, PostgreSQL, HTML5, and Tailwind CSS. It connects creative professionals (photographers, painters, musicians, dancers, poets, writers, actors, designers, illustrators) with clients looking for custom commissions and creative services.

---

## 🌟 Key Features

### For Artists 🎨
* **Custom Profile Management**: Set your primary discipline, experience years, bio statement, location, and profile picture.
* **Portfolio Showcase**: Upload sample artwork and portfolio posts with titles, descriptions, categories, and optional artwork pricing.
* **Services & Pricing**: Define custom service packages (e.g. Wedding Photography, Custom Portrait) with rates and pricing notes.
* **Request Management**: Receive client commission requests with event details, dates, and budgets. Manage work status across **Pending**, **Accepted (Upcoming Work)**, **In Progress**, and **Completed Work**.
* **Earnings Logging**: Automatic calculation and aggregation of total earnings from completed commission requests.

### For Clients 💼
* **Artist Discovery & Search**: Filter creative professionals by discipline category, location, or search keywords (matching name or bio).
* **Public Artist Profiles**: View artist portfolio galleries, service rates, and overall ratings.
* **Commission Request System**: Send detailed commission requests with event titles, dates, locations, and proposed budgets.
* **Ratings & Reviews**: Rate completed work on a 1 to 5-star scale and leave public reviews.

### Security & Architecture 🔐
* **Custom User Architecture**: Single custom `User` model (`AUTH_USER_MODEL = 'accounts.User'`) configured before initial migration with role selection (`ARTIST` / `CLIENT`).
* **Strict Authorization**: Server-side view permission checks ensuring users can only edit or delete their own profiles, posts, services, or requests.
* **Anti-Duplication Safeguards**: Unique database constraints on post likes and single-review enforcement per completed request.

---

## 🛠️ Technology Stack

* **Backend**: Python 3, Django 5
* **Database**: PostgreSQL
* **Frontend**: Server-rendered Django Templates + HTML5 + Tailwind CSS
* **Static Assets**: WhiteNoise (`CompressedManifestStaticFilesStorage`)
* **Media Storage**: Local storage in development, production-ready for Cloudinary (`django-cloudinary-storage`)
* **Server**: Gunicorn (WSGI)

---

## 🚀 Local Development Setup

### 1. Prerequisites
* **Python 3.10+**
* **PostgreSQL 18** (running locally on port 5432)

### 2. Create Database
Ensure the `artconnect` database exists on your local PostgreSQL server:
```sql
CREATE DATABASE artconnect;
```

### 3. Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/your-username/artconnect.git
cd artconnect

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Create a `.env` file in the project root directory with the following variables:

```env
# Django Configuration
SECRET_KEY="django-insecure-artconnect-local-dev-key"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Local PostgreSQL Credentials
DB_NAME=artconnect
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

# Cloudinary Storage Credentials (Leave blank for local media storage)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

### 6. Run Migrations & Seed Categories
```bash
# Apply migrations to PostgreSQL
python manage.py migrate

# Seed default artist disciplines
python -c "import django, os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); django.setup(); from artists.models import ArtistType; types = ['Photographer', 'Painter', 'Musician', 'Singer', 'Dancer', 'Poet', 'Writer', 'Actor', 'Designer', 'Illustrator', 'Other']; [ArtistType.objects.get_or_create(name=t) for t in types]"
```

### 7. Run Local Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser.

---

## 🧪 Running Automated Tests

Run the full Django test suite covering registration, authorization checks, portfolio CRUD, artist discovery, request workflows, likes, and reviews:

```bash
python manage.py test
```

---

## ☁️ Deployment Guide (Render)

When ready to deploy to Render:

1. **Create Web Service on Render** connected to your GitHub repository.
2. **Environment**: Python 3.x
3. **Build Command**:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
4. **Start Command**:
   ```bash
   gunicorn config.wsgi:application
   ```
5. **Add Environment Variables in Render Dashboard**:
   - `SECRET_KEY`: *(Generate a secure random key)*
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `DB_NAME`: *(Render PostgreSQL DB Name)*
   - `DB_USER`: *(Render PostgreSQL User)*
   - `DB_PASSWORD`: *(Render PostgreSQL Password)*
   - `DB_HOST`: *(Render PostgreSQL Hostname)*
   - `DB_PORT`: `5432`
   - `CLOUDINARY_CLOUD_NAME`: *(Your Cloudinary Cloud Name)*
   - `CLOUDINARY_API_KEY`: *(Your Cloudinary API Key)*
   - `CLOUDINARY_API_SECRET`: *(Your Cloudinary API Secret)*
