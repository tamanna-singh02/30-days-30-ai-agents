from agents.day_01_structured_output.graph import build_graph

def test_graph_compilation():
    """
    Test that the LangGraph workflow compiles cleanly.
    """
    graph = build_graph()
    assert graph is not None
