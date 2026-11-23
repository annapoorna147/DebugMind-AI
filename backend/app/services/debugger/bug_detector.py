from app.services.analyzer.syntax_analyzer import analyze_syntax
from app.services.analyzer.traceback_analyzer import analyze_traceback
from app.services.analyzer.static_analyzer import analyze_static


def detect_bugs(code: str, traceback_text: str | None = None) -> dict:
    """
    Combine syntax, traceback, and static analysis results.
    """

    syntax_result = analyze_syntax(code)

    if syntax_result["status"] == "invalid":
        return {
            "status": "failed",
            "syntax": syntax_result,
            "traceback": None,
            "static_analysis": None,
            "summary": "Fix the syntax error before further analysis."
        }

    traceback_result = (
        analyze_traceback(traceback_text)
        if traceback_text
        else None
    )

    static_result = analyze_static(code)

    return {
        "status": "completed",
        "syntax": syntax_result,
        "traceback": traceback_result,
        "static_analysis": static_result,
        "summary": "Debugging analysis completed."
    }
