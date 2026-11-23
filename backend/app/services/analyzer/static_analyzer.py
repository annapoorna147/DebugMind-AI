import json
import subprocess
import sys
import tempfile
from pathlib import Path


def analyze_static(code: str) -> dict:
    if not isinstance(code, str) or not code.strip():
        return {
            "status": "invalid",
            "issues": [],
            "message": "Please provide Python code."
        }

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "submitted_code.py"
            file_path.write_text(code, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "ruff",
                    "check",
                    "--output-format",
                    "json",
                    str(file_path)
                ],
                capture_output=True,
                text=True,
                timeout=10,
                check=False
            )

            issues = json.loads(result.stdout or "[]")

            return {
                "status": "analyzed",
                "issue_count": len(issues),
                "issues": [
                    {
                        "code": issue.get("code"),
                        "message": issue.get("message"),
                        "line": issue.get("location", {}).get("row"),
                        "column": issue.get("location", {}).get("column")
                    }
                    for issue in issues
                ]
            }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "issues": [],
            "message": "Static analysis timed out."
        }
    except (OSError, json.JSONDecodeError) as error:
        return {
            "status": "error",
            "issues": [],
            "message": str(error)
        }
