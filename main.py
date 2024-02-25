import telebot;
import quadratischeGleichung;
import system_linearerGleichungen;

bot = telebot.TeleBot('6705889567:AAGCti5hXgg034SjUFtBYntfGxl7bOzNF70');


@bot.message_handler(content_types=['text'])
def Start(message):
    bot.send_message(message.from_user.id, 'Serwus..');

    user_markup = telebot.types.ReplyKeyboardMarkup(True);
    user_markup.row('System linearer Gleichungen');
    user_markup.row('Quadratische Gleichung');
    user_markup.row('Mathematisch-physikalische Gleichung der Saitenschwingung');
    user_markup.row('Mathematisch-physikalische Gleichung der Wärmeleitfähigkeit einer Platte');
    user_markup.row('Mathematisch-physikalische Gleichung der Wärmeleitfähigkeit eines Stabes');

    if message.text == 'Quadratische Gleichung':
        return quadratischeGleichung.Start(message, bot);
    elif message.text == 'Quadratische Gleichung':
        return system_linearerGleichungen.Start(message, bot);

bot.polling(none_stop=True, interval=0);
