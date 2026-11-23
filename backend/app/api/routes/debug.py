from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.debugger.bug_detector import detect_bugs
from app.services.debugger.report_generator import generate_report

router = APIRouter()


class DebugRequest(BaseModel):
    code: str = Field(..., min_length=1)
    traceback: str | None = None


@router.post("/debug")
async def debug_code(request: DebugRequest):
    analysis = detect_bugs(
        request.code,
        request.traceback
    )

    report = generate_report(analysis)

    return report
