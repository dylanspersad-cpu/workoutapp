from fastapi import Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dependencies import SessionDep
from app.dependencies.auth import AuthDep
from app.repositories.routine_repository import RoutineRepository
from app.repositories.routine_workout_repository import RoutineWorkoutRepository
from app.repositories.workout_repository import WorkoutRepository
from app.services.routine_service import RoutineService
from app.services.workout_service import WorkoutService
from app.utilities.flash import flash
from . import router, templates


@router.get("/routines", response_class=HTMLResponse)
async def routines_view(request: Request, db: SessionDep, user: AuthDep):
    routine_repo = RoutineRepository(db)
    routine_workout_repo = RoutineWorkoutRepository(db)
    workout_repo = WorkoutRepository(db)
    routine_service = RoutineService(routine_repo, routine_workout_repo, workout_repo)

    routines = routine_service.get_user_routines(user.id)

    routine_cards = []
    for routine in routines:
        routine_items = routine_workout_repo.get_all_for_routine(routine.id)
        routine_cards.append(
    {
        "id": routine.id,
        "name": routine.name,
        "description": routine.description,
        "exercise_count": len(routine_items),
        "is_favorite": routine.is_favorite,
    }
)

    return templates.TemplateResponse(
        request=request,
        name="routines.html",
        context={
            "user": user,
            "routines": routine_cards,
        },
    )


@router.get("/routines/create", response_class=HTMLResponse)
async def create_routine_view(request: Request, user: AuthDep):
    return templates.TemplateResponse(
        request=request,
        name="create_routine.html",
        context={"user": user},
    )


@router.post("/routines/create", response_class=HTMLResponse)
async def create_routine_action(
    request: Request,
    db: SessionDep,
    user: AuthDep,
    name: str = Form(),
    description: str = Form(default=""),
):
    routine_repo = RoutineRepository(db)
    routine_workout_repo = RoutineWorkoutRepository(db)
    workout_repo = WorkoutRepository(db)
    routine_service = RoutineService(routine_repo, routine_workout_repo, workout_repo)

    routine, error = routine_service.create_routine(user.id, name, description)

    if error:
        flash(request, error, "danger")
        return RedirectResponse(
            url=request.url_for("create_routine_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    flash(request, "Routine created successfully")

    return RedirectResponse(
        url=request.url_for("routines_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/routines/{routine_id}", response_class=HTMLResponse)
async def routine_detail_view(
    request: Request,
    routine_id: int,
    db: SessionDep,
    user: AuthDep,
):
    routine_repo = RoutineRepository(db)
    routine_workout_repo = RoutineWorkoutRepository(db)
    workout_repo = WorkoutRepository(db)

    routine_service = RoutineService(routine_repo, routine_workout_repo, workout_repo)
    workout_service = WorkoutService(workout_repo)

    routine, routine_items = routine_service.get_routine_details(routine_id, user.id)
    if not routine:
        flash(request, "Routine not found", "danger")
        return RedirectResponse(
            url=request.url_for("routines_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    workouts = workout_service.get_workouts()

    return templates.TemplateResponse(
        request=request,
        name="routine_detail.html",
        context={
            "user": user,
            "routine": routine,
            "routine_items": routine_items,
            "workouts": workouts,
        },
    )


@router.get("/routines/{routine_id}/edit", response_class=HTMLResponse)
async def edit_routine_view(
    request: Request,
    routine_id: int,
    db: SessionDep,
    user: AuthDep,
):
    routine_repo = RoutineRepository(db)
    routine = routine_repo.get_by_id_for_user(routine_id, user.id)

    if not routine:
        flash(request, "Routine not found", "danger")
        return RedirectResponse(
            url=request.url_for("routines_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return templates.TemplateResponse(
        request=request,
        name="edit_routine.html",
        context={
            "user": user,
            "routine": routine,
        },
    )


@router.post("/routines/{routine_id}/edit", response_class=HTMLResponse)
async def edit_routine_action(
    request: Request,
    routine_id: int,
    db: SessionDep,
    user: AuthDep,
    name: str = Form(),
    description: str = Form(default=""),
):
    routine_repo = RoutineRepository(db)
    routine_workout_repo = RoutineWorkoutRepository(db)
    workout_repo = WorkoutRepository(db)
    routine_service = RoutineService(routine_repo, routine_workout_repo, workout_repo)

    updated, error = routine_service.update_routine(routine_id, user.id, name, description)

    if error:
        flash(request, error, "danger")
        if error == "Routine not found.":
            return RedirectResponse(
                url=request.url_for("routines_view"),
                status_code=status.HTTP_303_SEE_OTHER,
            )
        return RedirectResponse(
            url=request.url_for("edit_routine_view", routine_id=routine_id),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    flash(request, "Routine updated successfully")
    return RedirectResponse(
        url=request.url_for("routine_detail_view", routine_id=routine_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/routines/{routine_id}/delete", response_class=HTMLResponse)
async def delete_routine_action(
    request: Request,
    routine_id: int,
    db: SessionDep,
    user: AuthDep,
):
    routine_repo = RoutineRepository(db)
    routine_workout_repo = RoutineWorkoutRepository(db)
    workout_repo = WorkoutRepository(db)
    routine_service = RoutineService(routine_repo, routine_workout_repo, workout_repo)

    deleted = routine_service.delete_routine(routine_id, user.id)
    if not deleted:
        flash(request, "Routine not found", "danger")
    else:
        flash(request, "Routine deleted successfully")

    return RedirectResponse(
        url=request.url_for("routines_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/routines/{routine_id}/add-workout", response_class=HTMLResponse)
async def add_workout_to_routine_action(
    request: Request,
    routine_id: int,
    db: SessionDep,
    user: AuthDep,
    workout_id: int = Form(),
    sets: int | None = Form(default=None),
    reps: int | None = Form(default=None),
    duration_seconds: int | None = Form(default=None),
    notes: str = Form(default=""),
):
    routine_repo = RoutineRepository(db)
    routine_workout_repo = RoutineWorkoutRepository(db)
    workout_repo = WorkoutRepository(db)
    routine_service = RoutineService(routine_repo, routine_workout_repo, workout_repo)

    item, error = routine_service.add_workout_to_routine(
        routine_id=routine_id,
        user_id=user.id,
        workout_id=workout_id,
        sets=sets,
        reps=reps,
        duration_seconds=duration_seconds,
        notes=notes,
    )

    if error:
        flash(request, error, "danger")
        return RedirectResponse(
            url=request.url_for("routine_detail_view", routine_id=routine_id),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    flash(request, "Workout added to routine successfully")

    return RedirectResponse(
        url=request.url_for("routine_detail_view", routine_id=routine_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/routine-workout/{routine_workout_id}/delete", response_class=HTMLResponse)
async def remove_workout_from_routine_action(
    request: Request,
    routine_workout_id: int,
    db: SessionDep,
    user: AuthDep,
):
    routine_repo = RoutineRepository(db)
    routine_workout_repo = RoutineWorkoutRepository(db)
    workout_repo = WorkoutRepository(db)
    routine_service = RoutineService(routine_repo, routine_workout_repo, workout_repo)

    routine_workout = routine_workout_repo.get_by_id(routine_workout_id)
    if not routine_workout:
        flash(request, "Workout item not found", "danger")
        return RedirectResponse(
            url=request.url_for("routines_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    routine_id = routine_workout.routine_id

    removed = routine_service.remove_workout_from_routine(routine_workout_id, user.id)
    if not removed:
        flash(request, "Could not remove workout from routine", "danger")
        return RedirectResponse(
            url=request.url_for("routines_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    flash(request, "Workout removed from routine successfully")
    return RedirectResponse(
        url=request.url_for("routine_detail_view", routine_id=routine_id),
        status_code=status.HTTP_303_SEE_OTHER,
    )

@router.post("/routines/{routine_id}/duplicate", response_class=HTMLResponse)
async def duplicate_routine_action(
    request: Request,
    routine_id: int,
    db: SessionDep,
    user: AuthDep,
):
    routine_repo = RoutineRepository(db)
    routine_workout_repo = RoutineWorkoutRepository(db)
    workout_repo = WorkoutRepository(db)
    routine_service = RoutineService(routine_repo, routine_workout_repo, workout_repo)

    duplicated_routine, error = routine_service.duplicate_routine(routine_id, user.id)

    if error:
        flash(request, error, "danger")
        return RedirectResponse(
            url=request.url_for("routines_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    flash(request, "Routine duplicated successfully")

    return RedirectResponse(
        url=request.url_for("routine_detail_view", routine_id=duplicated_routine.id),
        status_code=status.HTTP_303_SEE_OTHER,
    )

@router.post("/routines/{routine_id}/favorite", response_class=HTMLResponse)
async def toggle_favorite_routine_action(
    request: Request,
    routine_id: int,
    db: SessionDep,
    user: AuthDep,
):
    routine_repo = RoutineRepository(db)
    routine_workout_repo = RoutineWorkoutRepository(db)
    workout_repo = WorkoutRepository(db)
    routine_service = RoutineService(routine_repo, routine_workout_repo, workout_repo)

    updated_routine, error = routine_service.toggle_favorite(routine_id, user.id)

    if error:
        flash(request, error, "danger")
        return RedirectResponse(
            url=request.url_for("routines_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    if updated_routine.is_favorite:
        flash(request, "Routine added to favorites")
    else:
        flash(request, "Routine removed from favorites")

    return RedirectResponse(
        url=request.url_for("routines_view"),
        status_code=status.HTTP_303_SEE_OTHER,
    )