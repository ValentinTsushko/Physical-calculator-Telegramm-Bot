import telebot
import math
import re

def start(message, bot):
    bot.send_message(message.from_user.id, "Please enter a b c, knowing that ax² + bx + c = 0\n"
    +"Please write it as shown in the example. If you have non-integer values, use a dot.\n"
    +"For example:");
    bot.send_message(message.from_user.id, "a = 1 b = 5.75 c = 4");
    bot.send_message(message.from_user.id, "Answer:\n"
    "D = 17.0625, then x_1 = -0.809661044767712 and x_2 = -4.9403389552322885");

    bot.register_next_step_handler(message, find_values, bot)

def find_values(message, bot):
    pattern = r'(\w+)\s*=\s*([^ \n]+)';
    matches = re.findall(pattern, message.text);
    variables = {};

    for match in matches:
        name, value = match;
        variables[name] = float(value);

    bot.send_message(message.from_user.id, f"Is your equation {variables['a']}x² "
    +f"+ {variables['b']}x + {variables['c']} = 0?");
    bot.register_next_step_handler(message, solution, bot, variables['a'], variables['b'], variables['c']);

def solution(message, bot, a, b, c):
    if message.text.lower() in ['ja', 'jö', 'jo', 'да', 'yes']:
        D = b**2 - 4*a*c;
        if (D > 0):
            x_1 = (-b + math.sqrt(D)) / (2*a);
            x_2 = (-b - math.sqrt(D)) / (2*a);
            bot.send_message(message.from_user.id, f"D = {D}, then x_1 = {x_1} and x_2 = {x_2}");

        elif (D == 0):
            x = -b / (2*a);
            bot.send_message(message.from_user.id, f"D = {D}, then only one root x = {x}");
        else:
            bot.send_message(message.from_user.id, f"D = {D}, then no roots");

    else:
        start(message, bot);
