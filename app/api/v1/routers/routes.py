from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, success: int = 0, error: int = 0):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "success": bool(success),
            "error": bool(error),
        },
    )