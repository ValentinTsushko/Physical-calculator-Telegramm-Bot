import telebot;
import os
import quadratischeGleichung;
import system_linearerGleichungen;
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("MY_API_KEY")

bot = telebot.TeleBot(api_key);


@bot.message_handler(content_types=['text'])
def Start(message):
    bot.send_message(message.from_user.id, 'Servus!');
    create_keyboard(message, bot);

def create_keyboard(message, bot):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('System linearer Gleichungen')
    keyboard.add('Quadratische Gleichung')
    keyboard.add('Mathematisch-physikalische Gleichung der Saitenschwingung')
    keyboard.add('Mathematisch-physikalische Gleichung der Wärmeleitfähigkeit einer Platte')
    keyboard.add('Mathematisch-physikalische Gleichung der Wärmeleitfähigkeit eines Stabes')


    if (message.text == 'Quadratische Gleichung'):
        return quadratischeGleichung.Start(message, bot);
    elif (message.text == 'System linearer Gleichungen'):
        return system_linearerGleichungen.Start(message, bot);
    elif (message.text == 'Mathematisch-physikalische Gleichung der Saitenschwingung'):
        bot.send_message(message.from_user.id, 'Work in progress');
    elif (message.text == 'Mathematisch-physikalische Gleichung der Wärmeleitfähigkeit einer Platte'):
        bot.send_message(message.from_user.id, 'Work in progress');
    elif (message.text == 'Mathematisch-physikalische Gleichung der Wärmeleitfähigkeit eines Stabes'):
        bot.send_message(message.from_user.id, 'Work in progress');

bot.polling(none_stop=True, interval=0);
