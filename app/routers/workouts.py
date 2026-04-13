from fastapi import Request, Query
from fastapi.responses import HTMLResponse

from app.dependencies import SessionDep
from app.dependencies.auth import AuthDep
from app.repositories.workout_repository import WorkoutRepository
from app.repositories.routine_repository import RoutineRepository
from app.services.workout_service import WorkoutService
from . import router, templates


@router.get("/workouts", response_class=HTMLResponse)
async def workouts_view(
    request: Request,
    db: SessionDep,
    user: AuthDep,
    q: str = Query(default=""),
):
    workout_repo = WorkoutRepository(db)
    workout_service = WorkoutService(workout_repo)
    workouts = workout_service.get_workouts(q)

    routine_repo = RoutineRepository(db)
    routines = routine_repo.get_all_for_user(user.id)
    routines_data = [{"id": r.id, "name": r.name} for r in routines]

    return templates.TemplateResponse(
        request=request,
        name="workouts.html",
        context={
            "user": user,
            "workouts": workouts,
            "q": q,
            "routines": routines_data,
        },
    )
