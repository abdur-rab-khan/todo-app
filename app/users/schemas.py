import re
from datetime import date

from pydantic import BaseModel, EmailStr, Field, computed_field, field_validator

PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9\s])\S{8,64}$"
)


# ------------------------- COMMON VALIDATE FUNCTIONS -------------------------
def validate_url(v: str) -> str:
    from pydantic import HttpUrl, TypeAdapter

    return str(TypeAdapter(HttpUrl).validate_python(v))


def validate_password(v: str) -> str:
    if not PASSWORD_REGEX.match(v):
        raise ValueError(
            "Password must be 8-64 characters with no spaces, and include at least one lowercase letter, uppercase letter, digit and special characters."
        )
    return v


# ------------------------- SCHEMA REQUIRED FOR USER -------------------------
class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def validate_pass(cls, value: str):
        return validate_password(value)


class CreateUser(BaseModel):
    id: str
    dob: date
    email: EmailStr
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    profile_url: str = Field(max_length=2083)
    password: str = Field(min_length=8, max_length=64)

    @field_validator("profile_url")
    @classmethod
    def validate_profile_url(cls, v: str) -> str:
        return validate_url(v)

    @field_validator("password")
    @classmethod
    def validate_pass(cls, v: str) -> str:
        return validate_password(v)


class UserData(BaseModel):
    id: str
    dob: date
    email: EmailStr
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    profile_url: str = Field(max_length=2083)
    password: str = Field(min_length=8, max_length=64)

    @computed_field
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @computed_field
    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.dob.year
            - ((today.month, today.day) < (self.dob.month, self.dob.day))
        )


class UpdateUser(BaseModel):
    email: EmailStr | None = None
    dob: date | None = None
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)
    profile_url: str | None = Field(default=None, max_length=2083)
    password: str | None = Field(default=None, min_length=8, max_length=64)
    refresh_token: str | None = None
