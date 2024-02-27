import telebot
import math
import re
import os
import json

def load_translation(language):
    file_path = os.path.join('Translation', f'quadraticEquation_{language}.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations

def startQE(message, bot, current_language):
    translations = load_translation(current_language);
    bot.send_message(message.from_user.id, translations.get("Please_enter_text"));
    bot.send_message(message.from_user.id, "a = 1 b = 5.75 c = 4");
    bot.send_message(message.from_user.id, translations.get("Answer_text"));

    bot.register_next_step_handler(message, find_values, bot, translations, current_language)

def find_values(message, bot, translations, current_language):
    try:
        pattern = r'(\w+)\s*=\s*([^ \n]+)';
        matches = re.findall(pattern, message.text);
        variables = {};

        for match in matches:
            name, value = match;
            variables[name] = float(value);

        bot.send_message(message.from_user.id, f"{translations.get('Check_text')} {variables['a']}x² "
    +f"+ {variables['b']}x + {variables['c']} = 0?");

        bot.register_next_step_handler(message, solution, bot, variables['a'], variables['b'], variables['c'], translations, current_language);
    except Exception as e:
        bot.send_message(message.from_user.id, translations.get("Error_text"));
        print(f"Error: {e}");
        bot.register_next_step_handler(message, find_values, bot, translations, current_language);



def solution(message, bot, a, b, c, translations, current_language):
    if message.text.lower() in ['ja', 'jö', 'jo', 'так', 'да', 'yes']:
        D = b**2 - 4*a*c;
        if (D > 0):
            x_1 = (-b + math.sqrt(D)) / (2*a);
            x_2 = (-b - math.sqrt(D)) / (2*a);
            bot.send_message(message.from_user.id, f"D = {D}, then x_1 = {x_1} and x_2 = {x_2}");

        elif (D == 0):
            x = -b / (2*a);
            bot.send_message(message.from_user.id, f"D = {D}, {translations.get('One_root_text')}{x}");
        else:
            bot.send_message(message.from_user.id, f"D = {D}, {translations.get('No_roots_text')}");

    else:
        startQE(message, bot, current_language);
