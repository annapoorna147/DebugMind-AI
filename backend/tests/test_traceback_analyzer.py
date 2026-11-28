from app.services.analyzer.traceback_analyzer import analyze_traceback


def test_empty_traceback():
    result = analyze_traceback("")
    assert result["status"] == "invalid"


def test_zero_division_root_cause():
    traceback = '''Traceback (most recent call last):
  File "main.py", line 5, in calculate
    result = 10 / 0
ZeroDivisionError: division by zero'''

    result = analyze_traceback(traceback)

    assert result["status"] == "analyzed"
    assert result["error_type"] == "ZeroDivisionError"
    assert result["file"] == "main.py"
    assert result["line"] == 5
    assert result["root_cause"] is not None
    assert "zero" in result["root_cause"]["description"].lower()


def test_name_error_root_cause():
    traceback = '''Traceback (most recent call last):
  File "app.py", line 8, in run
    print(username)
NameError: name 'username' is not defined'''

    result = analyze_traceback(traceback)

    assert result["error_type"] == "NameError"
    assert "variable" in result["root_cause"]["description"].lower()


def test_multiple_traceback_frames():
    traceback = '''Traceback (most recent call last):
  File "main.py", line 10, in main
    calculate()
  File "maths.py", line 4, in calculate
    return 10 / 0
ZeroDivisionError: division by zero'''

    result = analyze_traceback(traceback)

    assert len(result["frames"]) == 2
    assert result["file"] == "maths.py"
    assert result["line"] == 4


def test_unknown_exception():
    traceback = '''Traceback (most recent call last):
  File "main.py", line 3, in run
    raise CustomFailure("failed")
CustomFailure: failed'''

    result = analyze_traceback(traceback)

    assert result["error_type"] == "CustomFailure"
    assert result["root_cause"]["suggestion"]


def test_invalid_input():
    result = analyze_traceback(None)

    assert result["status"] == "invalid"
    assert result["frames"] == []
