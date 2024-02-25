import telebot;
import math;


def Start(message, bot):
    bot.send_message(message.from_user.id, "Bitte geben Sie a b c ein, wissen das ax² + bx + c = 0");
    bot.send_message(message.from_user.id, "Bitte geben Sie a");
    bot.register_next_step_handler(message, GebenA, bot);

def GebenA(message, bot):
    a = int(message.text);

    if(a == 0):
        bot.send_message(message.from_user.id, "Entschuldigung! Es ist nich quadratische gleichung!");
    else:
        bot.send_message(message.from_user.id, "Bitte geben Sie b");
        bot.register_next_step_handler(message, GebenB, bot, a);

def GebenB(message, bot, a):
    b = int(message.text);

    bot.send_message(message.from_user.id, "Bitte geben Sie c");
    bot.register_next_step_handler(message, GebenC, bot, a, b);

def GebenC(message, bot, a, b):
    c = int(message.text);

    bot.send_message(message.from_user.id, f"Ihre Gleichung ist {a}x² + {b}x + {c} = 0?");
    bot.register_next_step_handler(message, Leosung, bot, a, b, c);

def Leosung(message, bot, a, b, c):
    if(message.text == 'ja' or message.text == 'Ja'or message.text == 'jö' or message.text == 'Jö' or message.text == '1'):
        D = b**2 - 4*a*c;
        if (D > 0):
            x_1 = (-b + math.sqrt(D))/(2*a);
            x_2 = (-b - math.sqrt(D))/(2*a);
            bot.send_message(message.from_user.id, f"D = {D}, dann x_1 = {x_1} und x_2 = {x_2} ist");

        elif(D == 0):
            x = -b/(2*a);
            bot.send_message(message.from_user.id, f"D = {D}, dann nür eine Wurzel x = {x} ist");
        else:
            bot.send_message(message.from_user.id, f"D = {D}, dann keine Wurzel ist");

    else:
        Start(message, bot)
