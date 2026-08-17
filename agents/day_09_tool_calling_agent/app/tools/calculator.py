from simpleeval import simple_eval


def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    """

    try:
        result = simple_eval(expression)

        return str(result)

    except Exception as e:
        return f"Calculation error: {str(e)}"