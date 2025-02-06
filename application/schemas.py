from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated

ConstrainedStr = Annotated[str, Field(min_length=6, max_length=100)]

class RegisterForm(BaseModel):
    email: EmailStr
    password: ConstrainedStr
        
class LoginForm(BaseModel):
    email: EmailStr
    password: str

# Shared user schema
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    # For Pydantic v2+: use ConfigDict
    model_config = ConfigDict(from_attributes=True)


# Shared task schema
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)
