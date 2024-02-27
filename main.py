import telebot
import os
import json
import Functions.quadraticEquation as quadraticEquation
import Functions.linearSystemEquations as linearSystemEquations
import Functions.MathPhysicalEquationStringVibration as MathPhysicalEquationStringVibration
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("MY_API_KEY")

bot = telebot.TeleBot(api_key)



# Load translation
def load_translation(language):
    file_path = os.path.join('Translation', f'main_{language}.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations

# Set default language to English
current_language = 'EN'
translations = load_translation(current_language)

# Function to change language
def change_language(message):
    global current_language
    print(message.text)
    if(message.text == '/Change_Language_EN'):
        current_language = 'EN'
    elif(message.text == '/Change_Language_DE'):
        current_language = 'DE'
    elif(message.text == '/Change_Language_UA'):
        current_language = 'UA'
    elif(message.text == '/Change_Language_RU'):
        current_language = 'RU'
    return load_translation(current_language)

@bot.message_handler(commands=['Change_Language_EN', 'Change_Language_DE', 'Change_Language_UA', 'Change_Language_RU'])
def handle_change_language(message):
    print(1)
    global translations
    translations = change_language(message)
    bot.send_message(message.chat.id, f"Language changed to {current_language.upper()}")
    start_message(message)

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    help_text = translations.get("start_help_text", "Default Hello! I am your bot. I can do:\n\n"
                "/start - Start\n"
                "/help - Get help\n"
                "/System - System of linear equations\n"
                "/Quad - Quadratic equation\n"
                "/StringVibration - Mathematical-physical equation of string vibration\n"
                "/Change_Language_EN - English"
                "/Change_Language_DE - Deutsch"
                "/Change_Language_UA - Українська"
                "/Change_Language_RU - Русский")
    print(message.text)
    bot.send_message(message.chat.id, help_text)


# Help Menu
@bot.message_handler(commands=['System'])
def system_message(message):
    return linearSystemEquations.startLSE(message, bot, current_language)
@bot.message_handler(commands=['Quad'])
def quadratic_message(message):
    return quadraticEquation.startQE(message, bot, current_language)
@bot.message_handler(commands=['StringVibration'])
def string_vibration_message(message):
    return MathPhysicalEquationStringVibration.startMPESV(message, bot, current_language)

def create_keyboard(message, bot):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('System of linear equations')
    keyboard.add('Quadratic equation')
    keyboard.add('Mathematical-physical equation of string vibration')
    keyboard.add('Mathematical-physical equation of heat conductivity of a plate')
    keyboard.add('Mathematical-physical equation of heat conductivity of a rod')

    if message.text == 'Quadratic equation':
        return quadraticEquation.startQE(message, bot, current_language)
    elif message.text == 'System of linear equations':
        return linearSystemEquations.startLSE(message, bot, current_language)
    elif message.text == 'Mathematical-physical equation of string vibration':
        return MathPhysicalEquationStringVibration.startMPESV(message, bot, current_language)
    elif message.text == 'Mathematical-physical equation of heat conductivity of a plate':
        bot.send_message(message.from_user.id, 'Work in progress')
    elif message.text == 'Mathematical-physical equation of heat conductivity of a rod':
        bot.send_message(message.from_user.id, 'Work in progress')



bot.polling(none_stop=True, interval=0)
