import telebot;
import math;
import re;

def Start(message, bot):
    bot.send_message(message.from_user.id, "Bitte geben Sie wie viel Gleichungen Sie haben");
    bot.register_next_step_handler(message, MengeG, bot);

def MengeG (message, bot):
    Menge = int(message.text)
    if(Menge == 0 or Menge == 1):
        bot.send_message(message.from_user.id, "Entschuldigung! Es ist nich system!");
    elif(Menge == 2):
        bot.send_message(message.from_user.id, "Bitte geben Sie a_1_1, ... a_n_n");
        bot.send_message(message.from_user.id, "wissen das: 1) a_1_1*x + a_1_2*y = 0");
        bot.send_message(message.from_user.id, "            2) a_2_1*x + a_2_2*y = 0");
        bot.register_next_step_handler(message, SuchenInt, bot, Menge);
    else:
        bot.send_message(message.from_user.id, "Bitte geben Sie a_1_1, ... a_n_n");
        bot.send_message(message.from_user.id, "wissen das: 1) a_1_1*x_1 + a_1_2*x_2 + ... + a_1_n*x_n = 0");
        bot.send_message(message.from_user.id, "            2) a_2_1*x_1 + a_2_2*x_2 + ... + a_2_n*x_n = 0");
        bot.send_message(message.from_user.id, "            ..........................................");
        bot.send_message(message.from_user.id, "            n) a_n_1*x_1 + a_n_2*x_2 + ... + a_n_n*x_n = 0");
        bot.register_next_step_handler(message, SuchenInt, bot, Menge);

def SuchenInt(message, bot, Menge):
    pattern = r'(\w+)\s*=\s*([^ ]+)';
    Uebereinstimmen = re.findall(pattern, message.text);
    variablen = {};
    for Uebereinstimm in Uebereinstimmen:
        Name, Wert = Uebereinstimm
        print(Name)
        print(Wert)
        variablen[Name] = Wert
