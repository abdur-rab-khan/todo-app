from fastapi import FastAPI

from app.core.config import settings
from app.todo.router import todo_router
from app.users.router import user_router

app = FastAPI(title="todo-app")

app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(todo_router, prefix="/todo", tags=["Todos"])
