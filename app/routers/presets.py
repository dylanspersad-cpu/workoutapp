from fastapi import Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dependencies import SessionDep
from app.dependencies.auth import AuthDep
from app.repositories.routine_repository import RoutineRepository
from app.repositories.routine_workout_repository import RoutineWorkoutRepository
from app.repositories.workout_repository import WorkoutRepository
from app.services.preset_service import PresetService
from app.services.routine_service import RoutineService
from app.utilities.flash import flash
from . import router, templates


@router.get("/presets/{slug}", response_class=HTMLResponse)
async def preset_detail_view(request: Request, slug: str, user: AuthDep):
    preset_service = PresetService()
    preset = preset_service.get_preset(slug)

    if not preset:
        flash(request, "Preset not found", "danger")
        return RedirectResponse(
            url=request.url_for("dashboard_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return templates.TemplateResponse(
        request=request,
        name="preset_detail.html",
        context={
            "user": user,
            "preset": preset,
        },
    )


@router.post("/presets/{slug}/use", response_class=HTMLResponse)
async def use_preset_action(
    request: Request,
    slug: str,
    db: SessionDep,
    user: AuthDep,
):
    preset_service = PresetService()
    preset = preset_service.get_preset(slug)

    if not preset:
        flash(request, "Preset not found", "danger")
        return RedirectResponse(
            url=request.url_for("dashboard_view"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    routine_repo = RoutineRepository(db)
    routine_workout_repo = RoutineWorkoutRepository(db)
    workout_repo = WorkoutRepository(db)
    routine_service = RoutineService(routine_repo, routine_workout_repo, workout_repo)

    new_routine = routine_service.create_routine_from_preset(user.id, preset)

    flash(request, f"{preset['name']} added to your routines successfully")
    return RedirectResponse(
        url=request.url_for("routine_detail_view", routine_id=new_routine.id),
        status_code=status.HTTP_303_SEE_OTHER,
    )