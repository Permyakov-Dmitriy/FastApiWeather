from aiohttp import ClientSession

from .config import settings


async def get_weather(city):
    async with ClientSession() as session:
        url = settings.URL_API_WEATHER
        params = {'q': city, 'APPID': settings.TOKEN}

        async with session.get(url=url, params=params) as res:
            weather_json = await res.json()

            return {
                'city': weather_json['name'],
                'weather': weather_json["weather"][0]["main"],
                'temperature': int(weather_json["main"]["temp"] - 273.15),
                'wind': weather_json["wind"]["speed"]
            }