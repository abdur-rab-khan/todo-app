from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    age: int
    address: str = Field(min_length=1, max_length=255)
