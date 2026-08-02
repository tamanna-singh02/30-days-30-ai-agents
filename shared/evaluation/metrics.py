from typing import Any, Dict

def evaluate_extraction(expected: Dict[str, Any], actual: Dict[str, Any]) -> float:
    """
    Computes key matching accuracy between expected and actual extracted dictionary fields.
    """
    if not expected:
        return 1.0 if not actual else 0.0
    matches = 0
    total = len(expected)
    for key, expected_val in expected.items():
        if key in actual and actual[key] == expected_val:
            matches += 1
    return round(matches / total, 4)
