from datetime import date
from uuid import UUID, uuid4

from pydantic import EmailStr, computed_field, field_validator
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import AutoString, DateTime, Field, Relationship, SQLModel

from app.users.schemas import validate_password, validate_url


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PG_UUID(), primary_key=True, server_default=text("gen_random_uuid()")
        ),
    )
    email: EmailStr = Field(sa_type=AutoString, unique=True, index=True)
    password: str = Field(min_length=8, max_length=64)
    dob: date = Field(sa_column=Column(DateTime, nullable=False))
    first_name: str = Field(index=True, min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    profile_url: str = Field(max_length=2083)
    refresh_token: str | None = None

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        return (
            today.year
            - self.dob.year
            - ((today.month, today.day) < (self.dob.month, self.dob.day))
        )

    @field_validator("profile_url")
    @classmethod
    def validate_profile_url(cls, v: str) -> str:
        return validate_url(v)

    @field_validator("password")
    @classmethod
    def validate_pass(cls, value: str) -> str:
        return validate_password(value)

    todos: list["Todo"] = Relationship(back_populates="user")
