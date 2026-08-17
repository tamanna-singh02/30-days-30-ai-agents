
import requests
from pydantic import BaseModel


class WeatherArgs(BaseModel):
    city: str


def get_weather(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    try:
        url = "https://wttr.in"

        response = requests.get(
            f"{url}/{city}",
            params={
                "format": "j1"
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        current = data["current_condition"][0]

        temperature = current["temp_C"]
        humidity = current["humidity"]
        description = current["weatherDesc"][0]["value"]

        return (
            f"Weather in {city}: "
            f"{description}, "
            f"{temperature}°C, "
            f"humidity {humidity}%."
        )

    except requests.RequestException as e:
        return f"Weather API error: {str(e)}"

    except (KeyError, IndexError, TypeError) as e:
        return f"Invalid weather API response: {str(e)}"