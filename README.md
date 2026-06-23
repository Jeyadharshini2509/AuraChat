# Aura — ChatGPT-style Chat App

A ChatGPT-style app built with Django + Groq (Llama 3.3 70B).
Features: signup/login, persistent chat threads, full message history, continue old chats, markdown rendering, dark theme UI.

## Project layout

```
chatapp/
  manage.py
  chatapp/          <- project settings, urls, wsgi
  chat/             <- models, views, templates, static files, Groq client
  requirements.txt
  .env.example
  Procfile          <- tells Render/Railway how to start the app
  runtime.txt       <- Python version for deployment
```

## How the features map to code

| Feature | Where |
|---|---|
| Signup / login / logout | `chat/views.py` (signup) + Django's built-in auth views in `chatapp/urls.py` |
| Chat threads | `ChatThread` model in `chat/models.py` |
| Message history | `Message` model in `chat/models.py`, linked to a thread |
| Continue a chat | `chat_thread` view loads all messages for that thread from the DB |
| New chat | First message with no `thread_id` creates a new `ChatThread` |
| Calling Groq (Llama) | `chat/groq_client.py` |
| Markdown rendering | `chat/templatetags/chat_filters.py` — server-side using Python `markdown` library |
| Sidebar / UI | `chat/templates/chat/chat.html` + `chat/static/chat/style.css` |

## SQLite vs Postgres

The project uses both automatically depending on environment:
- No `DATABASE_URL` set → uses `db.sqlite3` locally (fine for development)
- `DATABASE_URL` set → uses Postgres (used in production on Render/Railway)

No code changes needed to switch — just set the environment variable.

---

## Run it locally

### 1. Install Python 3.12+
Download from python.org. On Windows, tick "Add Python to PATH" during install.

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your .env file
```bash
# Mac/Linux
cp .env.example .env

# Windows
copy .env.example .env
```

Open `.env` and fill in your values:
```
GROQ_API_KEY=your-groq-key-from-console.groq.com
DJANGO_SECRET_KEY=any-long-random-string
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

Get a free Groq API key (no credit card) at **console.groq.com** → API Keys.

### 5. Set up the database
```bash
python manage.py migrate
```

### 6. Run the server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** — sign up, start chatting.
To stop: `Ctrl+C`. To run again later, just activate venv and run `runserver`.

---

## Deploy to Render (free tier)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Create a Web Service on Render
1. Go to **render.com** → sign in with GitHub
2. **New** → **Web Service** → connect your repo
3. Fill in:
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start command:** `gunicorn chatapp.wsgi`
   - **Instance type:** Free
4. Add environment variables:
   - `GROQ_API_KEY` = your Groq key
   - `DJANGO_SECRET_KEY` = any long random string
   - `DJANGO_DEBUG` = `False`
5. Click **Create Web Service**

### 3. Add a free Postgres database
1. Render dashboard → **New** → **PostgreSQL** → Free tier → Create
2. Copy the **Internal Database URL**
3. Go to your Web Service → **Environment** → add:
   - `DATABASE_URL` = the Internal Database URL you copied
4. Render redeploys automatically

### 4. Run migrations
In your Web Service → **Shell** tab:
```bash
python manage.py migrate
```

Your app is live at `https://yourapp.onrender.com`.

### Deploying future changes
```bash
git add .
git commit -m "describe what changed"
git push
```
Render auto-redeploys on every push. If you changed `models.py`, also run `python manage.py migrate` in the Render shell after deploy.

---
