from fastapi import Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dependencies.auth import AuthDep
from app.services.ai_service import AIService
from app.utilities.flash import flash
from . import router, templates


@router.post("/ai/chat", response_class=HTMLResponse)
async def ai_chat_action(
    request: Request,
    user: AuthDep,
    prompt: str = Form(),
):
    prompt = prompt.strip()

    if not prompt:
        flash(request, "Please enter a message for the AI assistant.", "danger")
        return RedirectResponse(url=request.url_for("dashboard_view"), status_code=status.HTTP_303_SEE_OTHER)

    try:
        ai_service = AIService()
        ai_reply = ai_service.ask(prompt)
        request.session["ai_last_prompt"] = prompt
        request.session["ai_last_reply"] = ai_reply
    except Exception as e:
        print("AI assistant error:", e)
        flash(request, "The AI assistant is currently unavailable. Please try again later.", "danger")

    return RedirectResponse(url=request.url_for("dashboard_view"), status_code=status.HTTP_303_SEE_OTHER)