# 🚀 StudyStack - Deployment Guide

This guide covers deploying StudyStack to **Render, Heroku, or your own server**.

---

## 📋 Prerequisites

- GitHub account (for version control)
- Hosting platform account (Render, Heroku, AWS, etc.)
- PostgreSQL database (for production)
- GROQ API key (for AI features)
- Python 3.11+

---

## 🔧 Local Setup

### 1. Clone & Setup

```bash
git clone https://github.com/varun05126/StudyStack.git
cd StudyStack

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env with your values
nano .env
```

**Required variables:**
```
DJANGO_SECRET_KEY=<generate-with-command-below>
DJANGO_DEBUG=false
GROQ_API_KEY=<your-groq-api-key>
```

Generate a secret key:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. Migrate Database

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://localhost:8000

---

## 🎯 Deployment to Render.com

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Initial StudyStack deployment"
git push origin main
```

### Step 2: Create on Render

1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub repository
4. Fill in details:
   - **Name:** `studystack`
   - **Region:** Choose closest to users
   - **Runtime:** `Python 3.11`
   - **Build Command:** 
     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command:** 
     ```bash
     gunicorn config.wsgi:application
     ```

### Step 3: Add Environment Variables

In Render dashboard → Environment:

```
DJANGO_SECRET_KEY=<your-key>
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=postgresql://...  # PostgreSQL connection URL
GROQ_API_KEY=<your-groq-key>
GITHUB_CLIENT_ID=<optional>
GITHUB_CLIENT_SECRET=<optional>
```

### Step 4: Add PostgreSQL Database

1. In Render dashboard → **Create New** → **PostgreSQL**
2. Use the provided `DATABASE_URL`
3. Add to environment variables

### Step 5: Deploy

1. Click **"Deploy"**
2. Wait for build to complete
3. Visit your app URL
4. Create superuser (one-time):
   ```bash
   render logs  # From CLI
   # Then SSH into container and run:
   python manage.py createsuperuser
   ```

---

## 🌐 Deployment to Heroku

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or download from heroku.com/cli
```

### Step 2: Create Heroku App

```bash
heroku login
heroku create your-studystack-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev
```

### Step 3: Set Environment Variables

```bash
heroku config:set DJANGO_SECRET_KEY=<your-key>
heroku config:set DJANGO_DEBUG=false
heroku config:set GROQ_API_KEY=<your-groq-key>
```

### Step 4: Deploy

```bash
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

---

## 🖥️ Self-Hosted Deployment (Ubuntu/Debian)

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3.11-dev \
  postgresql postgresql-contrib nginx supervisor git

# Create app user
sudo useradd -m studystack
sudo -u studystack git clone <your-repo> /home/studystack/app
```

### Step 2: Python Environment

```bash
cd /home/studystack/app
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy and edit .env
cp .env.example .env
nano .env

# Set permissions
sudo chown -R studystack:studystack /home/studystack/app
```

### Step 4: Gunicorn Setup

Create `/home/studystack/app/gunicorn_config.py`:

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
```

### Step 5: Supervisor Configuration

Create `/etc/supervisor/conf.d/studystack.conf`:

```ini
[program:studystack]
directory=/home/studystack/app
command=/home/studystack/app/venv/bin/gunicorn -c gunicorn_config.py config.wsgi:application
user=studystack
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile=/var/log/studystack/gunicorn.log
stderr_logfile=/var/log/studystack/gunicorn-error.log
```

### Step 6: Nginx Configuration

Create `/etc/nginx/sites-available/studystack`:

```nginx
upstream studystack {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    client_max_body_size 20M;

    location /static/ {
        alias /home/studystack/app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/studystack/app/media/;
    }

    location / {
        proxy_pass http://studystack;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 30s;
        proxy_connect_timeout 30s;
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/studystack /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx supervisor
```

### Step 7: SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
sudo systemctl restart nginx
```

---

## 🔒 Security Checklist

- [ ] Change `DJANGO_SECRET_KEY`
- [ ] Set `DJANGO_DEBUG=false`
- [ ] Configure `ALLOWED_HOSTS` correctly
- [ ] Use HTTPS only (SSL certificate)
- [ ] Rotate API keys regularly
- [ ] Enable CSRF protection
- [ ] Setup database backups
- [ ] Monitor application logs
- [ ] Implement rate limiting
- [ ] Setup password reset emails

---

## 📊 Monitoring & Maintenance

### Check Logs

**Render:**
```bash
render logs -s web
```

**Heroku:**
```bash
heroku logs --tail
```

**Self-hosted:**
```bash
tail -f /var/log/studystack/gunicorn.log
```

### Database Backups

**PostgreSQL:**
```bash
pg_dump -U postgres studystack > backup.sql
```

### Update Dependencies

```bash
pip list --outdated
pip install --upgrade <package>
```

---

## 🆘 Troubleshooting

### 500 Internal Server Error

1. Check logs
2. Verify `DJANGO_SECRET_KEY` is set
3. Run migrations: `python manage.py migrate`
4. Check database connection

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

### Database Connection Issues

- Verify `DATABASE_URL` format
- Check database credentials
- Ensure database server is running

### AI Features Not Working

- Verify `GROQ_API_KEY` is set
- Check API rate limits
- Review error logs

---

## 📞 Support

- **Issues:** GitHub Issues
- **Documentation:** README.md
- **Contributing:** CONTRIBUTING.md

Happy deploying! 🚀
