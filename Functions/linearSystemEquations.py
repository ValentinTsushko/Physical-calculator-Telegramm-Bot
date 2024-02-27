import telebot
import math
import re
import os
import json
import numpy as np

def load_translation(language):
    file_path = os.path.join('Translation', f'linearSystemEquations_{language}.json');
    with open(file_path, 'r', encoding='utf-8') as file:
        translations = json.load(file);
    return translations;

def startLSE(message, bot, current_language):
    translations = load_translation(current_language);
    bot.send_message(message.from_user.id, translations.get("start_LSE_text"));
    bot.register_next_step_handler(message, num_equations, bot, current_language, translations);

def num_equations(message, bot, current_language, translations):
    num_equations = int(message.text);
    if num_equations == 0 or num_equations == 1:
        bot.send_message(message.from_user.id, translations.get("Sorry_text"));
    elif num_equations == 2:
        bot.send_message(message.from_user.id, translations.get("Example_text"));
        bot.send_message(message.from_user.id, "a_1_1 = 4.4 a_1_2 = 5 a_1_3 = 1.5 \n"
        +"a_2_1 = 8 a_2_2 = -2 a_2_3 = 38.75\n");
        bot.send_message(message.from_user.id, translations.get("Will_look_like_text"));
    else:
        bot.send_message(message.from_user.id, translations.get("Please_enter_text"));
        bot.send_message(message.from_user.id, "a_1_1 = 4.4 a_1_2 = 5 a_1_3 = 1.5 a_1_4 = 3\n"
        +"a_2_1 = 8 a_2_2 = -2 a_2_3 = 7.75 a_2_4 = 38.75\n"
        +"a_3_1 = 6 a_3_2 = 1 a_3_3 = 1.5 a_3_4 = 6\n");
        bot.send_message(message.from_user.id, translations.get("Will_look_like_2"));
    bot.register_next_step_handler(message, find_integers, bot, num_equations, current_language, translations);

def find_integers(message, bot, num_equations, current_language, translations):
    try:
        pattern = r'(\w+)\s*=\s*([^ \n]+)';
        matches = re.findall(pattern, message.text);
        variables = {};
        for match in matches:
            name, value = match;
            variables[name] = float(value);
        if num_equations == 2:
            solve_system_2d(message, bot, variables);
        else:
            solve_system_nd(message, bot, variables, num_equations);
    except Exception as e:
        bot.send_message(message.from_user.id, translations.get("Error_text"));
        print(f"Error: {e}");
        bot.register_next_step_handler(message, find_integers, bot, num_equations, current_language, translations);

def solve_system_2d(message, bot, variables):
    delta = variables['a_1_1']*variables['a_2_2'] - variables['a_2_1']*variables['a_1_2'];
    delta_x = variables['a_1_3']*variables['a_2_2'] - variables['a_2_3']*variables['a_1_2'];
    delta_y = variables['a_1_1']*variables['a_2_3'] - variables['a_2_1']*variables['a_1_3'];
    try:
        x = delta_x / delta;
        y = delta_y / delta;
    except Exception as e:
        bot.send_message(message.from_user.id, "Incomplete system");
        print(f"Error: {e}");
        x = 0
        y = 0
    bot.send_message(message.from_user.id, f"x = {x} and y = {y}");

def solve_system_nd(message, bot, variables, num_equations):
    coefficients_matrix = np.array(list(variables.values()));
    coefficients_matrix_2d = coefficients_matrix.reshape((num_equations, -1));

    B_n_vector = coefficients_matrix_2d[:, -1];
    A_n_n_matrix = coefficients_matrix_2d[:, :-1];

    solution = np.linalg.solve(A_n_n_matrix, B_n_vector);
    bot.send_message(message.from_user.id, f"x_1, x_2, ... x_{num_equations} = {solution}");
