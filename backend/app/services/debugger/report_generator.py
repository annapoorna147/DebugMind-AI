def generate_report(analysis: dict) -> dict:
    """
    Convert debugging analysis into a readable report.
    """

    if analysis.get("status") != "completed":
        return {
            "status": "failed",
            "title": "Debugging Report",
            "findings": [analysis.get("summary", "Analysis failed.")]
        }

    findings = []

    syntax = analysis.get("syntax", {})

    if syntax.get("status") == "valid":
        findings.append({
            "category": "Syntax",
            "severity": "info",
            "message": "No syntax errors detected."
        })
    else:
        findings.append({
            "category": "Syntax",
            "severity": "error",
            "message": syntax.get("message", "Syntax error detected."),
            "line": syntax.get("line")
        })

    traceback = analysis.get("traceback")

    if traceback:
        findings.append({
            "category": "Runtime",
            "severity": "error",
            "message": (
                f"{traceback['error_type']}: "
                f"{traceback['message']}"
            ),
            "file": traceback.get("file"),
            "line": traceback.get("line")
        })

    static_analysis = analysis.get("static_analysis", {})

    for issue in static_analysis.get("issues", []):
        findings.append({
            "category": "Code Quality",
            "severity": "warning",
            "code": issue.get("code"),
            "message": issue.get("message"),
            "line": issue.get("line"),
            "column": issue.get("column")
        })

    return {
        "status": "completed",
        "title": "DebugMind AI Debugging Report",
        "total_findings": len(findings),
        "findings": findings,
        "summary": analysis.get("summary")
    }
