from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.database import Base

# Association table for shared lists with roles
list_shares = Table(
    "list_shares",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("list_id", Integer, ForeignKey("task_lists.id")),
    Column("role", String, default="read")  # Roles: read, write, admin
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Now will store hashed password
    created_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)  # for email verification flow

    tasks = relationship("Task", back_populates="user")
    task_lists = relationship("TaskList", back_populates="owner")
    shared_lists = relationship("TaskList", secondary=list_shares, back_populates="shared_users")

class TaskList(Base):
    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="task_list")
    owner = relationship("User", back_populates="task_lists")
    shared_users = relationship("User", secondary=list_shares, back_populates="shared_lists")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    list_id = Column(Integer, ForeignKey("task_lists.id"), nullable=True)

    user = relationship("User", back_populates="tasks")
    task_list = relationship("TaskList", back_populates="tasks")
