import requests
from configs import url, token, weather_api  # сторонний py с данными
from time import sleep
import datetime

greetings = ('здравствуй', 'привет', 'ку', 'здорово', 'hi', 'хай', 'good morning', 'gutten morgen', 'q')
weather = ('погода', 'прогноз погоды', 'погоды', 'температура', 'ветер', 'атмосферное давление')
Yekaterinburg = ('ёбург','екатеринбург', 'екб', 'свердловск', 'столица урала')
Moskow = ('москва','моква','москоу','столица')
Petersburg = ('питер','болото','культурная столица','питербург','петербург','петер','пита') 
now = datetime.datetime.now()

class Bot_handler:
	def __init__(self,token):
		self.token = token
		self.api_url = url
		self.weather_api = weather_api
	def get_updates_json(self, request, offset=None, timeout=30):
		params = {'timeout': timeout, 'offset': offset}
		method = 'getUpdates'
		response = requests.get(self.api_url + method,data = params)
		result_json = response.json()['result']
		return result_json
	def last_update(self):
		return self.get_updates_json(self.api_url)[-1]
	def get_chat_id(update):
		return update['message']['chat']['id']
	def get_user_name(update): 
		return update['message']['chat']['first_name']
	def send_message(self, chat, text):
		params = {'chat_id': chat, 'text': text}
		return requests.post(self.api_url + 'sendMessage', data = params)
	def weather_func(self, s_city, last_chat_id):
		#params = {'q': f'{s_city}', 'type': 'like', 'units': 'metric', 'lang': 'ru', 'appid': '0d176d252a549c178c6492a3eebd6606'}
		weather = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={s_city}&lang=ru&units=metric&appid=0d176d252a549c178c6492a3eebd6606').json()
		city = weather['name']
		climat = weather['weather'][0]['description']
		temperature = weather['main']['temp']
		fl_temperature = weather['main']['feels_like']
		self.send_message(last_chat_id, f'Город: {city} \nКлимат: {climat}\nТемпература: {temperature} , но ощущается как {fl_temperature} ')
		
_1st_bot = Bot_handler(token)  # bot initialization



def main():
	new_message= 0
	new_offset = None
	weather_coef = 0
	today = now.day
	hour = now.hour
	while True:
		_1st_bot.get_updates_json(new_offset)
		last_update = _1st_bot.last_update() # Class function to get last update
		last_update_id = last_update['update_id']
		last_chat_text = last_update['message']['text']
		last_chat_id = last_update['message']['chat']['id']
		last_chat_name = last_update['message']['chat']['first_name']
		current_message = last_update['message']['message_id']

		if new_message == 0 or new_message <= current_message:
			if last_chat_text.lower() == '777':
				_1st_bot.send_message(last_chat_id,f'{last_chat_name}, иди нахуй, ебаное казино бл ')
				new_message = current_message + 2
			if last_chat_text.lower() in weather:
				_1st_bot.send_message(last_chat_id, f'{last_chat_name}, в каком городе узнать погоду?')
				new_message = current_message + 2
				weather_coef = 1
			if weather_coef == 1:
				if last_chat_text.lower() in Yekaterinburg:
					_1st_bot.weather_func('Yekaterinburg',last_chat_id)
					weather_coef=0
				elif last_chat_text.lower() in Moskow:
					_1st_bot.weather_func('Moskva',last_chat_id)
					weather_coef=0
				elif last_chat_text.lower() in Petersburg:
					_1st_bot.weather_func('Saint Petersburg',last_chat_id)
					weather_coef=0


		new_offset = last_update_id + 1



if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()