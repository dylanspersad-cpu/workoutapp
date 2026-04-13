from app.repositories.workout_repository import WorkoutRepository


class WorkoutService:
    def __init__(self, workout_repo: WorkoutRepository):
        self.workout_repo = workout_repo

    def get_workouts(self, q: str = ""):
        if q:
            return self.workout_repo.search(q)
        return self.workout_repo.get_all()

    def get_workout_by_id(self, workout_id: int):
        return self.workout_repo.get_by_id(workout_id)