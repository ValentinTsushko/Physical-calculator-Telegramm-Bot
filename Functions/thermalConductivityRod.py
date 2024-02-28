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
    file_path = os.path.join('Translation', f'thermalConductivityRod_{language}.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations

def startTCR(message, bot, current_language):
    translations = load_translation(current_language);
    bot.send_message(message.from_user.id, translations.get("startTCR_text"));
    bot.register_next_step_handler(message, Check_inhomogeneous, bot, translations);

def Check_inhomogeneous(message, bot, translations):
    global IsInhomogeneous;
    if message.text.lower() in ['ja', 'jö', 'jo', 'так', 'да', 'yes', '1', '+']:
        IsInhomogeneous = True;
    else:
        IsInhomogeneous = False;
    bot.send_message(message.from_user.id, translations.get("find_Out_Variables_text"));
    bot.send_message(message.from_user.id, "L = 1 alpha = 0.01 t = 0.1 \nT_fixed_0 = 0 T_fixed_1 = 0 \nNx = 100 Nt = 100");
    bot.register_next_step_handler(message, find_variables, bot, translations);

def find_variables(message, bot, translations):
    try:
        pattern = r'(\w+)\s*=\s*([^ \n]+)';
        matches = re.findall(pattern, message.text);
        variables = {};
        for match in matches:
            name, value = match;
            variables[name] = float(value);

        variables['Nx'] = int(variables['Nx']);
        variables['Nt'] = int(variables['Nt']);

        solve_conduction_equation(message, bot, variables);
    except Exception as e:
        bot.send_message(message.from_user.id, translations.get("Error_text"));
        print(f"Error: {e}");
        bot.register_next_step_handler(message, find_variables, bot, translations);

def heat_conduction_equation(L, t, alpha, Nx, Nt, T_fixed_0, T_fixed_1):
    dx = L / Nx;
    dt = t / Nt;

    # Initialize the grid
    x_values = np.linspace(0, L, Nx + 1);
    u = np.zeros((Nt + 1, Nx + 1));

    # Initial and boundary conditions
    if(IsInhomogeneous):
        u[0, :] = initial_condition_inhomogeneous(x_values);
    else:
        u[0, :] = initial_condition_constant(x_values);
    u[:, 0] = boundary_condition(0, t, alpha, T_fixed_0, T_fixed_1, L);
    u[:, -1] = boundary_condition(L, t, alpha, T_fixed_0, T_fixed_1, L);

    # Solving the heat equation using the finite difference method
    for n in range(0, Nt):
        for i in range(1, Nx):
            u[n + 1, i] = u[n, i] + alpha * dt / dx**2 * (u[n, i + 1] - 2 * u[n, i] + u[n, i - 1]);

    return x_values, u

def initial_condition_inhomogeneous(x):
    return np.sin(np.pi * x);
def initial_condition_constant(x):
    return x;

def boundary_condition(x, t, alpha, T_fixed_0, T_fixed_1, L):
    # Set a fixed temperature on both boundaries
    if (x == 0):
        return T_fixed_0;
    elif(x == L):
        return T_fixed_1;
    else:
        return 0


# Task parameters
def solve_conduction_equation(message, bot, variables):
     L = variables['L'];            # Rod length
     t = variables['t'];            # Time
     alpha = variables['alpha'];    # Coefficient of thermal conductivity

     Nx = variables['Nx'];          # Number of spatial nodes
     Nt = variables['Nt'];          # Number of temporary nodes

    T_fixed_0 = variables['T_fixed_0'];
    T_fixed_1 = variables['T_fixed_1'];

    # Solving the heat equation
    x_values, u = heat_conduction_equation(L, t, alpha, Nx, Nt, T_fixed_0, T_fixed_1)
    bot.send_message(message.from_user.id, f"x_values - {x_values}, U - {u}");

    # Visualization of results
    plt.imshow(u, extent=[0, L, 0, t], origin='lower', aspect='auto', cmap='hot')
    plt.colorbar(label='Temperature')
    plt.title('Heat Conduction in a Rod')
    plt.xlabel('Position')
    plt.ylabel('Time')
    buffer = BytesIO();
    plt.savefig(buffer, format='png');
    buffer.seek(0);
    bot.send_photo(chat_id=message.chat.id, photo=buffer);
