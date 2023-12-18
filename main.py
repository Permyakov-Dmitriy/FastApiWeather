from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import asyncio
from aiohttp import ClientSession
from deep_translator import GoogleTranslator
from model import db, User, History
from urllib.parse import unquote
from util import genToken
from sqlalchemy import desc

app = FastAPI()

app.mount('/static/', StaticFiles(directory='public', html=True))


@app.get('/')
def home():
    return RedirectResponse('/static/')


@app.get('/about')
def home():
    return RedirectResponse('/static/about.html')


@app.post('/sendWeather')
def sendHome(data = Body()):
    city = data.decode('UTF-8')

    tr = GoogleTranslator(source='auto', target='ru')
    trEng = GoogleTranslator(source='auto', target='en')

    city = trEng.translate(city)


    async def get_weather(city):
        async with ClientSession() as session:
            url = f'http://api.openweathermap.org/data/2.5/weather'
            params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}

            async with session.get(url=url, params=params) as res:
                weather_json = await res.json()
                return {'Погода': tr.translate(weather_json["weather"][0]["main"]),
                        'Температура': int(weather_json["main"]["temp"] - 273.15),
                        'Ветер': weather_json["wind"]["speed"]}


    async def main(city):
        task = asyncio.create_task(get_weather(city))

        await task

        return task.result()

    return asyncio.run(main(city))


@app.get('/getHistory')
def get_token(token):
    query = db.query(History).filter(History.token == token).order_by(desc(History.id)).limit(4).all()

    return {
        'history': query
    }


@app.post('/setToken')
def set_token(data = Body()):
    data = data.decode('UTF-8').split('=')
    token = data[1]
    res = ''

    if token == 'None':
        res = genToken()

        while db.query(User).filter(User.token == res).first():
            res = genToken()

        person = User(token=res)

        db.add(person)
        db.commit()

    return {
        'status': 'ok' if res else 'null',
        'token': res
    }


@app.post('/setHistory')
def set_history(data = Body()):
    string_data = unquote(data.decode('UTF-8')).replace('&', '=')
    arr_data = string_data.split('=')
    data = dict([(j, arr_data[((i * 2) + 1)]) for i, j in enumerate(arr_data[::2])])

    his = History(city=data['city'], weather=data['weather'], temp=int(data['temp']), wind=float(data['wind']), token=data['token'])

    db.add(his)
    db.commit()