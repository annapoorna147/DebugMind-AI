import re


def analyze_traceback(traceback_text: str) -> dict:
    """
    Extract useful debugging information from a Python traceback.
    Does not execute submitted code.
    """
    if not isinstance(traceback_text, str) or not traceback_text.strip():
        return {
            "status": "invalid",
            "error_type": None,
            "message": "Please provide a traceback.",
            "file": None,
            "line": None
        }

    exception_pattern = r"([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception)):\s*(.*)"
    exception_matches = re.findall(exception_pattern, traceback_text)

    frame_pattern = r'File "([^"]+)", line (\d+)'
    frame_matches = re.findall(frame_pattern, traceback_text)

    if not exception_matches:
        return {
            "status": "unrecognized",
            "error_type": None,
            "message": "Could not identify the exception.",
            "file": None,
            "line": None
        }

    error_type, message = exception_matches[-1]

    file_name, line_number = (
        frame_matches[-1] if frame_matches else (None, None)
    )

    return {
        "status": "analyzed",
        "error_type": error_type,
        "message": message,
        "file": file_name,
        "line": int(line_number) if line_number else None
    }
