from sqlmodel import Session, select, desc
from app.models import Routine


class RoutineRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_user(self, user_id: int) -> list[Routine]:
        return self.db.exec(
            select(Routine)
            .where(Routine.user_id == user_id)
            .order_by(desc(Routine.is_favorite), Routine.name)
        ).all()

    def get_by_id_for_user(self, routine_id: int, user_id: int):
        return self.db.exec(
            select(Routine).where(Routine.id == routine_id, Routine.user_id == user_id)
        ).one_or_none()

    def create(self, user_id: int, name: str, description: str = ""):
        routine = Routine(user_id=user_id, name=name, description=description)
        self.db.add(routine)
        self.db.commit()
        self.db.refresh(routine)
        return routine

    def update(self, routine: Routine, name: str, description: str):
        routine.name = name
        routine.description = description
        self.db.add(routine)
        self.db.commit()
        self.db.refresh(routine)
        return routine

    def toggle_favorite(self, routine: Routine):
        routine.is_favorite = not routine.is_favorite
        self.db.add(routine)
        self.db.commit()
        self.db.refresh(routine)
        return routine

    def delete(self, routine: Routine):
        self.db.delete(routine)
        self.db.commit()