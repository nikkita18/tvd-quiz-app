# 🚀 Deployment Guide: GitHub & Vercel

Follow these simple steps to push your project to GitHub and deploy it live on Vercel.

---

## Part 1: Push Project to GitHub

### Step 1: Initialize Git & Commit Files

Open your terminal in the project directory:

```bash
# 1. Initialize git
git init

# 2. Add all files (secrets in .env & gmailpass.txt are automatically ignored by .gitignore)
git add .

# 3. Commit your changes
git commit -m "Initial release of Mystic Falls TVD Quiz App"
```

### Step 2: Create a GitHub Repository & Push

1. Go to [GitHub.com](https://github.com) and click **New Repository**.
2. Name your repository (e.g., `tvd-quiz-app`).
3. Keep it Public or Private, and do **not** initialize with README or .gitignore (we already have them).
4. Run the following commands:

```bash
# Rename default branch to main
git branch -M main

# Link remote repository (replace with your actual GitHub URL)
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git

# Push code to GitHub
git push -u origin main
```

---

## Part 2: Cloud Database Setup (Required for Vercel)

> ⚠️ **Important Note**: Vercel runs in the cloud (serverless), so it cannot connect to your local `localhost:3306` MySQL. You will need a free cloud MySQL instance.

### Recommended Free Cloud MySQL Providers:
1. **[TiDB Serverless (Free Forever)](https://tidbcloud.com/)** *(Recommended — 5GB free, instant setup)*
2. **[Aiven for MySQL (Free Tier)](https://aiven.io/)**
3. **[Railway (Free Trial / Hobby)](https://railway.app/)**
4. **[Clever Cloud MySQL](https://www.clever-cloud.com/)**

### Steps to Initialize Cloud Database:
1. Create a database instance on your chosen provider (e.g. TiDB Cloud).
2. Copy the connection details: **Host**, **Port**, **User**, **Password**, and **Database Name**.
3. Open a SQL query console in your cloud provider and run the contents of [`schema.sql`](file:///c:/Users/HP/OneDrive/Desktop/app/App/schema.sql).
4. Run the seeder locally against your cloud DB to populate questions:
   ```bash
   # Temporarily set your cloud DB variables in .env, then run:
   python seed_questions.py
   ```

---

## Part 3: Deploy on Vercel

### Step 1: Import Project to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard) and log in with GitHub.
2. Click **Add New...** -> **Project**.
3. Select your GitHub repository (`tvd-quiz-app`) and click **Import**.

### Step 2: Configure Environment Variables

In the **Environment Variables** section on Vercel before clicking Deploy, add the following key-value pairs:

| Variable | Value | Description |
| :--- | :--- | :--- |
| `DB_HOST` | `gateway01.your-cloud-db.com` | Your Cloud MySQL Host |
| `DB_PORT` | `4000` or `3306` | Cloud MySQL Port |
| `DB_USER` | `your_cloud_user` | Cloud MySQL User |
| `DB_PASSWORD` | `your_cloud_password` | Cloud MySQL Password |
| `DB_NAME` | `b12_app` | Cloud Database Name |
| `DB_SSL` | `true` | Set to `true` for cloud DBs (TiDB, Aiven, etc.) |
| `SECRET_KEY` | `random-secure-32-char-string` | Secret key for Flask sessions |
| `MAIL_SERVER` | `smtp.gmail.com` | SMTP server for OTP emails |
| `MAIL_PORT` | `587` | SMTP Port |
| `MAIL_USE_TLS` | `true` | Use TLS |
| `MAIL_USERNAME` | `your_email@gmail.com` | Gmail address |
| `MAIL_PASSWORD` | `your_16_char_app_password` | Google 16-character App Password |

### Step 3: Deploy

1. Click **Deploy**.
2. Vercel will install dependencies from `requirements.txt`, configure `@vercel/python`, and serve your app.
3. Once finished, you will receive a live URL (e.g., `https://tvd-quiz-app.vercel.app`).
