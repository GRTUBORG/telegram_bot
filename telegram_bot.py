import telebot
import pymorphy2

from covid import Covid
from pyowm import OWM
from pyowm.utils.config import get_default_config
from translate import Translator

bot = telebot.TeleBot("1483059988:AAFQaZeheQXtBWSVnn4OY2hh6BoxfqBE3ek")
print('Бот работает!')

@bot.message_handler(commands = ['start'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Пока что я тестовый бот и ничего не умею, но скоро во мне будет очень много строк кода, так что попрошу немного подождать :)\n"
                          "Держи мои команды:\n1) /covid [country]\n2) /weather [город]")
@bot.message_handler(commands = ['help'])
def send_help(message):
	bot.reply_to(message, "Привет! Вот все мои команды:\n1) /covid [страна]\n2) /weather [город]")

@bot.message_handler(func = lambda m: True)
def weather_command_message(message):
    if str(message.text)[:8] == '/weather':
        city = str(message.text)[9:]
        city = str(city)
        if city == "":
            city = 'Москва'
        morph = pymorphy2.MorphAnalyzer()
        counties = morph.parse(city)[0]
        gent = counties.inflect({'loct'})
        gent_new = gent.word
        gent_correct = gent_new.capitalize()
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = OWM('0d16f6ffb7d46c30c1202a765e2cb0fc', config_dict)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        w = observation.weather
        cloud = str(w.detailed_status)
        clouds = str(w.clouds) 
        temp = w.temperature('celsius')['temp']
        temperature = str(temp).rsplit(".")[0]
        weather_message = (f'Сейчас в {gent_correct} {temperature} °C\n'
                           f'Небо затянуто на {clouds}%, {cloud}')
        bot.send_message(message.from_user.id, weather_message)
    elif str(message.text)[:6] == '/covid':
        bot.send_message(message.from_user.id, "Пожалуйста, подождите, собираю статистику...")
        country = str(message.text)[7:]
        country = str(country)
        if country == "":
            country = 'россия'
        translator = Translator(from_lang = "ru", to_lang = "en")
        translation = translator.translate(country)
        morph = pymorphy2.MorphAnalyzer()
        counties = morph.parse(country)[0]
        gent = counties.inflect({'gent'})
        gent_new = gent.word
        gent_correct = gent_new.capitalize()
        covid = Covid(source = "worldometers")
        country_cases = covid.get_status_by_country_name(translation)['new_cases']
        if country_cases == 0:
            country_cases = 'Статистика обновляется. Попробуйте заново через несколько часов.'
        else:
            country_cases = '+' + str(country_cases)
        confirmed_country_cases = covid.get_status_by_country_name(translation)['confirmed']
        deaths_country_cases = covid.get_status_by_country_name(translation)['deaths']
        covid_message = (f'Статистика для {gent_correct}:\n'
                         f'Всего заболевших за сутки: {country_cases}\n'
                         f'Всего случаев: {confirmed_country_cases}\n'
                         f'Зафиксировано смертей: {deaths_country_cases}')
        bot.send_message(message.from_user.id, covid_message)
    else:
        bot.send_message(message.from_user.id, "Я пока что не знаю, что мне на это ответить. Пожалуйста, пропиши команду /help")


bot.polling(none_stop = True)
