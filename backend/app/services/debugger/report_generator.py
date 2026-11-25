def generate_report(analysis: dict) -> dict:
    """
    Convert all debugging analysis results into a readable report.
    """

    if analysis.get("status") != "completed":
        return {
            "status": "failed",
            "title": "Debugging Report",
            "total_findings": 0,
            "findings": [],
            "summary": analysis.get("summary", "Analysis failed.")
        }

    findings = []

    # Syntax findings
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

    # Runtime findings
    traceback = analysis.get("traceback")

    if traceback:
        findings.append({
            "category": "Runtime",
            "severity": "error",
            "message": (
                f"{traceback.get('error_type', 'RuntimeError')}: "
                f"{traceback.get('message', 'Runtime error detected.')}"
            ),
            "file": traceback.get("file"),
            "line": traceback.get("line")
        })

    # Ruff static analysis findings
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

    # AST-based bug pattern findings
    bug_patterns = analysis.get("bug_patterns", {})

    for issue in bug_patterns.get("issues", []):
        findings.append({
            "category": "Bug Pattern",
            "severity": issue.get("severity", "warning"),
            "code": issue.get("code"),
            "message": issue.get("message"),
            "suggestion": issue.get("suggestion"),
            "line": issue.get("line")
        })

    return {
        "status": "completed",
        "title": "DebugMind AI Debugging Report",
        "total_findings": len(findings),
        "findings": findings,
        "summary": analysis.get("summary")
    }
