from datetime import date
from uuid import UUID

from pydantic import computed_field, field_validator
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import DateTime, Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        )
    )
    dob: date = Field(sa_column=Column(DateTime, nullable=False))
    first_name: str = Field(index=True, min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    profile_url: str = Field(max_length=2083)
    refresh_token: str

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
        from pydantic import HttpUrl, TypeAdapter

        return str(TypeAdapter(HttpUrl).validate_python(v))

    todos: list["Todo"] = Relationship(back_populates="user")
