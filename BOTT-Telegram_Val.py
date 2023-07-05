import telebot
import csv 
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from parsing import exchanger_currency
from text import text_start

TOKEN = ''

bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('Рассылка', 'Админ панель', 'Курсы валют')
keyboard.add('Тех.поддержка',)

list_1 = [1008889358, 5949761485, 5647517221, 5873445472,705754682,346706198]

@bot.message_handler(commands=['start','help', '123'])
def hello_bot(message):
    with open('IDs.csv','r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        user_id = [str(message.from_user.id),str(message.from_user.first_name)]
        check_user =  list(reader)
        if  user_id not in check_user:
            with open('IDs.csv','a') as file:
                writer = csv.writer(file)
                writer.writerow([message.from_user.id, message.from_user.first_name])
                bot.send_message(message.from_user.id, text=text_start, reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, text='Привет ты есть в базе', reply_markup=keyboard)


@bot.message_handler(commands=['info'])
def info_bot(message):
    if message.from_user.id == 5873445472:
        for item in list_1:
            try:
                bot.send_message(chat_id=item, text='Рассылка от Атоша')
            except Exception:
                continue

        bot.send_message(message.from_user.id, text='Рассылка успешно отправлена') 
    else:
        bot.send_message(message.from_user.id, text='Рассылка недоступна')


@bot.message_handler(commands=['admin'])
def admin_bot(message):
    print(message.from_user.first_name)
    if message.from_user.id == 5873445472:
        bot.reply_to(message, 'Привет админ')
        list_id = []
        with open('database.txt','r') as file:
            display = file.read()
            bot.reply_to(message, f'Все пользователи бота: \n\n{display}')  
            list_id.append(display)
        with open('database.txt','r') as file:
            display_ID = file.readlines()
        for ids in display_ID:
            bot.send_message(chat_id=ids, text='Рассылка от Атоша')      
    else:
        bot.reply_to(message, 'Вы не админ')


@bot.message_handler(content_types=['text'])
def message_text(message):
    if message.text == 'Тех.поддержка':
        bot.send_message(message.from_user.id, text='Связаться с тех поддержкой можно по ссылке\n\n@Xxxanderrrs')

    elif message.text == 'Рассылка':
        info_bot(message)

    elif message.text == 'Админ панель':
        admin_bot(message)
    
    elif message.text == 'Курсы валют':
        currency = exchanger_currency()
        currency_list = []
        for key, value in currency.items():
            result = f'{key}-{value}'
            currency_list.append(result)
        text = '\n'.join(currency_list)
        bot.send_message(message.from_user.id, text=f'Курсы валют\n\n{text}')


if __name__ == '__main__':
    bot.polling()