from app.tool import Tool
from app.tool_registry import ToolRegistry

from app.schemas import (
    CalculatorArgs,
    WeatherArgs,
    HttpGetArgs,
    WordCountArgs,
)

from app.tools.string_tools import (
    word_count,
)

from app.tools.calculator import calculate
from app.tools.weather import get_weather
from app.tools.http import http_get


registry = ToolRegistry()


registry.register(
    Tool(
        name="calculate",
        description="Evaluate a mathematical expression.",
        schema=CalculatorArgs,
        handler=calculate,
        risk_level="low",
        timeout=5,
        category="computation",
    )
)


registry.register(
    Tool(
        name="get_weather",
        description="Get the current weather for a city.",
        schema=WeatherArgs,
        handler=get_weather,
        risk_level="low",
        timeout=10,
        category="information",
    )
)


registry.register(
    Tool(
        name="http_get",
        description="Make an HTTP GET request to an allowed URL.",
        schema=HttpGetArgs,
        handler=http_get,
        risk_level="medium",
        timeout=10,
          
    )
)

registry.register(
    Tool(
        name="word_count",
        description="Count the number of words in text.",
        schema=WordCountArgs,
        handler=word_count,
        risk_level="low",
        timeout=2,
    )
)