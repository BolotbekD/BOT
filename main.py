import telebot
import csv
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from test22 import exchanger_currency
from text import text_start
from database import Database
TOKEN = ''

bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('Рассылка', 'Админ панель')
keyboard.add('Курсы валют')
keyboard.add('Техподдержка')

keyboard_url = InlineKeyboardMarkup()
instagram_url = InlineKeyboardButton(text='Instagram', url='https://www.google.com/search?q=%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4%D1%87%D0%B8%D0%BA&oq=&aqs=chrome.1.69i59i450l8.13697524j0j15&sourceid=chrome&ie=UTF-8')
telegram_url = InlineKeyboardButton(text='Telegram', url='https://t.me/Xxxanderrrs')
keyboard_url.add(instagram_url, telegram_url)


list_1 = [573015206, 5949761485, 5647517221, 5873445472]

@bot.message_handler(commands=['start','help', '123'])
def hello_bot(message):
    db = Database()
    db.connect()
    db.create_user_table()
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    chek = db.check_user(user_id)
    if chek:
        bot.send_message(message.from_user.id, text='Привет ты есть в базе', reply_markup=keyboard)
    else:
        db.insert_user(first_name, user_id)
        bot.send_message(message.from_user.id, text='Привет ты прошел регистрацию', reply_markup=keyboard)

    db.close()


@bot.message_handler(commands=['info'])
def info_bot(message):
    db = Database()
    db.connect()
    user_list = db.mailing_message()
    if message.from_user.id==1008889358:
        for item in  user_list:
            print(item)
            try:
                bot.send_message(chat_id= item[0], text='рассылка от Дастан')
            except Exception:
                continue

        bot.send_message(message.from_user.id, text='Рассылка успешно отправлено')
    else:
        bot.reply_to(message, 'Верни админа')

    db.close()


@bot.message_handler(commands=['admin'])
def admin_bot(message):
    db = Database()
    db.connect()
    all_user = db.all_user()
    if message.from_user.id == 1008889358:
        bot.reply_to(message, 'Привет админ')
        text = 'Все пользователи бота\n'
        for users in all_user:
            text += f'{users[0]}\n'
        bot.send_message(message.from_user.id, text= text)

    else:
        bot.reply_to(message, 'ты не админ')

    

@bot.message_handler(content_types=['text'])
def message_text(message):
    first_name = message.from_user.first_name
    msg = message.text
    with open('message_text.txt', 'a') as file:
           file.write(f'от пользователя: {first_name} Сообщение: {msg}\n')
    if message.text == 'Техподдержка':
        bot.send_message(message.from_user.id, text='Связаться с тех поддержкой можно по ссылке\n@dfassdf',reply_markup= keyboard_url)
    elif message.text == 'Рассылка':
        info_bot(message)
    elif message.text == 'Админ панель':
        admin_bot(message)
    elif message.text == 'Курсы валют':
        currency = exchanger_currency()
        currency_list = []
        for key, value in currency.items():
            result = f'{key} - {value}'
            currency_list.append(result)
        text = '\n'.join(currency_list)

        bot.send_message(message.from_user.id, text=f'Курсы валют\n\n{text}')
        

if __name__=='__main__':
    bot.polling(non_stop=True)
    