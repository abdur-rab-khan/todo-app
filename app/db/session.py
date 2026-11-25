from sqlmodel import Session, create_engine

from app.core.config import settings
from app.todo.models import *
from app.users.models import *

# The connection string lives on Settings so Alembic and the app share it.
DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=True)

# Tables are managed by Alembic now, not by create_all().


# Making for dependency injection, so that anyone can easily inject it
def get_session():
    with Session(engine) as session:
        yield session
