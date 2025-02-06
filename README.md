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
10. [Future Roadmap](#future-roadmap)  
11. [License](#license)  

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

1. **User Registration**: Create new users and store credentials (currently stored in plain text — can be easily replaced with password hashing).
2. **Task Management**:
   - Create tasks for each user
   - Retrieve tasks for each user
   - Mark tasks as completed
3. **Basic Analytics**:
   - Daily Active Users (DAU) (dummy example)
   - Tasks completed per day (dummy example)
   - 4-week user retention (dummy example)
4. **Referral Links**:
   - Generate unique referral links to invite friends
5. **API Documentation**:
   - Interactive OpenAPI docs at `/docs`

---

## Tech Stack

- **Language**: Python
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database**: SQLite (swappable for Postgres, MySQL, etc. by changing `DB_URL` in `.env`)
- **Testing**: [pytest](https://pytest.org/)
- **Environment Management**: [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Architecture

A high-level view of the application architecture:

```

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

> 1. Connect your GitHub repository.

> 2. Set environment variables (like `DB_URL`, `SECRET_KEY`) in the hosting dashboard.

> 3. Provide a start command, e.g., `uvicorn application.main:app --host 0.0.0.0 --port 8000`.

---

## Future Roadmap

Below are some suggestions to expand or improve the application:

1. **User Authentication**  
   - Implement OAuth2 / JWT tokens for secure endpoints instead of plain text credentials.

2. **Password Hashing**  
   - Store hashed passwords with [Passlib](https://passlib.readthedocs.io/).

3. **Push or Email Notifications**  
   - Integrate with a scheduling system (e.g., [APScheduler](https://apscheduler.readthedocs.io/)) to send daily or weekly reminders to users.

4. **Advanced Analytics**  
   - Actually record user activity to calculate real DAU, retention, etc.
   - Visualize user behavior with charts or dashboards.

5. **Better UI**  
   - Create a React, Vue, or plain HTML/JS frontend to interact with the FastAPI backend.

6. **Deployment & CI/CD**  
   - Automate tests and deployments using GitHub Actions or GitLab CI.

---

## License

This project is under the [MIT License](https://opensource.org/licenses/MIT). Feel free to fork or copy for personal or commercial use.

> **Disclaimer**: This is a sample reference application. For **production use**, remember to:

> - Implement secure password hashing and authentication
> - Use a robust database migration strategy
> - Add proper monitoring and error handling

---

**Thank you for checking out the Task & Habit Tracker!**
