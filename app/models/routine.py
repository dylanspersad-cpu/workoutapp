from sqlmodel import SQLModel, Field
from typing import Optional


class Routine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str = Field(index=True)
    description: str = ""
    is_favorite: bool = False

    def __str__(self) -> str:
        return f"(Routine id={self.id}, name={self.name}, user_id={self.user_id}, is_favorite={self.is_favorite})"