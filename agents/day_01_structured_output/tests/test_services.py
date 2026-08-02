from unittest.mock import MagicMock, patch
from agents.day_01_structured_output.services import get_structured_llm

@patch("agents.day_01_structured_output.services.get_llm")
def test_get_structured_llm_service(mock_get_llm):
    mock_llm = MagicMock()
    mock_get_llm.return_value = mock_llm

    get_structured_llm()

    mock_get_llm.assert_called_once()
    mock_llm.with_structured_output.assert_called_once()
