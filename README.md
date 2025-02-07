# Task & Habit Tracker

A lightweight web application (built with **FastAPI** and **SQLAlchemy**) for creating tasks, setting recurring reminders, and visualizing daily or weekly progress. It provides basic analytics (e.g., DAU, tasks completed per day, user retention) and a simple referral system to invite friends.

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Architecture](#architecture)  
5. [Getting Started](#getting-started)  
    - [Prerequisites](#prerequisites)  
    - [Installation & Setup](#installation--setup)  
6. [Running the Application](#running-the-application)  
7. [Testing the Application](#testing-the-application)  
8. [Endpoints & User Flow](#endpoints--user-flow)  
9. [Live Demo (Optional)](#live-demo-optional)  
10. [Deployment & Hosting](#deployment--hosting)
11. [Local Setup & Usage](#local-setup--usage)
12. [Monitoring & Logging](#monitoring--logging)
13. [Future Roadmap](#future-roadmap)  
14. [License](#license)  

---

## Overview

**Task & Habit Tracker** is designed to help users manage their daily or weekly tasks and habits. Users can:

- **Register** an account
- **Create tasks** with optional descriptions
- **Mark tasks as completed**
- **Generate referrals** for friends
- View **basic analytics** on usage, tasks completed per day, and user retention

This repository demonstrates a **production-ready project structure** using FastAPI, complete with:

- **Database integration** (SQLite by default)
- **API documentation** via `/docs` (Swagger UI)
- **Logging and basic monitoring**
- **Automated testing** with `pytest`

---

## Features

- **User Management:**  
  - Register, log in, and log out.
  - Secure password storage using Passlib (passwords are hashed).
  
- **Task Management:**  
  - Create, view, and complete tasks.
  - Dashboard view for user tasks.
  
- **Admin Monitoring:**  
  - Restricted admin dashboard (requires an admin key) displaying dummy analytics.
  
- **Responsive UI/UX:**  
  - Retro, notebook-style interface with a simple, mobile-friendly design.
  
- **Deployment & Monitoring:**  
  - Hosted on Render with CI/CD via GitHub Actions.
  - Basic logging integrated for monitoring application health.

- **Mobile Client:**  
  - A minimal Kivy client available for Android, iOS, and desktop packaging.

---

## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** SQLite (default; can be replaced with PostgreSQL, etc.)
- **ORM:** SQLAlchemy
- **Templating:** Jinja2
- **Password Hashing:** Passlib
- **CI/CD:** GitHub Actions
- **Hosting:** Render (free tier)
- **Monitoring & Logging:** Python's built-in logging (viewable via Render dashboard)
- **Language**: Python
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database**: SQLite (swappable for Postgres, MySQL, etc. by changing `DB_URL` in `.env`)
- **Testing**: [pytest](https://pytest.org/)
- **Environment Management**: [python-dotenv](https://pypi.org/project/python-dotenv/)
- **PWA & Offline:** Service Worker, Manifest, localForage (JavaScript)
- **IPFS Integration:** ipfshttpclient (Python)
- **Mobile Client:** Kivy
- **Testing:** pytest, Selenium (for responsiveness)

---

## Architecture

A high-level view of the application architecture:

``` bash

 ┌─────────────┐
 │   Clients    │
 └──────┬───────┘
        │  (HTTP Requests)
 ┌───────────────┐
 │   FastAPI      │
 │ (application)  │
 └──────┬─────────┘
  (SQLAlchemy ORM)
 ┌───────────────┐
 │   Database     │
 │ (SQLite)       │
 └───────────────┘
```

- **application/**: Contains all business logic (routes, models, schemas, utility functions).
- **infrastructure/**: Database connections (SQLAlchemy engine, session management).
- **monitoring/**: Basic logging setup (logging config).
- **tests/**: `pytest` test suite.
- **manage.py**: Simple CLI to **run** or **test** the application.

---

## Getting Started

### Prerequisites

- **Python 3.8+** installed
- (Optional) **Virtual Environment** (recommended)

### Installation & Setup

1. **Clone** or download this repository:

   ```bash
   git clone https://github.com/your-username/task_habit_tracker.git
   cd task_habit_tracker
   ```

2. (Optional) **Create and activate** a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # or "venv\Scripts\activate" on Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure** the `.env` file (found at the root of the project). By default:

   ```bash
   DB_URL=sqlite:///./tracker.db
   SECRET_KEY=mysecretkey
   ```

   - If you want to use Postgres or MySQL, change `DB_URL` accordingly (e.g., `postgresql://user:pass@localhost:5432/dbname`).

> **Note**: This project automatically creates all tables in the database (e.g., `tracker.db`) on startup. In production, you’d typically use migrations (Alembic or similar).

---

## Running the Application

After installation:

```bash
# Start the server
python manage.py run
```

- By default, the app listens on `http://0.0.0.0:8000`.
- Visit **[http://localhost:8000/docs](http://localhost:8000/docs)** for the interactive API documentation (Swagger UI).
- If you navigate to `http://localhost:8000/` in your browser, you’ll see a simple welcome message.

---

## Testing the Application

To run the automated tests (via pytest):

```bash
python manage.py test
```

- This will look for tests inside the `tests/` folder.
- If everything is set up correctly, you should see a successful test run.

---

## Endpoints & User Flow

Here is a typical **user flow**:

1. **Sign Up**
   - `POST /users` with JSON body:

     ```json

     {
       "email": "user@example.com",
       "password": "password123"
     }
     ```

   - Returns a new user object with `id` and `created_at`.

2. **View User Info**
   - `GET /users/{user_id}`
   - Returns user data.

3. **Create a Task**
   - `POST /users/{user_id}/tasks` with JSON body:

     ```json
     {
       "title": "My Task",
       "description": "Some details about the task."
     }
     
     ```

   - Returns the created task object.

4. **View Tasks**
   - `GET /users/{user_id}/tasks`
   - Returns a list of all tasks for that user.

5. **Complete a Task**
   - `PATCH /tasks/{task_id}`
   - Marks the task as completed.

6. **Analytics**
   - `GET /analytics/dau` => Returns a dummy DAU metric.
   - `GET /analytics/tasks_per_day` => Returns a dummy tasks completed per day metric.
   - `GET /analytics/retention` => Returns a dummy 4-week retention metric.

7. **Generate Referral Link**
   - `GET /referral/{user_id}` => Returns a referral URL for the given user.

---

## Live Demo (Optional)

If you decide to deploy this on a free platform (e.g., Render, Fly.io, Railway, or Deta Space), you can link your repository and set up environment variables accordingly. Then you can add a link here for others to try your app:

- **Live App URL**: [https://my-task-habit-tracker.onrender.com](https://my-task-habit-tracker.onrender.com) (Example)

> Please note that the exact deployment steps vary based on the hosting platform. Typically, you need to:
> 1.Connect your GitHub repository
> 2. Set environment variables (like `DB_URL`, `SECRET_KEY`) in the hosting dashboard.
> 3. Provide a start command, e.g., `uvicorn application.main:app --host 0.0.0.0 --port 8000`.

---

## Deployment & Hosting

### Hosted on Render

The application is deployed on Render. To deploy your own instance:

1. **Push the Code to GitHub/GitLab:**  
   Ensure your project (including all source code, templates, and configuration files) is hosted on a Git repository.

2. **Set Up GitHub Actions:**  
   The repository includes a CI/CD workflow in `.github/workflows/ci.yml` that runs tests on every push to the `main` branch.

3. **Create a New Web Service on Render:**
   - Sign up/log in to [Render](https://render.com/).
   - Click on **"New"** and select **"Web Service"**.
   - Connect your repository and select the appropriate branch (typically `main`).
   - **Build Command:**

     ```bash

     pip install -r requirements.txt

     ```

   - **Start Command:**  

     ```bash

     uvicorn application.main:app --host 0.0.0.0 --port 8000

     ```

   - **Environment Variables:**  
     Configure the following variables in Render's dashboard (matching your local `.env`):
     - `DB_URL`
     - `SECRET_KEY`
     - `ADMIN_KEY`
  
4. **Accessing the Live Application:**  
   Once deployed, Render will assign you a URL (for example, `https://your-task-habit-tracker.onrender.com`). Use this URL to access the live app.

---

See [deployment.md](deployment.md) for a detailed deployment guide covering:

- Deploying the web app on Render
- Packaging the mobile client for Android (using Buildozer), iOS (using Kivy-ios), and desktop (using PyInstaller)
- IPFS integration requirements

---

## Mobile Client

A Kivy-based mobile client is included in the `mobile/` directory. To run locally:

1. Navigate to the mobile directory:
   bash
   cd mobile
   python main.py

2. For Android, build the APK using Buildozer:

   bash
   buildozer -v android debug

3. For desktop, package the app using PyInstaller:

   bash
   pyinstaller --onefile main.py

Refer to the [deployment.md](deployment.md) for detailed packaging instructions.

---

## Local Setup & Usage

### Prerequisites\

- Python 3.9+
- Git

### Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/task_habit_tracker.git
   cd task_habit_tracker
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**  
   Create a `.env` file in the root directory with the following (example):

   ```ini
   DB_URL=sqlite:///./tracker.db
   SECRET_KEY=mysecretkey
   ADMIN_KEY=supersecretadminkey
   ```

5. **Run Tests:**

   ```bash
   python manage.py test
   ```

6. **Start the Application:**

   ```bash
   python manage.py run
   ```

   Open your browser and navigate to [http://localhost:8000](http://localhost:8000).

---

## Testing

Comprehensive tests cover:

- **Web API & PWA:** Using pytest for endpoints, manifest, service worker, and offline sync.
- **Responsive UI:** Selenium tests simulate different screen sizes.
- **IPFS Integration:** Tests to ensure task data is stored on IPFS.
- **Mobile Client:** Manual testing guidelines and packaging instructions.
  
See [testing.md](testing.md) for complete details and commands to run the tests.

## Monitoring & Logging

- **Logging:**  
  The application uses Python’s built-in logging (configured in `monitoring/logging_config.py`). Logs are printed to the console and can be viewed in the Render dashboard.

- **Basic Admin Monitoring:**  
  An admin dashboard is available at `/admin?admin_key=supersecretadminkey` (replace with your admin key). This dashboard shows dummy analytics (e.g., DAU, tasks per day, 4-week retention).

---

## Future Roadmap

For detailed future enhancements, see the [FUTURE_PLAN.md](FUTURE_PLAN.md) file. Upcoming phases include:

- Enhanced UI/UX and offline capabilities (PWA support).
- Rich list management and collaborative features.
- AI/ML-driven task organization and recommendations.
- Advanced scheduling, calendar integrations, and task dependencies.
- Gamification, social integration, and advanced behavioral analytics.
- Enterprise-level integrations and a plugin ecosystem.

---

## License

This project is under the [MIT License](https://opensource.org/licenses/MIT). Feel free to fork or copy for personal or commercial use.

> **Disclaimer**: This is a sample reference application. For **production use**, remember to:
> -Implement secure password hashing and authentication
> -Use a robust database migration strategy
> -Add proper monitoring and error handling

---

**Thank you for checking out the Task & Habit Tracker!**
