from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.debugger.bug_detector import detect_bugs
from app.services.debugger.report_generator import generate_report
from app.services.ai.ai_debugger import analyze_with_ai

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
    ai_result = analyze_with_ai(request.code, report)
    report['ai_analysis'] = ai_result

    return report
