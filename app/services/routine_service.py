from app.repositories.routine_repository import RoutineRepository
from app.repositories.routine_workout_repository import RoutineWorkoutRepository
from app.repositories.workout_repository import WorkoutRepository


class RoutineService:
    def __init__(
        self,
        routine_repo: RoutineRepository,
        routine_workout_repo: RoutineWorkoutRepository,
        workout_repo: WorkoutRepository,
    ):
        self.routine_repo = routine_repo
        self.routine_workout_repo = routine_workout_repo
        self.workout_repo = workout_repo

    def get_user_routines(self, user_id: int):
        return self.routine_repo.get_all_for_user(user_id)

    def create_routine(self, user_id: int, name: str, description: str = ""):
        name = name.strip()
        description = description.strip()

        if not name:
            return None, "Routine name cannot be blank."

        routine = self.routine_repo.create(user_id, name, description)
        return routine, None

    def get_routine_details(self, routine_id: int, user_id: int):
        routine = self.routine_repo.get_by_id_for_user(routine_id, user_id)
        if not routine:
            return None, []

        routine_items = self.routine_workout_repo.get_all_for_routine(routine.id)

        detailed_items = []
        for item in routine_items:
            workout = self.workout_repo.get_by_id(item.workout_id)
            detailed_items.append(
                {
                    "id": item.id,
                    "order_index": item.order_index,
                    "sets": item.sets,
                    "reps": item.reps,
                    "duration_seconds": item.duration_seconds,
                    "notes": item.notes,
                    "workout": workout,
                }
            )

        return routine, detailed_items

    def update_routine(self, routine_id: int, user_id: int, name: str, description: str):
        routine = self.routine_repo.get_by_id_for_user(routine_id, user_id)
        if not routine:
            return None, "Routine not found."

        name = name.strip()
        description = description.strip()

        if not name:
            return None, "Routine name cannot be blank."

        updated = self.routine_repo.update(routine, name, description)
        return updated, None

    def delete_routine(self, routine_id: int, user_id: int):
        routine = self.routine_repo.get_by_id_for_user(routine_id, user_id)
        if not routine:
            return False

        routine_items = self.routine_workout_repo.get_all_for_routine(routine.id)
        for item in routine_items:
            self.routine_workout_repo.delete(item)

        self.routine_repo.delete(routine)
        return True

    def add_workout_to_routine(
        self,
        routine_id: int,
        user_id: int,
        workout_id: int,
        sets: int | None = None,
        reps: int | None = None,
        duration_seconds: int | None = None,
        notes: str = "",
    ):
        routine = self.routine_repo.get_by_id_for_user(routine_id, user_id)
        if not routine:
            return None, "Routine not found."

        workout = self.workout_repo.get_by_id(workout_id)
        if not workout:
            return None, "Selected workout does not exist."

        if sets is not None and sets < 0:
            return None, "Sets cannot be negative."

        if reps is not None and reps < 0:
            return None, "Reps cannot be negative."

        if duration_seconds is not None and duration_seconds < 0:
            return None, "Duration cannot be negative."

        if reps is None and duration_seconds is None:
            return None, "Please enter at least reps or duration."

        notes = notes.strip()

        existing_items = self.routine_workout_repo.get_all_for_routine(routine.id)
        next_order = len(existing_items) + 1

        item = self.routine_workout_repo.add_to_routine(
            routine_id=routine.id,
            workout_id=workout.id,
            order_index=next_order,
            sets=sets,
            reps=reps,
            duration_seconds=duration_seconds,
            notes=notes,
        )
        return item, None

    def remove_workout_from_routine(self, routine_workout_id: int, user_id: int):
        routine_workout = self.routine_workout_repo.get_by_id(routine_workout_id)
        if not routine_workout:
            return False

        routine = self.routine_repo.get_by_id_for_user(routine_workout.routine_id, user_id)
        if not routine:
            return False

        self.routine_workout_repo.delete(routine_workout)
        return True
    
    def duplicate_routine(self, routine_id: int, user_id: int):
        original_routine = self.routine_repo.get_by_id_for_user(routine_id, user_id)
        if not original_routine:
            return None, "Routine not found."

        original_name = original_routine.name.strip()

        user_routines = self.routine_repo.get_all_for_user(user_id)
        existing_names = {routine.name for routine in user_routines}

        counter = 1
        new_name = f"{original_name} Remix {counter}"

        while new_name in existing_names:
            counter += 1
            new_name = f"{original_name} Remix {counter}"

        new_description = original_routine.description.strip() if original_routine.description else ""

        duplicated_routine = self.routine_repo.create(
            user_id=user_id,
            name=new_name,
            description=new_description,
        )

        original_items = self.routine_workout_repo.get_all_for_routine(original_routine.id)

        for item in original_items:
            self.routine_workout_repo.add_to_routine(
                routine_id=duplicated_routine.id,
                workout_id=item.workout_id,
                order_index=item.order_index,
                sets=item.sets,
                reps=item.reps,
                duration_seconds=item.duration_seconds,
                notes=item.notes,
            )

        return duplicated_routine, None
    
    def create_routine_from_preset(self, user_id: int, preset: dict):
        original_name = preset["name"].strip()

        user_routines = self.routine_repo.get_all_for_user(user_id)
        existing_names = {routine.name for routine in user_routines}

        counter = 1
        new_name = original_name

        while new_name in existing_names:
            counter += 1
            new_name = f"{original_name} Remix {counter}"

        new_routine = self.routine_repo.create(
            user_id=user_id,
            name=new_name,
            description=preset["description"],
        )

        order_index = 1
        for item in preset["items"]:
            workout = self.workout_repo.get_by_name(item["workout_name"])
            if not workout:
                continue

            self.routine_workout_repo.add_to_routine(
                routine_id=new_routine.id,
                workout_id=workout.id,
                order_index=order_index,
                sets=item.get("sets"),
                reps=item.get("reps"),
                duration_seconds=item.get("duration_seconds"),
                notes=item.get("notes", ""),
            )
            order_index += 1

        return new_routine
    
    def toggle_favorite(self, routine_id: int, user_id: int):
        routine = self.routine_repo.get_by_id_for_user(routine_id, user_id)
        if not routine:
            return None, "Routine not found."

        updated_routine = self.routine_repo.toggle_favorite(routine)
        return updated_routine, None