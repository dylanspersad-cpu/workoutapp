from sqlmodel import Session, select
from app.models import RoutineWorkout


class RoutineWorkoutRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_routine(self, routine_id: int) -> list[RoutineWorkout]:
        return self.db.exec(
            select(RoutineWorkout)
            .where(RoutineWorkout.routine_id == routine_id)
            .order_by(RoutineWorkout.order_index)
        ).all()

    def get_by_id(self, routine_workout_id: int):
        return self.db.get(RoutineWorkout, routine_workout_id)

    def add_to_routine(
        self,
        routine_id: int,
        workout_id: int,
        order_index: int,
        sets: int | None = None,
        reps: int | None = None,
        duration_seconds: int | None = None,
        notes: str = "",
    ):
        item = RoutineWorkout(
            routine_id=routine_id,
            workout_id=workout_id,
            order_index=order_index,
            sets=sets,
            reps=reps,
            duration_seconds=duration_seconds,
            notes=notes,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, routine_workout: RoutineWorkout):
        self.db.delete(routine_workout)
        self.db.commit()