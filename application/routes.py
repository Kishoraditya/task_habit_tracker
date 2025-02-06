from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import ValidationError
from application.schemas import UserCreate, UserOut, TaskCreate, TaskOut
from application.models import User, Task
from application.schemas import RegisterForm, LoginForm
from application.utils import generate_referral_link, hash_password, verify_password
from infrastructure.database import get_db
from typing import List
from typing import List
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def landing_page(request: Request):
    """
    Render the landing page with a retro, notebook style.
    """
    return templates.TemplateResponse(
        request,
        "landing.html",
        {"request": request}
    )

@router.get("/register", response_class=HTMLResponse, include_in_schema=False)
def register_form(request: Request):
    """
    Display the registration form.
    """
    return templates.TemplateResponse(
        request,
        "register.html",
        {"request": request}
    )

@router.post("/register", response_class=HTMLResponse, include_in_schema=False)
def register_user(request: Request,
                  email: str = Form(...),
                  password: str = Form(...),
                  db: Session = Depends(get_db)):
    # 1) Use Pydantic for validation
    try:
        data = RegisterForm(email=email, password=password)
    except ValidationError as e:
        return templates.TemplateResponse(
            request,
            "register.html",
            {
                "request": request,
                "error": str(e)
            },
            status_code=400
        )

    # 2) Check if email is already registered
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        return templates.TemplateResponse(
            request,
            "register.html",
            {
                "request": request,
                "error": "Email already registered."
            },
            status_code=400
        )

    # 3) Hash password
    hashed = hash_password(data.password)

    # 4) Create user
    new_user = User(email=data.email, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5) Log user in
    request.session["user_id"] = new_user.id

    # (Optional) send verification email here, set new_user.is_verified=False initially
    # Later, user clicks a link => we set is_verified=True

    return RedirectResponse(url="/dashboard", status_code=302)

@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_form(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse, include_in_schema=False)
def login_user(request: Request,
               email: str = Form(...),
               password: str = Form(...),
               db: Session = Depends(get_db)):
    # 1) Use Pydantic for validation
    try:
        data = LoginForm(email=email, password=password)
    except ValidationError as e:
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "request": request,
                "error": str(e)
            },
            status_code=400
        )

    # 2) Find user in DB
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "request": request,
                "error": "Invalid email or password."
            },
            status_code=400
        )

    # 3) Check password
    if not verify_password(data.password, user.password):
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "request": request,
                "error": "Invalid email or password."
            },
            status_code=400
        )

    # (Optional) check if user.is_verified?
    # if not user.is_verified:
    #     return templates.TemplateResponse(
    #         request,
    #         "login.html",
    #         {"request": request, "error": "Please verify your email first."},
    #         status_code=403
    #     )

    # 4) Successful login
    request.session["user_id"] = user.id
    return RedirectResponse(url="/dashboard", status_code=302)

@router.get("/logout", include_in_schema=False)
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)

@router.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=302)

    tasks = db.query(Task).filter(Task.user_id == user_id).all()

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"request": request, "user": user, "tasks": tasks}
    )

@router.post("/create_task", response_class=HTMLResponse, include_in_schema=False)
def create_task_view(request: Request,
                     title: str = Form(...),
                     description: str = Form(""),
                     db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    new_task = Task(title=title, description=description, user_id=user_id)
    db.add(new_task)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=302)

@router.get("/complete_task/{task_id}", response_class=HTMLResponse, include_in_schema=False)
def complete_task_ui(task_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        task.completed = True
        db.commit()

    return RedirectResponse(url="/dashboard", status_code=302)

@router.get("/admin", response_class=HTMLResponse, include_in_schema=False)
def admin_dashboard(request: Request, admin_key: str, db: Session = Depends(get_db)):
    # same as before
    required_key = os.getenv("ADMIN_KEY", "")
    if admin_key != required_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin key")

    dau = {"DAU": 123}
    tasks_per_day = {"tasks_completed_per_day": 45}
    retention = {"4_week_retention_percentage": 32.5}

    return templates.TemplateResponse(
        request,
        "admin_dashboard.html",
        {
            "request": request,
            "dau": dau,
            "tasks_per_day": tasks_per_day,
            "retention": retention
        }
    )

# Existing JSON endpoints can remain the same...
@router.get("/analytics/dau", operation_id="get_dau_metrics")
async def get_dau():
    return {"message": "DAU Analytics"}

@router.get("/analytics/tasks_per_day", operation_id="get_tasks_completed_metrics")
async def get_tasks_completed_per_day():
    return {"message": "Tasks per Day Analytics"}

@router.get("/analytics/retention", operation_id="get_retention_metrics")
async def get_4_week_retention():
    return {"message": "4-Week Retention Analytics"}

@router.get("/referral/{user_id}", operation_id="generate_user_referral")
async def generate_referral(user_id: int):
    return {"message": f"Referral for user {user_id}"}


@router.post("/users", response_model=UserOut, include_in_schema=False)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # In production, hash the password
    new_user = User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{user_id}", response_model=UserOut, include_in_schema=False)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/users/{user_id}/tasks", response_model=TaskOut, include_in_schema=False)
def create_task_for_user(user_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    new_task = Task(**task.dict(), user_id=user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/users/{user_id}/tasks", response_model=List[TaskOut], include_in_schema=False)
def get_tasks_for_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.tasks

@router.patch("/tasks/{task_id}", response_model=TaskOut, include_in_schema=False)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    task.completed = True
    db.commit()
    db.refresh(task)
    return task


@router.post("/create_task", response_class=HTMLResponse, include_in_schema=False)
def create_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    new_task = Task(title=title, description=description, user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return RedirectResponse(url="/dashboard", status_code=302)



