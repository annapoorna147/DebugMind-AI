import re


ERROR_HINTS = {
    "ZeroDivisionError": (
        "The code attempted to divide a number by zero.",
        "Check the denominator before division. Ensure it is not zero."
    ),
    "NameError": (
        "The code used a variable or name that has not been defined.",
        "Check variable spelling and make sure it is defined before use."
    ),
    "TypeError": (
        "An operation or function received an incompatible data type.",
        "Check the types of the values being passed and convert them if needed."
    ),
    "IndexError": (
        "The code tried to access a list or sequence index that does not exist.",
        "Check the sequence length and ensure the index is within range."
    ),
    "KeyError": (
        "The code tried to access a dictionary key that does not exist.",
        "Check whether the key exists before accessing it, or use dict.get()."
    ),
    "AttributeError": (
        "The code tried to access an attribute or method that does not exist.",
        "Check the object's type and verify that the attribute or method is valid."
    ),
    "FileNotFoundError": (
        "The requested file or directory could not be found.",
        "Verify the file path, filename, and working directory."
    ),
    "ImportError": (
        "Python could not import a requested module or object.",
        "Check the module name, installation, and import statement."
    ),
    "ModuleNotFoundError": (
        "Python could not find the requested module.",
        "Install the missing package in the active environment or correct the module name."
    ),
    "ValueError": (
        "A function received a value of the correct type but an invalid value.",
        "Validate the input before passing it to the function."
    ),
    "IndentationError": (
        "The code contains inconsistent or invalid indentation.",
        "Check indentation levels and use consistent spaces."
    ),
    "SyntaxError": (
        "Python could not parse the code because of invalid syntax.",
        "Inspect the reported line and the line immediately before it."
    ),
    "RecursionError": (
        "The code exceeded Python's maximum recursion depth.",
        "Check recursive calls and make sure each recursive path has a stopping condition."
    ),
    "MemoryError": (
        "The program ran out of available memory.",
        "Reduce memory usage or process large data in smaller batches."
    ),
    "AssertionError": (
        "An assertion condition evaluated to False.",
        "Check the asserted condition and the values used in the test."
    ),
    "StopIteration": (
        "An iterator has no more items to provide.",
        "Check iterator exhaustion or use a loop that handles completion."
    ),
}


def _extract_frames(traceback_text: str) -> list:
    """Extract file, line, function, and source context from traceback frames."""
    frames = []
    lines = traceback_text.splitlines()

    for index, line in enumerate(lines):
        match = re.search(
            r'File "([^"]+)", line (\d+)(?:, in (.+))?',
            line
        )

        if not match:
            continue

        source_line = None

        if index + 1 < len(lines):
            candidate = lines[index + 1].strip()
            if candidate and not candidate.startswith("File "):
                source_line = candidate

        frames.append({
            "file": match.group(1),
            "line": int(match.group(2)),
            "function": match.group(3),
            "source": source_line,
        })

    return frames


def _identify_root_cause(error_type: str, message: str) -> dict:
    """Return a probable explanation and suggested fix."""
    explanation, suggestion = ERROR_HINTS.get(
        error_type,
        (
            f"The program raised a {error_type}.",
            "Inspect the traceback and the reported line to identify the failing operation."
        )
    )

    return {
        "description": explanation,
        "suggestion": suggestion,
        "details": message,
    }


def analyze_traceback(traceback_text: str) -> dict:
    """
    Analyze a Python traceback and identify a probable root cause.
    Does not execute submitted code.
    """
    if not isinstance(traceback_text, str) or not traceback_text.strip():
        return {
            "status": "invalid",
            "error_type": None,
            "message": "Please provide a traceback.",
            "file": None,
            "line": None,
            "frames": [],
            "root_cause": None,
        }

    exception_pattern = (
        r"^([A-Za-z_][A-Za-z0-9_]*)"
        r"(?::\s*(.*))?$"
    )

    exception_matches = re.findall(
        exception_pattern,
        traceback_text,
        flags=re.MULTILINE
    )

    if not exception_matches:
        return {
            "status": "unrecognized",
            "error_type": None,
            "message": "Could not identify the exception.",
            "file": None,
            "line": None,
            "frames": [],
            "root_cause": None,
        }

    error_type, message = exception_matches[-1]
    frames = _extract_frames(traceback_text)

    last_frame = frames[-1] if frames else {}

    return {
        "status": "analyzed",
        "error_type": error_type,
        "message": message or "",
        "file": last_frame.get("file"),
        "line": last_frame.get("line"),
        "frames": frames,
        "root_cause": _identify_root_cause(error_type, message or ""),
    }
