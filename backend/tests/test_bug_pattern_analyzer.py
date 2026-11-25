from app.services.analyzer.bug_pattern_analyzer import analyze_bug_patterns
from app.services.debugger.bug_detector import detect_bugs
from app.services.debugger.report_generator import generate_report


def test_detect_division_by_zero():
    result = analyze_bug_patterns("result = 10 / 0")

    assert any(
        issue["code"] == "DIV001"
        for issue in result["issues"]
    )


def test_detect_eval_and_exec():
    code = """
x = eval("10 + 20")
exec("print('hello')")
"""
    result = analyze_bug_patterns(code)

    codes = [issue["code"] for issue in result["issues"]]

    assert "SEC001" in codes
    assert "SEC002" in codes


def test_detect_mutable_default():
    result = analyze_bug_patterns("def greet(items=[]): pass")

    assert any(
        issue["code"] == "BUG001"
        for issue in result["issues"]
    )


def test_detect_unsafe_exception_handlers():
    code = """
try:
    print("hello")
except:
    pass
"""
    result = analyze_bug_patterns(code)

    codes = [issue["code"] for issue in result["issues"]]

    assert "BUG002" in codes
    assert "BUG003" in codes


def test_invalid_syntax_is_skipped():
    result = analyze_bug_patterns("def broken(")

    assert result["status"] == "skipped"
    assert result["issues"] == []


def test_bug_patterns_reach_final_report():
    code = "result = 10 / 0"

    analysis = detect_bugs(code)
    report = generate_report(analysis)

    assert report["status"] == "completed"
    assert any(
        finding.get("code") == "DIV001"
        for finding in report["findings"]
    )
