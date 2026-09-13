# 🦇 Mystic Falls — The Vampire Diaries Quiz App

A full-featured, interactive **The Vampire Diaries** themed web application built with Python Flask, MySQL, and modern gothic/vampire UI aesthetics.

---

## 🌟 Features

- 🩸 **Mystic Falls Lore & Characters**: Interactive character profiles with HD imagery and lore.
- 🎯 **Dynamic Quiz Engine**: 3 difficulty levels (Easy, Medium, Hard) with 10 questions per level.
- 🏆 **Live Scoreboard & Leaderboard**: Real-time scoring and ranking using SQL window functions.
- 🔐 **User Authentication**: Secure password hashing (SHA-256), email OTP verification via SMTP.
- 👑 **Admin Portal**: Dedicated dashboard to manage quiz questions and view registered users.
- ⚡ **Cloud & Serverless Ready**: Prepared for seamless deployment on Vercel and cloud MySQL (TiDB / Aiven / Railway / PlanetScale).

---

## 📁 Project Structure

```text
├── api/
│   └── index.py            # Vercel serverless function entrypoint
├── static/
│   ├── css/                # Custom styled CSS stylesheets
│   ├── img/                # Character & UI graphics
│   ├── js/                 # Client-side scripts
│   └── Salvatore.mp3       # Mystic soundtrack
├── templates/              # Jinja2 HTML templates
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules for secrets & cache
├── admin.py                # Admin database operations
├── app.py                  # Main Flask application & routing
├── db.py                   # Centralized database connection helper
├── encryption.py           # Password hashing & encryption
├── myEmail.py              # Flask-Mail OTP sender
├── requirements.txt        # Python package dependencies
├── schema.sql              # MySQL DDL schema script
├── seed_questions.py       # Quiz question seeder
├── user.py                 # User database operations
├── validation.py           # Form & input validation
└── vercel.json             # Vercel deployment configuration
```

---

## 🚀 Local Development Setup

### 1. Clone & Setup Environment

```bash
git clone <your-repo-url>
cd App

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your details:

```bash
cp .env.example .env
```

Edit `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=b12_app
DB_SSL=false
SECRET_KEY=your_secret_key_here
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

### 3. Setup Database & Seed Questions

Run MySQL locally and initialize the database:

```bash
# Option A: Import schema.sql into your MySQL instance
mysql -u root -p < schema.sql

# Option B: Run the seeder (creates questions)
python seed_questions.py
```

### 4. Run the Flask App

```bash
python app.py
```
Open your browser at `http://localhost:5001`.

---

## ☁️ Deploying to Vercel

See [DEPLOYMENT.md](file:///c:/Users/HP/OneDrive/Desktop/app/App/DEPLOYMENT.md) for step-by-step instructions on setting up a free cloud MySQL database and deploying to Vercel.
