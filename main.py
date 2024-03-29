

import telebot
from telebot import types
from config import *
import requests


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row("Поиск","Команды")
    bot.send_message(message.chat.id,f"Привет {message.from_user.username},выбери команду",reply_markup=menu)

@bot.message_handler(commands=["город"])
def city(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton("Бишкек")
    b2 = types.KeyboardButton("Москва")
    b3 = types.KeyboardButton("Берлин")
    b4 = types.KeyboardButton("/назад")
    menu.add(b1,b2,b3,b4)
    bot.send_message(message.chat.id,"Выбери город:",reply_markup=menu)

@bot.message_handler(commands=['Дата'])
def date(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton("Текущий прогноз погоды")
    b2 = types.KeyboardButton("Прогноз на неделю")
    b3 = types.KeyboardButton("/back")
    menu.add(b1,b2,b3)
    bot.send_message(message.chat.id,"Выберите опцию",reply_markup=menu)

@bot.message_handler(commands=["стоп"])
def heandle_stop(message):
    menu = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Заглядывай чаще!", reply_markup=menu)

@bot.message_handler(commands=["помощь"])
def heandle_help(message):
    bot.send_message(message.chat.id, """Мои возможности весьма спецефичны, но, ты тоько псомотри!
    Всё работает!!!""")

@bot.message_handler(commands=['назад'])
def back(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.row("Поиск","Команды")
    bot.send_message(message.chat.id,f"Привет {message.from_user.username},выбери команду",reply_markup=menu)

@bot.message_handler(content_types=["text"])
def heandle_text(message):
    if message.text == 'Команды':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('/старт', '/город', '/дата', '/помощь', '/стоп', '/назад')
        bot.send_message(message.chat.id, "Выбери команду: ", reply_markup=markup)
    elif message.text == 'Поиск':
        bot.send_message(message.chat.id, f'<b>Укажите город:</b>', parse_mode="html")
    else:
        try:
            a = open('weather.txt', 'a')
            CITY = message.text
            URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API}'
            data = requests.get(url=URL)
            print(data.text)
            a.write(data.text)
            response = requests.get(url = URL).json()
            city_info = {
                "city":CITY,
                'temp':response['main']['temp'],
                'weather':response['weather'][0]['description'],
                'wind':response['wind']['speed'],
                'pressure':response['main']['pressure'],
            }
            msg = f"<b><u>{CITY.upper()}</u></b>\n\n<b>Weather: {city_info['weather']}</b>\n----------------------------------\nTemperature: <b>{city_info['temp']} C</b>\n----------------------------------\nWind: <b>{city_info['wind']} m/s</b>\n----------------------------------\nPressure: <b>{city_info['pressure']}hPa</b>"
            bot.send_message(message.chat.id, msg, parse_mode="html")
        except:
            msg1 = f"<b> Nothing found to country. Try again</b>"
            bot.send_message(message.chat.id, msg1, parse_mode="html")



bot.polling(non_stop=True)