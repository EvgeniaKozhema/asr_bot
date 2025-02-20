import telebot
import os
import whisper_model  # Импортируем файл с моделью
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Токен бота
TOKEN = "MY_TOKEN"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start_command(message):
    """Отправляет приветствие и меню с кнопками."""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Начать работу"), KeyboardButton("Завершить работу"))

    bot.send_message(
        message.chat.id,
        "Привет! Я бот для преобразования голосовых сообщений в текст.\n"
        "Нажмите 'Начать работу', чтобы отправить голосовое сообщение.",
        reply_markup=keyboard,
    )

@bot.message_handler(func=lambda message: message.text == "Начать работу")
def start_processing(message):
    """Сообщает, что бот готов к работе."""
    bot.send_message(message.chat.id, "Отправьте голосовое сообщение для обработки.")

@bot.message_handler(func=lambda message: message.text == "Завершить работу")
def stop_processing(message):
    """Убирает клавиатуру и завершает диалог."""
    bot.send_message(message.chat.id, "Работа завершена. Чтобы начать снова, введите /start", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    """Обрабатывает голосовые сообщения."""
    file_info = bot.get_file(message.voice.file_id)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)

    ogg_file = "voice.ogg"
    wav_file = "voice.wav"

    with open(ogg_file, "wb") as f:
        f.write(downloaded_file)

    text = whisper_model.transcribe_audio(ogg_file)  # Используем функцию из whisper_model.py

    os.remove(ogg_file)

    bot.reply_to(message, text)

# Запускаем бота
bot.polling(none_stop=True)
