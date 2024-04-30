import telebot
from collections import Counter
import re

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на свой токен, который вы получили от BotFather
TOKEN = '7028295680:AAFtqEeqt5levT9OhKr4Kvo7QFk8W69Vans'

bot = telebot.TeleBot(TOKEN)

mode_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
mode_keyboard.add(telebot.types.KeyboardButton('Математика'), telebot.types.KeyboardButton('Текст'))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Выбери режим работы (математика или текст).", reply_markup=mode_keyboard)


@bot.message_handler(func=lambda message: message.text == 'Математика')
def math_mode(message):
    bot.reply_to(message, "Хорошо! Теперь введи любой пример формата 2+2.")


@bot.message_handler(func=lambda message: message.text == 'Текст')
def text_mode(message):
    bot.reply_to(message,
                 "Окей! Теперь отправь мне текст (не более 500 символов), и я посчитаю различные статистические показатели.")


@bot.message_handler(func=lambda message: True)
def process_message(message):
    if message.text == 'Математика':
        bot.reply_to(message, "Хорошо! Теперь введи любой пример формата 2+2.")
    elif message.text == 'Текст':
        bot.reply_to(message,
                     "Окей! Теперь отправь мне текст (не более 500 символов), и я посчитаю различные статистические показатели.")
    elif re.match(r'^(\d+)([+\-*/])(\d+)$', message.text):
        num1, operator, num2 = re.match(r'^(\d+)([+\-*/])(\d+)$', message.text).groups()
        num1, num2 = int(num1), int(num2)
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                result = "Ошибка: деление на ноль"
        else:
            result = "Ошибка: неверный оператор"
        bot.reply_to(message, f"Результат: {result}")
    else:
        text = message.text  # Ограничиваем текст до 300 символов

        if len(text) > 500:
            bot.reply_to(message, "Извините, ваш текст превышает 500 символов. Пожалуйста, отправьте текст короче.")
            return

        text_length = len(text)
        word_count = len(text.split())
        sentence_count = len(re.findall(r'[.!?]+', text))

        # Находим самое длинное слово
        words = text.split()
        longest_word = max(words, key=len)

        # Находим самое редко встречающееся слово
        word_count = Counter(words)
        rarest_word = min(word_count, key=word_count.get)

        # Находим самую часто встречающуюся букву
        letter_count = Counter(filter(str.isalpha, text.lower()))
        most_common_letter = max(letter_count, key=letter_count.get)

        # Считаем количество цифр и других символов
        digit_count = sum(c.isdigit() for c in text)
        punctuation_count = sum(c in '.,?!:;-()[]{}' for c in text)

        reply_text = (
                f"Длина текста: {text_length} символов\n"
                f"Количество слов: {word_count}\n"
                f"Количество предложений: {sentence_count}\n"
                f"Самое длинное слово: {longest_word}\n"
                f"Самое редко встречающееся слово: {rarest_word}\n"
                f"Самая часто встречающаяся буква: {most_common_letter}\n\n"
                f"Количество цифр: {digit_count}\n"
                f"Количество знаков пунктуации: {punctuation_count}\n\n"
                "Статистика использования букв в тексте:\n" +
                '\n'.join([f'{letter}: {count}' for letter, count in letter_count.items()])
        )
        bot.reply_to(message, reply_text)


bot.polling()