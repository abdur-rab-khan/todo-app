from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.todo.models import *
from app.users.models import *

DATABASE_URL = f"postgresql://{settings.user}:{settings.password}@{settings.host_name}:{settings.port}/{settings.db_name}"

engine = create_engine(DATABASE_URL, echo=True)

# Here we are creating all the tables
SQLModel.metadata.create_all(engine)


# Making for dependency injection, so that anyone can easily inject it
def get_session():
    with Session(engine) as session:
        yield session
