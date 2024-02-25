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
        bot.send_message(message.from_user.id, "Bitte geben Sie a_1_1 ... a_n_n");
        bot.send_message(message.from_user.id, "wissen das: ")
        bot.send_message(message.from_user.id, "1) a_1_1*x + a_1_2*y = a_1_3");
        bot.send_message(message.from_user.id, "2) a_2_1*x + a_2_2*y = a_2_3");
        bot.send_message(message.from_user.id, "Bitte füllen mit Raum und wenn Sie nicht ganze Zahlen haben, dann schreiben Sie mit dem Punkt");
        bot.send_message(message.from_user.id, "Zum Beispiel:")
        bot.send_message(message.from_user.id, "a_1_1 = 4.4 a_1_2 = 5 a_1_3 = 1.5 a_2_1 = 8 a_2_2 = -2 a_2_3 = 38.75");
        bot.send_message(message.from_user.id, "Wird aussehen wie")
        bot.send_message(message.from_user.id, "1) 4*x + 5*y = 1");
        bot.send_message(message.from_user.id, "2) 8*x - 2*y = 38");
        bot.send_message(message.from_user.id, "Antwort:")
        bot.send_message(message.from_user.id, "x = 4.031762295081967 und y = -3.2479508196721314");

    else:
        bot.send_message(message.from_user.id, "Bitte geben Sie a_1_1, ... a_n_n");
        bot.send_message(message.from_user.id, "wissen das: 1) a_1_1*x_1 + a_1_2*x_2 + ... + a_1_n = 0");
        bot.send_message(message.from_user.id, "            2) a_2_1*x_1 + a_2_2*x_2 + ... + a_2_n = 0");
        bot.send_message(message.from_user.id, "            ..........................................");
        bot.send_message(message.from_user.id, "            n) a_n_1*x_1 + a_n_2*x_2 + ... + a_n_n = 0");

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
    if(Menge == 2):
        LoesenSys_2d(message, bot, variablen);
    else:
        LoesenSys_nd(message, bot, variablen)

def LoesenSys_2d(message, bot, variablen):
    Delta = float(variablen['a_1_1'])*float(variablen['a_2_2']) - float(variablen['a_2_1'])*float(variablen['a_1_2']);
    DeltaX = float(variablen['a_1_3'])*float(variablen['a_2_2']) - float(variablen['a_2_3'])*float(variablen['a_1_2']);
    DeltaY = float(variablen['a_1_1'])*float(variablen['a_2_3']) - float(variablen['a_2_1'])*float(variablen['a_1_3']);

    x = DeltaX / Delta;
    y = DeltaY / Delta;

    bot.send_message(message.from_user.id, f"x = {x} und y = {y}")

def LoesenSys_nd(message, bot, variablen):
    print(0);
