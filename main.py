import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram import Update

from config import TOKEN

# Создание таблицы, если её нет
def create_table():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Определение команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь свой отзыв.')

# Обработка нового отзыва
# Обработка нового отзыва
def handle_review(update: Update, context: CallbackContext) -> None:
    review_text = update.message.text

    # Сохранение отзыва в базе данных
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (text) VALUES (?)", (review_text,))
    conn.commit()
    conn.close()

    # Отправка отзыва в указанный чат
    chat_id = '-1002026921664'  # Замените на актуальный chat_id вашего чата
    context.bot.send_message(chat_id, f'Новый отзыв: {review_text}')

    # Ответ пользователю
    update.message.reply_text('Спасибо за отзыв!')

# Просмотр последних отзывов
def view_reviews(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews ORDER BY timestamp DESC LIMIT 5")
    reviews = cursor.fetchall()
    conn.close()

    if not reviews:
        update.message.reply_text('Пока нет отзывов.')
    else:
        for review in reviews:
            update.message.reply_text(f'{review[2]}: {review[1]}')

# Запуск бота
def main() -> None:
    create_table()

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(None, handle_review))
    dp.add_handler(CommandHandler("view_reviews", view_reviews))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
