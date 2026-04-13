from sqlmodel import SQLModel, Field
from typing import Optional


class RoutineWorkout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    routine_id: int = Field(foreign_key="routine.id")
    workout_id: int = Field(foreign_key="workout.id")
    order_index: int = 1
    sets: Optional[int] = None
    reps: Optional[int] = None
    duration_seconds: Optional[int] = None
    notes: str = ""

    def __str__(self) -> str:
        return (
            f"(RoutineWorkout id={self.id}, routine_id={self.routine_id}, "
            f"workout_id={self.workout_id}, order={self.order_index})"
        )