import telebot;
import math;
import re;
import numpy as np;

def Start(message, bot):
    bot.send_message(message.from_user.id, "Bitte geben Sie wie viel Gleichungen Sie haben");
    bot.register_next_step_handler(message, MengeG, bot);

def MengeG (message, bot):
    Menge = int(message.text)
    if(Menge == 0 or Menge == 1):
        bot.send_message(message.from_user.id, "Entschuldigung! Es ist nich system!");
    elif(Menge == 2):
        bot.send_message(message.from_user.id, "Bitte geben Sie a_1_1 ... a_n_n");
        bot.send_message(message.from_user.id, "wissen das: ");
        bot.send_message(message.from_user.id, "1) a_1_1*x + a_1_2*y = a_1_3");
        bot.send_message(message.from_user.id, "2) a_2_1*x + a_2_2*y = a_2_3");
        bot.send_message(message.from_user.id, "Bitte füllen mit Raum und wenn Sie nicht ganze Zahlen haben, dann schreiben Sie mit dem Punkt");
        bot.send_message(message.from_user.id, "Zum Beispiel:");
        bot.send_message(message.from_user.id, "a_1_1 = 4.4 a_1_2 = 5 a_1_3 = 1.5 \n a_2_1 = 8 a_2_2 = -2 a_2_3 = 38.75");
        bot.send_message(message.from_user.id, "Wird aussehen wie");
        bot.send_message(message.from_user.id, "1) 4.4*x + 5*y = 1.5");
        bot.send_message(message.from_user.id, "2) 8*x - 2*y = 38.75");
        bot.send_message(message.from_user.id, "Antwort:");
        bot.send_message(message.from_user.id, "x = 4.031762295081967 und y = -3.2479508196721314");

    else:
        bot.send_message(message.from_user.id, "Bitte geben Sie a_1_1, ... a_n_n");
        bot.send_message(message.from_user.id, "wissen das:");
        bot.send_message(message.from_user.id, "1) a_1_1*x_1 + a_1_2*x_2 + ... + a_1_n*x_n = B_1");
        bot.send_message(message.from_user.id, "2) a_2_1*x_1 + a_2_2*x_2 + ... + a_2_n*x_n = B_2");
        bot.send_message(message.from_user.id, "................................................");
        bot.send_message(message.from_user.id, "n) a_n_1*x_1 + a_n_2*x_2 + ... + a_n_n*x_n = B_n");
        bot.send_message(message.from_user.id, "Bitte füllen mit Raum und wenn Sie nicht ganze Zahlen haben, dann schreiben Sie mit dem Punkt");
        bot.send_message(message.from_user.id, "Zum Beispiel:");
        bot.send_message(message.from_user.id, "a_1_1 = 4.4 a_1_2 = 5 a_1_3 = 1.5 a_1_4 = 3\n a_2_1 = 8 a_2_2 = -2 a_2_3 = 7.75 a_2_4 = 38.75 \n a_3_1 = 6 a_3_2 = 1 a_3_3 = 1.5 a_3_4 = 6");
        bot.send_message(message.from_user.id, "Wird aussehen wie");
        bot.send_message(message.from_user.id, "1) 4.4*x_1 + 5*x_2 + 1.5*x_3 = 3");
        bot.send_message(message.from_user.id, "2) 8*x_1 - 2*x_2 + 7.75*x_3 = 38.75");
        bot.send_message(message.from_user.id, "3) 6*x_1 + 1*x_2 + 1.5*x_3 = 6");
        bot.send_message(message.from_user.id, "Antwort:");
        bot.send_message(message.from_user.id, "x_1, x_1, ... x_3 = [-0.09181701 -0.7867268   4.89175258]");

    bot.register_next_step_handler(message, SuchenInt, bot, Menge);

def SuchenInt(message, bot, Menge):
    pattern = r'(\w+)\s*=\s*([^ \n]+)';
    Uebereinstimmen = re.findall(pattern, message.text);
    variablen = {};
    for Uebereinstimm in Uebereinstimmen:
        Name, Wert = Uebereinstimm
        print(Name)
        print(Wert)
        variablen[Name] = float(Wert);
    if(Menge == 2):
        LoesenSys_2d(message, bot, variablen);
    else:
        LoesenSys_nd(message, bot, variablen, Menge)

def LoesenSys_2d(message, bot, variablen):
    Delta = variablen['a_1_1']*variablen['a_2_2'] - variablen['a_2_1']*variablen['a_1_2'];
    DeltaX = variablen['a_1_3']*variablen['a_2_2'] - variablen['a_2_3']*variablen['a_1_2'];
    DeltaY = variablen['a_1_1']*variablen['a_2_3'] - variablen['a_2_1']*variablen['a_1_3'];

    x = DeltaX / Delta;
    y = DeltaY / Delta;

    bot.send_message(message.from_user.id, f"x = {x} und y = {y}")

def LoesenSys_nd(message, bot, variablen, Menge):
    K_M = np.array(list(variablen.values()));
    K_M_2d = K_M.reshape((Menge, -1));
    B_n = K_M_2d[:, -1];
    A_n_n = K_M_2d[:, :-1];

    print(K_M_2d);
    print();
    print(B_n);
    print();
    print(A_n_n);

    Solve = np.linalg.solve(A_n_n, B_n)
    bot.send_message(message.from_user.id, f"x_1, x_2, ... x_{Menge} = {Solve}");
