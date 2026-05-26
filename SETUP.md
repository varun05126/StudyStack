# 👨‍💻 StudyStack - Developer Setup Guide

Complete guide to get StudyStack running locally for development.

---

## 🎯 What You'll Get

- Django development server running on localhost
- SQLite database (no external setup needed)
- AI features using GROQ API
- Static files served via WhiteNoise
- Admin panel at `/admin`

---

## ✅ Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/)
- **GitHub Account** - For pulling the repo
- **~500MB disk space** - For dependencies
- **GROQ API key** (optional) - For AI features

---

## 📥 Step 1: Clone the Repository

```bash
# Clone the repo
git clone https://github.com/varun05126/StudyStack.git
cd StudyStack

# Verify you're in the right directory
ls  # Should see manage.py, config/, core/, etc.
```

---

## 🔧 Step 2: Create Virtual Environment

A virtual environment isolates project dependencies from your system.

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# You should see (venv) in your terminal prompt
```

---

## 📦 Step 3: Install Dependencies

```bash
# Upgrade pip (recommended)
pip install --upgrade pip

# Install production dependencies
pip install -r requirements.txt

# (Optional) Install development tools
pip install -r requirements-dev.txt
```

---

## 🌍 Step 4: Configure Environment Variables

```bash
# Copy the template
cp .env.example .env

# Edit the .env file
# On macOS/Linux:
nano .env

# On Windows:
notepad .env

# Required changes:
# 1. DJANGO_SECRET_KEY - Uncomment and generate one:
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# 2. DJANGO_DEBUG=true (for development)

# 3. GROQ_API_KEY (optional, for AI features)
#    Get one free from: https://console.groq.com
```

**Your `.env` should look like:**

```env
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
GROQ_API_KEY=gsk_...  # (optional)
```

---

## 🗄️ Step 5: Setup Database

```bash
# Apply migrations (creates SQLite database)
python manage.py migrate

# Create an admin user
python manage.py createsuperuser
# Follow prompts:
# Username: admin
# Email: your@email.com
# Password: (enter a password)

# (Optional) Load sample data
python manage.py loaddata sample_data  # If available

# Verify database was created
ls  # Should see db.sqlite3
```

---

## 🚀 Step 6: Run the Development Server

```bash
# Start Django development server
python manage.py runserver

# You should see:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

---

## 🌐 Step 7: Access the Application

Open your browser and visit:

| URL | Purpose |
|-----|---------|
| `http://localhost:8000` | Main application |
| `http://localhost:8000/login` | Login page |
| `http://localhost:8000/dashboard` | Dashboard (requires login) |
| `http://localhost:8000/admin` | Django admin panel |

**Admin credentials:** Use the superuser you created in Step 5

---

## 🧪 Common Development Tasks

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core

# Run specific test file
pytest core/tests.py
```

### Format Code (Black)

```bash
black core/ config/
```

### Check Code Quality

```bash
# Lint
flake8 core/ config/

# Type checking
mypy core/ config/
```

### Create a Superuser (if you forgot)

```bash
python manage.py createsuperuser
```

### Reset Database (WARNING: Deletes all data)

```bash
# Delete the database file
rm db.sqlite3

# Recreate it
python manage.py migrate
python manage.py createsuperuser
```

### Create Migrations (after model changes)

```bash
# Create migration file
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

---

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'django'

**Solution:** Make sure virtual environment is activated
```bash
# Check if (venv) appears in your terminal
# If not, run:
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate.bat  # Windows
```

### django.core.exceptions.ImproperlyConfigured: settings.DATABASES is improperly configured

**Solution:** Your `.env` file is missing or `DJANGO_SECRET_KEY` is not set
```bash
cp .env.example .env
# Edit .env and add DJANGO_SECRET_KEY
```

### Port 8000 already in use

**Solution:** Use a different port
```bash
python manage.py runserver 8001
```

### Database locked error

**Solution:** Delete the database and recreate it
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static files not loading (404 errors)

**Solution:** Collect static files
```bash
python manage.py collectstatic --noinput
```

### GROQ API not working

**Solution:** Verify your API key
1. Go to https://console.groq.com
2. Create API key if you don't have one
3. Add to `.env`: `GROQ_API_KEY=gsk_...`
4. Restart development server

---

## 📁 Project Structure

```
StudyStack/
├── config/              # Django project configuration
│   ├── settings.py      # Configuration file
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI server config
│   └── asgi.py          # ASGI server config
│
├── core/                # Main Django app
│   ├── models.py        # Database models
│   ├── views.py         # Views/Controllers
│   ├── forms.py         # Django forms
│   ├── urls.py          # App URL routing
│   ├── admin.py         # Admin panel config
│   └── services/        # Business logic
│       ├── groq.py      # AI service
│       ├── github.py    # GitHub sync
│       └── ...
│
├── templates/           # HTML templates
│   └── core/
│       ├── base.html
│       ├── dashboard.html
│       └── ...
│
├── static/              # CSS, JS, images
│   └── core/
│       ├── style.css
│       └── ...
│
├── manage.py            # Django management script
├── requirements.txt     # Dependencies
├── requirements-dev.txt # Dev dependencies
├── .env.example         # Environment template
├── README.md            # Project documentation
├── DEPLOYMENT.md        # Deployment guide
└── db.sqlite3          # SQLite database (created after migration)
```

---

## 🎨 Making Changes

### Add a new feature

1. **Create a model** (core/models.py)
   ```python
   class MyModel(models.Model):
       name = models.CharField(max_length=100)
   ```

2. **Create migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create a view** (core/views.py)
4. **Add template** (templates/core/my_template.html)
5. **Add URL** (core/urls.py)
6. **Register in admin** (core/admin.py)

### Git Workflow

```bash
# See your changes
git status

# Stage changes
git add .

# Commit
git commit -m "Add new feature: description"

# Push to GitHub
git push origin main
```

---

## 📚 Learning Resources

- **Django Docs:** https://docs.djangoproject.com/
- **Django Tutorial:** https://www.djangoproject.com/start/
- **Python:** https://python.readthedocs.io/
- **PostgreSQL (for production):** https://www.postgresql.org/docs/

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/my-feature
   ```
3. Make changes and test locally
4. Commit and push
   ```bash
   git commit -m "Add feature"
   git push origin feature/my-feature
   ```
5. Create a Pull Request on GitHub

---

## 📞 Need Help?

- **GitHub Issues:** [Open an issue](https://github.com/varun05126/StudyStack/issues)
- **Documentation:** Check README.md
- **Django Docs:** https://docs.djangoproject.com/

Happy coding! 🎉
