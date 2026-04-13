from sqlmodel import SQLModel, Field
from typing import Optional


class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    category: str
    target_muscle: str
    equipment: str
    difficulty: str
    instructions: str
    duration_minutes: int = 0
    image_filename: str = "default.png"
    youtube_url: str = ""

    def __str__(self) -> str:
        return f"(Workout id={self.id}, name={self.name}, category={self.category})"