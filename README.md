# 📘 StudyStack  
### Smart Study Planner & Learning Platform

<div align="center">
  <strong>Organized Planning • Productive Learning • Community Support</strong>
  <br/>
  <a href="https://github.com/varun05126/StudyStack"><img src="https://img.shields.io/badge/GitHub-StudyStack-blue?style=for-the-badge&logo=github"></a>
  <a href="#getting-started"><img src="https://img.shields.io/badge/Get%20Started-Now-brightgreen?style=for-the-badge"></a>
</div>

---

## 🎯 Vision

StudyStack is a comprehensive platform designed to help students **plan effectively**, **track progress**, and **learn smarter**. It combines task management, progress tracking, and AI-assisted learning into one unified ecosystem.

**From simple study planning to competitive programming tracking** — StudyStack has it all.

---

## ✨ Key Features

### 📋 Task & Study Management
- 📝 Create tasks with deadlines, difficulty levels, and time estimates
- ✅ Track completion and maintain study streaks
- 🎯 Multiple task types (assignments, projects, exams, revision)
- 📁 Upload study materials (PDF, DOCX, TXT)

### 🤖 AI-Powered Learning
- 💡 AI assistance for task help and solutions
- 🧠 Smart learning goals with generated resources
- 📚 Auto-populated resources and study guides
- 🔗 Curated content from multiple sources

### 👥 Competitive Programming Hub
- 🌟 GitHub profile integration (repos, commits, XP)
- 💻 LeetCode sync (problems solved, difficulty levels)
- 🏢 GeeksforGeeks tracking (DSA problems, XP)
- 🎯 CodeForces, HackerRank support
- 🏆 Global leaderboards and rankings

### 📊 Analytics & Progress
- 📈 Study heatmap and streaks
- 📉 Performance insights across platforms
- 🎖️ Achievement badges and levels
- 📅 Historical activity tracking

### 📚 Notes & Resources
- 📝 Create public/private notes and study materials
- 🔍 Discover notes shared by other students
- 🏷️ Organize by subjects and topics
- 💾 File-based storage and management

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 6.0, Python 3.11+ |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Database** | SQLite (dev), PostgreSQL (prod) |
| **Server** | Gunicorn, Nginx |
| **AI** | GROQ API |
| **Deployment** | Render, Heroku, Self-hosted |

---

## 🚀 Quick Start

### 🔗 Live Demo
**[View on Render](https://studystack-9k4x.onrender.com)** (Note: In development)

### 💻 Local Development (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/varun05126/StudyStack.git
cd StudyStack

# 2. Setup (see SETUP.md for detailed guide)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
cp .env.example .env      # Edit with your keys

# 3. Install & run
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Open browser: http://localhost:8000
```

**For detailed setup:** See **[SETUP.md](SETUP.md)**

---

## 📦 Deployment

### 🌐 Deploy to Render (Recommended)
1. Push to GitHub
2. Connect to Render
3. Set environment variables
4. Deploy! (See **[DEPLOYMENT.md](DEPLOYMENT.md)** for details)

### 🌐 Other Platforms
- **Heroku** - See DEPLOYMENT.md
- **AWS** - See DEPLOYMENT.md
- **Self-hosted** - See DEPLOYMENT.md

**Full deployment guide:** See **[DEPLOYMENT.md](DEPLOYMENT.md)**

---

## 📋 Project Structure

```
StudyStack/
├── config/              # Django settings & URL routing
├── core/                # Main app (models, views, forms)
│   └── services/        # Business logic (AI, syncing)
├── templates/           # HTML templates
├── static/              # CSS, JavaScript, images
├── SETUP.md            # Local development guide
├── DEPLOYMENT.md       # Production deployment guide
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```

---

## 🎓 How to Use

### 1. **Create Account & Login**
   - Sign up with email and password
   - Access your personalized dashboard

### 2. **Manage Your Studies**
   - Create tasks for assignments and exams
   - Set deadlines and time estimates
   - Upload study materials
   - Track completion with progress bar

### 3. **Get AI Help**
   - Ask AI for help on stuck tasks
   - Get study suggestions and resources
   - Create learning goals with auto-generated plans

### 4. **Connect Platforms**
   - Link GitHub, LeetCode, GFG, etc.
   - Auto-sync achievements and stats
   - View consolidated progress

### 5. **Share & Collaborate**
   - Upload notes for others to discover
   - Browse community study materials
   - Contribute to the learning ecosystem

---

## 🔧 Configuration

### Required Environment Variables

```env
DJANGO_SECRET_KEY=<your-secret-key>
DJANGO_DEBUG=false              # Set to true for development
GROQ_API_KEY=<your-groq-key>   # For AI features

# Optional: Platform integrations
GITHUB_CLIENT_ID=<optional>
GITHUB_CLIENT_SECRET=<optional>
```

See **[.env.example](.env.example)** for all available options.

---

## 📊 Current Status

✅ **Stable Features**
- User authentication (signup/login)
- Task management with deadlines
- Study progress tracking
- GitHub integration
- LeetCode & GFG sync
- AI-assisted learning

🚧 **In Development**
- Advanced analytics
- Mobile app
- Real-time collaboration
- Advanced filtering & search

---

## 🗺️ Roadmap

### Q1 2026
- [ ] React frontend rewrite
- [ ] Mobile app (iOS/Android)
- [ ] Advanced search & filtering
- [ ] Community features

### Q2 2026
- [ ] REST API (Django REST Framework)
- [ ] Real-time notifications
- [ ] Study groups & collaboration
- [ ] Gamification improvements

### Q3 2026
- [ ] Advanced analytics dashboard
- [ ] ML-based recommendations
- [ ] Integration with more platforms
- [ ] Offline mode

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/my-feature`)
3. **Make** your changes
4. **Test** locally
5. **Commit** with clear messages
6. **Push** and create a **Pull Request**

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for detailed guidelines.

---

## 📞 Support & Feedback

- 🐛 **Found a bug?** [Open an issue](https://github.com/varun05126/StudyStack/issues)
- 💡 **Have an idea?** [Start a discussion](https://github.com/varun05126/StudyStack/discussions)
- 📧 **Questions?** Check [SETUP.md](SETUP.md) or [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 About

**StudyStack** is developed by **Varun M**, B.Tech student at Vardhaman College of Engineering.

Passionate about building practical learning platforms that make a real difference.

---

## 🌟 Acknowledgments

- **GROQ** - For powerful AI API
- **Django** - For excellent web framework
- **GitHub** - For version control & OAuth
- **Community** - For feedback and contributions

---

<div align="center">
  <strong>Made with ❤️ for students, by students</strong>
  <br/>
  <a href="https://github.com/varun05126/StudyStack">⭐ Star us on GitHub</a>
</div>
