from datetime import datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, func


class Todo(SQLModel):
    __tablename__ = "todos"

    id: UUID = Field(
        sa_column=Column(
            PG_UUID(), primary_key=True, server_default=text("gen_random_uuid()")
        )
    )
    title: str = Field(min_length=5, max_items=255)
    description: str = Field(default="", min_length=5, max_length=500, nullable=True)
    is_done: bool = Field(default=False)
    user_id: UUID = Field(sa_type=PG_UUID(), nullable=False)

    # 👉 "server_default" run when generates an INSERT statement, if application does not provide anything database will
    #     automatically run "func.now()"
    # 👉 "func.now()" gives list of utils functions
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    )

    # 👉 It's use to populate the data without using ".join()", and "back_populates" what's the field name in the related table
    user: "User" = Relationship(back_populates="todos")
