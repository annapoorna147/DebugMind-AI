import ast


def analyze_syntax(code: str) -> dict:
    """
    Analyze Python code for syntax errors.
    Does not execute the submitted code.
    """

    if not isinstance(code, str) or not code.strip():
        return {
            "status": "invalid",
            "error_type": "EmptyCode",
            "message": "Please provide Python code.",
            "line": None,
            "column": None
        }

    try:
        ast.parse(code)

        return {
            "status": "valid",
            "error_type": None,
            "message": "No syntax errors detected.",
            "line": None,
            "column": None
        }

    except SyntaxError as error:
        return {
            "status": "invalid",
            "error_type": "SyntaxError",
            "message": error.msg,
            "line": error.lineno,
            "column": error.offset
        }

    except (ValueError, TypeError) as error:
        return {
            "status": "invalid",
            "error_type": type(error).__name__,
            "message": str(error),
            "line": None,
            "column": None
        }
