
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=1, le=120)
    course: str = Field(min_length=2, max_length=100)

    @field_validator("name", "course")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError("At least 2 characters are required")

        return value


class StudentUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=1, le=120)
    course: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    @field_validator("name", "course")
    @classmethod
    def strip_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return value

        value = value.strip()

        if len(value) < 2:
            raise ValueError("At least 2 characters are required")

        return value


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    course: str

    model_config = ConfigDict(from_attributes=True)