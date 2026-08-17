
from pydantic import BaseModel


class CalculatorArgs(BaseModel):
    expression: str


class WeatherArgs(BaseModel):
    city: str


class HttpGetArgs(BaseModel):
    url: str


class WordCountArgs(BaseModel):
    text: str