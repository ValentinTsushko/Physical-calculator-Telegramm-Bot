import telebot
import os
import Functions.quadraticEquation as quadraticEquation
import Functions.linearSystemEquations as linearSystemEquations
import Functions.MathPhysicalEquationStringVibration as MathPhysicalEquationStringVibration
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("MY_API_KEY")

bot = telebot.TeleBot(api_key)

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    help_text = "Hello! I am your bot. I can do:\n\n" \
                "/start - Start\n" \
                "/help - Get help\n" \
                "/System - System of linear equations\n" \
                "/Quad - Quadratic equation\n" \
                "/StringVibration - Mathematical-physical equation of string vibration"

    bot.send_message(message.chat.id, help_text)

# Help Menu
@bot.message_handler(commands=['System'])
def system_message(message):
    return linearSystemEquations.start(message, bot)
@bot.message_handler(commands=['Quad'])
def quadratic_message(message):
    return quadraticEquation.start(message, bot)
@bot.message_handler(commands=['StringVibration'])
def string_vibration_message(message):
    return MathPhysicalEquationStringVibration.start(message, bot)


@bot.message_handler(content_types=['text'])
def start(message):
    create_keyboard(message, bot)

def create_keyboard(message, bot):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('System of linear equations')
    keyboard.add('Quadratic equation')
    keyboard.add('Mathematical-physical equation of string vibration')
    keyboard.add('Mathematical-physical equation of heat conductivity of a plate')
    keyboard.add('Mathematical-physical equation of heat conductivity of a rod')

    if message.text == 'Quadratic equation':
        return quadraticEquation.start(message, bot)
    elif message.text == 'System of linear equations':
        return linearSystemEquations.start(message, bot)
    elif message.text == 'Mathematical-physical equation of string vibration':
        return MathPhysicalEquationStringVibration.start(message, bot)
    elif message.text == 'Mathematical-physical equation of heat conductivity of a plate':
        bot.send_message(message.from_user.id, 'Work in progress')
    elif message.text == 'Mathematical-physical equation of heat conductivity of a rod':
        bot.send_message(message.from_user.id, 'Work in progress')



bot.polling(none_stop=True, interval=0)
