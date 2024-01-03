from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import asyncio

from .schemas import WeatherInfo
from .config import settings
from .utils import get_weather

from deep_translator import GoogleTranslator


app = FastAPI(
    title=settings.APP_NAME
)

app.mount('/static/', StaticFiles(directory='public', html=True))


@app.get('/')
def home():
    return RedirectResponse('/static/')


@app.get('/weather', response_model=WeatherInfo)
async def weather(city: str):
    trEng = GoogleTranslator(source='auto', target='en')

    city = trEng.translate(city)

    return await get_weather(city)


@app.get('/weather-major-cities', response_model=list[WeatherInfo])
async def weather_major_cities():
    tasks = [asyncio.create_task(get_weather(c)) for c in settings.LIST_MAJOR_CITIES]

    await asyncio.gather(*tasks)

    return [t.result() for t in tasks]
