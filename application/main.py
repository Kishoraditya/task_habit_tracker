from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from application.routes import router as api_router
from monitoring.logging_config import setup_logging
import os
from infrastructure.database import Base, engine
from starlette.staticfiles import StaticFiles
app = FastAPI(
    title="Task & Habit Tracker",
    description="A lightweight web app for tracking tasks & habits with basic analytics and referrals.",
    version="1.0.0"
)

# 1) Ensure DB tables are created at startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    
# Initialize logging
setup_logging()

# Include our API routes
app.include_router(api_router)

# Optionally, you can add event handlers (startup/shutdown) here if needed
# @app.on_event("startup")
# async def startup_event():
#     pass
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     pass
# 3) Mount static files so /static/css/style.css will be found
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4) Include our routes (endpoints, HTML forms, etc.)
app.include_router(api_router)

# 5) Add session middleware for login sessions
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
