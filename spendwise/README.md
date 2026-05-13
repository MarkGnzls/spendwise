# SpendWise

SpendWise is a lightweight expense monitoring web application built with Flask and PostgreSQL, optimized for deployment on Render's free plan. It provides modern financial dashboards, transaction tracking, analytics, and a clean, responsive interface.

## Features

- User registration and login
- Password hashing and secure sessions
- Expense and income tracking
- Category-based spending analytics
- Responsive dashboard with interactive Chart.js charts
- Dark/light mode toggle with localStorage persistence
- Clean modern UI optimized for mobile and desktop

## Project Structure

```plaintext
spendwise/
├── app/
│   ├── static/
│   ├── templates/
│   ├── routes/
│   ├── models/
│   └── __init__.py
├── config.py
├── run.py
├── requirements.txt
├── Procfile
├── render.yaml
└── README.md
```

## Setup

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create environment variables (optional):

Create a `.env` file in the project root:

```env
SECRET_KEY=super-secret-key
DATABASE_URL=postgresql://username:password@host:port/dbname
```

**Note:** If `DATABASE_URL` is not set, the app will use **SQLite** for local development. To use PostgreSQL, set the `DATABASE_URL` environment variable.

4. Run the app:

```bash
python run.py
```

The app starts on `http://localhost:5000`. Database tables are created automatically on first run. Log in or create a new account.

### (Optional) Manual database initialization

If you need to manually create tables, run:

```bash
python init_db.py
```

## Render Deployment

1. Create a new Web Service on Render and connect your Git repository.
2. Set the build command:

```bash
pip install -r requirements.txt && python init_db.py
```

3. Set the start command:

```bash
gunicorn run:app
```

4. Add environment variables in Render settings:

- `SECRET_KEY` — a strong secret key
- `DATABASE_URL` — your Render PostgreSQL connection string (e.g., `postgresql://user:password@host/dbname`)

5. Create a PostgreSQL database on Render and link it via the `DATABASE_URL` variable.

Once deployed, your app will automatically use PostgreSQL instead of SQLite.

## Notes

- **Local Development:** Uses SQLite by default for quick testing without PostgreSQL.
- **Production (Render):** Uses PostgreSQL when `DATABASE_URL` is set.
- Keep `SECRET_KEY` and database credentials secure.
- The app follows Flask best practices and is beginner-friendly.
- To use PostgreSQL locally, set `DATABASE_URL` in your `.env` file.
