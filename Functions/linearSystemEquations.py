import telebot
import math
import re
import numpy as np

def start(message, bot):
    bot.send_message(message.from_user.id, "Please enter how many equations you have\n"
    +"For example: 2 or 3");
    bot.register_next_step_handler(message, num_equations, bot);

def num_equations(message, bot):
    num_equations = int(message.text)

    if num_equations == 0 or num_equations == 1:
        bot.send_message(message.from_user.id, "Sorry! It's not a system!");

    elif num_equations == 2:
        bot.send_message(message.from_user.id, "Please enter a_1_1 ... a_n_n\n"
        + "If we know:\n"
        +"1) a_1_1*x + a_1_2*y = a_1_3\n"
        +"2) a_2_1*x + a_2_2*y = a_2_3\n"
        +"Please write it as shown in the example. If you have non-integer values, use a dot.\n"
        +"For example:\n");
        bot.send_message(message.from_user.id, "a_1_1 = 4.4 a_1_2 = 5 a_1_3 = 1.5 \n"
        +"a_2_1 = 8 a_2_2 = -2 a_2_3 = 38.75\n");
        bot.send_message(message.from_user.id, "Will look like:\n"
        +"1) 4.4*x + 5*y = 1.5\n"
        +"2) 8*x - 2*y = 38.75\n"
        +"Answer:\n"
        +"x = 4.031762295081967 and y = -3.2479508196721314");

    else:
        bot.send_message(message.from_user.id, "Please enter a_1_1, ... a_n_n\n"
        +"If we know:\n"
        +"1) a_1_1*x_1 + a_1_2*x_2 + ... + a_1_n*x_n = B_1\n"
        +"2) a_2_1*x_1 + a_2_2*x_2 + ... + a_2_n*x_n = B_2\n"
        +"..................................................\n"
        +"n) a_n_1*x_1 + a_n_2*x_2 + ... + a_n_n*x_n = B_n\n\n"
        +"Please write it as shown in the example. If you have non-integer values, use a dot.\n"
        +"For example:\n");
        bot.send_message(message.from_user.id, "a_1_1 = 4.4 a_1_2 = 5 a_1_3 = 1.5 a_1_4 = 3\n"
        +"a_2_1 = 8 a_2_2 = -2 a_2_3 = 7.75 a_2_4 = 38.75\n"
        +"a_3_1 = 6 a_3_2 = 1 a_3_3 = 1.5 a_3_4 = 6\n");
        bot.send_message(message.from_user.id, "Will look like\n"
        +"1) 4.4*x_1 + 5*x_2 + 1.5*x_3 = 3\n"
        +"2) 8*x_1 - 2*x_2 + 7.75*x_3 = 38.75\n"
        +"3) 6*x_1 + 1*x_2 + 1.5*x_3 = 6\n"
        +"Answer:\n"
        +"x_1, x_1, ... x_n = [-0.09181701 -0.7867268   4.89175258]\n");

    bot.register_next_step_handler(message, find_integers, bot, num_equations);

def find_integers(message, bot, num_equations):
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

def solve_system_2d(message, bot, variables):
    delta = variables['a_1_1']*variables['a_2_2'] - variables['a_2_1']*variables['a_1_2'];
    delta_x = variables['a_1_3']*variables['a_2_2'] - variables['a_2_3']*variables['a_1_2'];
    delta_y = variables['a_1_1']*variables['a_2_3'] - variables['a_2_1']*variables['a_1_3'];

    x = delta_x / delta;
    y = delta_y / delta;

    bot.send_message(message.from_user.id, f"x = {x} and y = {y}");

def solve_system_nd(message, bot, variables, num_equations):
    coefficients_matrix = np.array(list(variables.values()));

    coefficients_matrix_2d = coefficients_matrix.reshape((num_equations, -1));

    B_n_vector = coefficients_matrix_2d[:, -1];
    A_n_n_matrix = coefficients_matrix_2d[:, :-1];

    solution = np.linalg.solve(A_n_n_matrix, B_n_vector)
    bot.send_message(message.from_user.id, f"x_1, x_2, ... x_{num_equations} = {solution}")
