import telebot
import os

from covid import Covid


token = os.environ.get('bot_token')
bot = telebot.TeleBot(str(token))
print('Бот работает!')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Пока что я тестовый бот и ничего не умею, но скоро во мне будет очень много строк кода, так что попрошу немного подождать :)\n"
                          "Держи мою первую команду: /covid")

@bot.message_handler(func=lambda m: True)
def echo_message(message):
    if message.text == '/covid' or '/cov':
        bot.send_message(message.from_user.id, "Пожалуйста, подождите, собираю статистику для России...")
        covid = Covid(source = "worldometers")
        country_cases = covid.get_status_by_country_name('Russia')['new_cases']
        confirmed_country_cases = covid.get_status_by_country_name('Russia')['confirmed']
        deaths_country_cases = covid.get_status_by_country_name('Russia')['deaths']
        covid_message = (f'Всего заболевших за сутки: +{country_cases}\n'
                         f'Всего случаев для России: {confirmed_country_cases}\n'
                         f'Зафиксировано смертей: {deaths_country_cases}')
        bot.send_message(message.from_user.id, covid_message)

bot.polling(none_stop=True)
