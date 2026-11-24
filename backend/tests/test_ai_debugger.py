from unittest.mock import patch

from app.services.ai.ai_debugger import analyze_with_ai


def test_missing_api_key():
    with patch("app.services.ai.ai_debugger.API_KEY", None):
        result = analyze_with_ai("print('hello')", {})

    assert result["status"] == "unavailable"


def test_gemini_success():
    mock_response = type(
        "Response",
        (),
        {"text": "The code prints hello."}
    )()

    with patch("app.services.ai.ai_debugger.API_KEY", "test-key"), \
         patch("app.services.ai.ai_debugger.genai.Client") as mock_client:

        mock_client.return_value.models.generate_content.return_value = mock_response

        result = analyze_with_ai("print('hello')", {})

    assert result["status"] == "success"
    assert "hello" in result["explanation"]


def test_gemini_unavailable():
    with patch("app.services.ai.ai_debugger.API_KEY", "test-key"), \
         patch("app.services.ai.ai_debugger.genai.Client") as mock_client:

        mock_client.return_value.models.generate_content.side_effect = Exception(
            "Service unavailable"
        )

        result = analyze_with_ai("print('hello')", {})

    assert result["status"] == "unavailable"
