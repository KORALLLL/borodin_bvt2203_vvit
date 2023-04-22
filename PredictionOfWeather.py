import requests

city = 'Moscow,RU'
appid = 'dae7cd5beefc51073f6396e826b827db'

res = requests.get("http://api.openweathermap.org/data/2.5/weather",
 params={'q':city, 'units':'metric', 'lang':'ru', 'APPID':appid})
data = res.json()


print('city ', city)
print('погодные условия ', data['weather'][0]['description'])
print('температура ', data['main']['temp'])
print('минимальная температура', data['main']['temp_min'])
print('максимальная температура', data['main']['temp_max'])
print('скорость ветра ', data['wind']['speed'])
print('видимость', data['visibility'])

res = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=
{'q':city, 'units':'metric', 'land':'ru','APPID':appid})
data = res.json()

for i in data['list']:
    print('Дата<', i['dt_txt'], '>\r\nТемпература<', '{0:3.0f}'.format(i['main']['temp']), 
    ">\r\nПогодные условия<", i['weather'][0]['description'], '>')
    print('Скорость ветра<', '{0:3.0f}'.format(i['wind']['speed']), '>')
    print('Видимость<', i['visibility'], '>')
    print('_______________________________________________')