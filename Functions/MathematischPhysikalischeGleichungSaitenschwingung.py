import telebot;
import math;
import re;
import numpy as np;
from scipy.integrate import solve_ivp as s_i;
from io import BytesIO;
import matplotlib.pyplot as plt;


def Start(message, bot):
    bot.send_message(message.from_user.id, "Bitte geben Sie Saitenlänge L, Wellenausbreitungsgeschwindigkeit c, Zeit t, Anfangsende der Saite dydt0 und Endende dydt1");
    bot.send_message(message.from_user.id, "Bitte schreiben Sie, wie im Beispiel, wenn Sie nicht ganze Zahlen haben, dann schreiben Sie mit dem Punkt");
    bot.send_message(message.from_user.id, "Zum Beispiel:");
    bot.send_message(message.from_user.id, "L = 1 c = 1 t = 2 \ndydt0 = 74 dydt1 = 0");
    bot.register_next_step_handler(message, SuchenVar, bot);

def SuchenVar(message, bot):
    pattern = r'(\w+)\s*=\s*([^ \n]+)';
    Uebereinstimmen = re.findall(pattern, message.text);
    variablen = {};
    for Uebereinstimm in Uebereinstimmen:
        Name, Wert = Uebereinstimm;

        variablen[Name] = float(Wert);

    SaitenschwingungGleichung(message, bot, variablen);

def waveEquationDiff(t, y, c, L, variablen):
    dydt = np.zeros_like(y);
    dydt[0] = variablen['dydt0'];
    dydt[-1] = variablen['dydt1'];
    dydt[1:-1] = c**2 * (y[:-2] - 2*y[1:-1] + y[2:]) / L**2;
    return dydt;

def SaitenschwingungGleichung(message, bot, variablen):
    # Параметры струны
    L = variablen['L'];         # Длина струны
    c = variablen['c'];         # Скорость распространения волны

    # Начальные условия
    initial_displacement = np.sin(np.pi * np.linspace(0, 1, 101));  # Исходное смещение струны
    initial_velocity = np.zeros_like(initial_displacement);         # Исходная скорость струны

    initial_conditions = np.concatenate([initial_displacement, initial_velocity]);

    t = (0, variablen['t']);  # Интегрируем от 0 до n секунд

    # Решение дифференциального уравнения
    Loesung = s_i(waveEquationDiff, t, initial_conditions, args=(c, L, variablen), t_eval=np.linspace(0, 2, 100))
    bot.send_message(message.from_user.id, f"{Loesung}");

    plt.figure(figsize=(8, 4));
    plt.plot(Loesung.t, Loesung.y[0:101, :].T);
    plt.title('Saitenvibrationen');
    plt.xlabel('Zeit');
    plt.ylabel('Saitevershobung');
    buffer = BytesIO();
    plt.savefig(buffer, format='png');
    buffer.seek(0);
    bot.send_photo(chat_id=message.chat.id, photo=buffer);
