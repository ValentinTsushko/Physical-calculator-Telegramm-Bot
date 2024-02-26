import telebot;
import math;
import re;
import numpy as np;
from scipy.integrate import solve_ivp as s_i;
from io import BytesIO;
import matplotlib.pyplot as plt;


def Start(message, bot):
    bot.send_message(message.from_user.id, "Bitte geben Sie длину струны");
    bot.register_next_step_handler(message, SaitenschwingungGleichung, bot);

def waveEquationDiff(t, y, c, L):
    dydt = np.zeros_like(y)
    #dydt[0] = y[1]
    dydt[0] = 0
    dydt[-1] = 0  # Закрепляем конец струны
    dydt[1:-1] = c**2 * (y[:-2] - 2*y[1:-1] + y[2:]) / L**2
    return dydt

def SaitenschwingungGleichung(message, bot):
    # Параметры струны         # Длина струны
    L = float(message.text);
    c = 1.0         # Скорость распространения волны

    # Начальные условия
    initial_displacement = np.sin(np.pi * np.linspace(0, 1, 101))  # Исходное смещение струны
    initial_velocity = np.zeros_like(initial_displacement)         # Исходная скорость струны

    initial_conditions = np.concatenate([initial_displacement, initial_velocity])

    t = (0, 2)  # Интегрируем от 0 до 2 секунд

    # Решение дифференциального уравнения
    Loesung = s_i(waveEquationDiff, t, initial_conditions, args=(c, L), t_eval=np.linspace(0, 2, 100))
    bot.send_message(message.from_user.id, f"{Loesung}");

    plt.figure(figsize=(8, 4))
    plt.plot(Loesung.t, Loesung.y[0:101, :].T)
    plt.title('Колебания струны')
    plt.xlabel('Время')
    plt.ylabel('Смещение струны')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    bot.send_photo(chat_id=message.chat.id, photo=buffer);
