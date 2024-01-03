from pydantic import BaseModel


class WeatherInfo(BaseModel):
    city: str
    weather: str
    temperature: int
    wind: float
