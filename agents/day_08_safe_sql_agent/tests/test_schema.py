"""Unit tests for schema formatting and introspection in Safe SQL Agent."""

from agents.day_08_safe_sql_agent.database.schema import format_schema, get_columns


def test_format_schema():
    sample_schema = {
        "products": {
            "columns": [
                {"name": "id", "type": "integer", "nullable": False},
                {"name": "title", "type": "varchar", "nullable": True},
            ],
            "relationships": [],
        }
    }

    formatted = format_schema(sample_schema)
    assert "DATABASE SCHEMA" in formatted
    assert "TABLE: products" in formatted
    assert "id: integer NOT NULL" in formatted
    assert "title: varchar" in formatted


def test_get_columns_signature(mocker):
    # Mock connection to avoid needing real database
    mock_conn = mocker.patch("agents.day_08_safe_sql_agent.database.schema.get_connection")
    mock_cursor = mocker.MagicMock()
    mock_conn.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("users", "id", "integer", "NO")]

    res = get_columns()
    assert len(res) == 1
    assert res[0]["column"] == "id"
