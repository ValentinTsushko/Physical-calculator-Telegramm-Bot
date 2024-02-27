import telebot
import math
import re
import os
import json
import numpy as np
from scipy.integrate import solve_ivp as s_i
from io import BytesIO
import matplotlib.pyplot as plt

def load_translation(language):
    file_path = os.path.join('Translation', f'MathPhysicalEquationStringVibration_{language}.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations

def startMPESV(message, bot, current_language):
    translations = load_translation(current_language);
    bot.send_message(message.from_user.id, translations.get("start_MPESV_text"));
    bot.send_message(message.from_user.id, "L = 1 c = 1 t = 2 \ndydt0 = 74 dydt1 = 0");
    bot.register_next_step_handler(message, find_variables, bot, translations);

def find_variables(message, bot, translations):
    try:
        pattern = r'(\w+)\s*=\s*([^ \n]+)';
        matches = re.findall(pattern, message.text);
        variables = {};

        for match in matches:
            name, value = match;
            variables[name] = float(value);

        solve_wave_equation(message, bot, variables);

    except Exception as e:
        bot.send_message(message.from_user.id, translations.get("Error_text"));
        print(f"Error: {e}");
        bot.register_next_step_handler(message, find_variables, bot, translations);



def wave_equation_diff(t, y, c, L, variables):
    dydt = np.zeros_like(y);
    dydt[0] = variables['dydt0'];
    dydt[-1] = variables['dydt1'];
    dydt[1:-1] = c**2 * (y[:-2] - 2*y[1:-1] + y[2:]) / L**2;
    return dydt;

def solve_wave_equation(message, bot, variables):
    # String parameters
    L = variables['L'];  # String length
    c = variables['c'];  # Wave propagation speed

    # Initial conditions
    initial_displacement = np.sin(np.pi * np.linspace(0, 1, 101));  # Initial displacement of the string
    initial_velocity = np.zeros_like(initial_displacement);  # Initial velocity of the string

    initial_conditions = np.concatenate([initial_displacement, initial_velocity]);

    t = (0, variables['t']);  # Integrate from 0 to n seconds

    # Solve the differential equation
    solution = s_i(wave_equation_diff, t, initial_conditions, args=(c, L, variables), t_eval=np.linspace(0, 2, 100));
    bot.send_message(message.from_user.id, f"{solution}");

    # Plot the string vibrations
    plt.figure(figsize=(8, 4));
    plt.plot(solution.t, solution.y[0:101, :].T);
    plt.title('String Vibrations');
    plt.xlabel('Time');
    plt.ylabel('String Displacement');
    buffer = BytesIO();
    plt.savefig(buffer, format='png');
    buffer.seek(0);
    bot.send_photo(chat_id=message.chat.id, photo=buffer);
