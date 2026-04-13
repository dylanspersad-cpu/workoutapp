from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from . import router, templates


@router.get("/app", response_class=HTMLResponse)
async def dashboard_view(request: Request, user: AuthDep):
    ai_last_prompt = request.session.get("ai_last_prompt")
    ai_last_reply = request.session.get("ai_last_reply")

    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={
            "user": user,
            "ai_last_prompt": ai_last_prompt,
            "ai_last_reply": ai_last_reply,
        },
    )