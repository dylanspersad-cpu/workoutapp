from sqlmodel import Session, select
from app.models import Workout


class WorkoutRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Workout]:
        return self.db.exec(select(Workout).order_by(Workout.name)).all()

    def search(self, q: str) -> list[Workout]:
        return self.db.exec(
            select(Workout)
            .where(
                Workout.name.ilike(f"%{q}%")
                | Workout.category.ilike(f"%{q}%")
                | Workout.target_muscle.ilike(f"%{q}%")
                | Workout.equipment.ilike(f"%{q}%")
                | Workout.difficulty.ilike(f"%{q}%")
            )
            .order_by(Workout.name)
        ).all()

    def get_by_id(self, workout_id: int):
        return self.db.get(Workout, workout_id)
    
    def get_by_name(self, name: str):
        return self.db.exec(
            select(Workout).where(Workout.name == name)
        ).one_or_none()