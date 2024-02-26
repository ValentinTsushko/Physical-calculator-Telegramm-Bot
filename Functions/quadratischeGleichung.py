import telebot;
import math;
import re;


def Start(message, bot):
    bot.send_message(message.from_user.id, "Bitte geben Sie a b c ein, wenn wir wissen, dass ax² + bx + c = 0");
    bot.send_message(message.from_user.id, "Bitte schreiben Sie, wie im Beispiel, wenn Sie nicht ganze Zahlen haben, dann schreiben Sie mit dem Punkt");
    bot.send_message(message.from_user.id, "Zum Beispiel:");
    bot.send_message(message.from_user.id, "a = 1 b = 5.75 c = 4");
    bot.send_message(message.from_user.id, "Antwort:");
    bot.send_message(message.from_user.id, "D = 17.0625, dann x_1 = -0.809661044767712 und x_2 = -4.9403389552322885 ist");
    bot.register_next_step_handler(message, SuchenInt, bot);

def SuchenInt(message, bot):
    pattern = r'(\w+)\s*=\s*([^ \n]+)';
    Uebereinstimmen = re.findall(pattern, message.text);
    variablen = {};
    for Uebereinstimm in Uebereinstimmen:
        Name, Wert = Uebereinstimm;
        print(Name)
        print(Wert)
        variablen[Name] = float(Wert);

    bot.send_message(message.from_user.id, f"Ihre Gleichung ist {variablen['a']}x² + {variablen['b']}x + {variablen['c']} = 0?");
    bot.register_next_step_handler(message, Loesung, bot, variablen['a'], variablen['b'], variablen['c']);

def Loesung(message, bot, a, b, c):
    if(message.text == 'ja' or message.text == 'Ja'or message.text == 'jö' or message.text == 'Jö' or message.text == '1'or message.text == 'jo' or message.text == 'Jo'or message.text == 'да' or message.text == 'Да' or message.text == 'yes' or message.text == 'Yes'):
        D = b**2 - 4*a*c;
        if (D > 0):
            x_1 = (-b + math.sqrt(D))/(2*a);
            x_2 = (-b - math.sqrt(D))/(2*a);
            bot.send_message(message.from_user.id, f"D = {D}, dann x_1 = {x_1} und x_2 = {x_2} ist");

        elif(D == 0):
            x = -b/(2*a);
            bot.send_message(message.from_user.id, f"D = {D}, dann nur eine Wurzel x = {x} ist");
        else:
            bot.send_message(message.from_user.id, f"D = {D}, dann keine Wurzel sind");

    else:
        Start(message, bot)
