import telebot
from covid import Covid

bot = telebot.TeleBot("1483059988:AAFQaZeheQXtBWSVnn4OY2hh6BoxfqBE3ek")
print('Бот работает!')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Пока что я тестовый бот и ничего не умею, но скоро во мне будет очень много строк кода, так что попрошу немного подождать :)\n"
                          "Держи мою первую команду: /covid [country]")

@bot.message_handler(func=lambda m: True)
def echo_message(message):
    if str(message.text)[:6] == '/covid':
        country = str(message.text)[7:]
        country = str(country)
        if country == "":
            country = 'russia'
        bot.send_message(message.from_user.id, "Пожалуйста, подождите, собираю статистику...")
        covid = Covid(source = "worldometers")
        country_cases = covid.get_status_by_country_name(country)['new_cases']
        if country_cases == 0:
            country_cases = 'Статистика обновляется. Попробуйте заново через несколько часов.'
        else:
            country_cases = '+' + str(country_cases)
        confirmed_country_cases = covid.get_status_by_country_name(country)['confirmed']
        deaths_country_cases = covid.get_status_by_country_name(country)['deaths']
        covid_message = (f'Всего заболевших за сутки: {country_cases}\n'
                         f'Всего случаев: {confirmed_country_cases}\n'
                         f'Зафиксировано смертей: {deaths_country_cases}')
        bot.send_message(message.from_user.id, covid_message)
    else:
        bot.send_message(message.from_user.id, "Я пока что не знаю, что мне на это ответить. Пожалуйста, пропиши команду /covid")

bot.polling(none_stop = True)
