# бот для вивчення англійських слів з CSV файлу  + статистика за користувачами
# https://t.me/idstickerbot для отримання колу стикерів
# для публікації бота - https://www.pythonanywhere.com/user/vkm/consoles/
import random
import csv
from telebot import TeleBot, types
from _keyeng import TOKEN

# Об'єкт бота
bot = TeleBot(TOKEN)

# Зберігаємо підрахунок вірних і невірних виборів для кожного користувача
user_stats = {}

# Змінна для зберігання режиму відображення
display_mode = "uk_to_en"  # "uk_to_en" або "en_to_uk"

# Змінна для зберігання правильного перекладу
correct_translation = ""
question_word = ""

# Читання даних з CSV файлу
file_path = 'D:\\Python\\vsc01\\tg_bot_english\\eng_word_big.csv'
words = []

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        words.append({'en': row['en'], 'ua': row['ua']})

def get_random_words():
    return random.sample(words, 4)

# Функція для відправки кнопок керування
def send_control_buttons(chat_id):
    control_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    control_kb.add(types.KeyboardButton('🔄 Змінити режим'))
    control_kb.add(types.KeyboardButton('📊 Ваші результати'), types.KeyboardButton('📈 Загальні результати'))
    # control_kb.add(types.KeyboardButton('🗑️ Очистити статистику'))  # Додаємо кнопку
    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEM9jVnC9qu5HDVKMavp8sc2WeTLeWQGAACfQAD9wLIDy7JuwrdyyJJNgQ')
    bot.send_message(chat_id, "Вітаю!\nБот для вивчення англійських слів з CSV файлу та підрахунком результатів", reply_markup=control_kb) #"Оберіть опцію:"
    # Додаємо inline кнопку з посиланням на канал
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(types.InlineKeyboardButton('Viktor Kaliuta', url='https://t.me/vkaliuta'))
    bot.send_message(chat_id, "Задати питання автору:", reply_markup=inline_kb)

# Хендлер на команду /start
@bot.message_handler(commands=['start'])
def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_stats:
        user_stats[user_id] = {'correct_count': 0, 'incorrect_count': 0}
    send_control_buttons(message.chat.id)
    send_new_word(message.chat.id)

# Функція для відправки нового слова з варіантами
def send_new_word(chat_id):
    global display_mode, correct_translation, question_word
    selected_words = get_random_words()
    correct_word = random.choice(selected_words)
    correct_translation = correct_word['ua'] if display_mode == "uk_to_en" else correct_word['en']
    question_word = correct_word['en'] if display_mode == "uk_to_en" else correct_word['ua']

    inline_kb = types.InlineKeyboardMarkup()
    if display_mode == "uk_to_en":
        for word in selected_words:
            inline_kb.add(types.InlineKeyboardButton(word['en'], callback_data=f"{word['en']}_{correct_word['ua']}"))
        bot.send_message(chat_id, f"Обери переклад - {correct_word['ua']} :", reply_markup=inline_kb)
    else:
        for word in selected_words:
            inline_kb.add(types.InlineKeyboardButton(word['ua'], callback_data=f"{word['ua']}_{correct_word['en']}"))
        bot.send_message(chat_id, f"Choose a translation - {correct_word['en']} :", reply_markup=inline_kb)

# Хендлер для обробки callback data
def callback_filter(call):
    if call.data:
        return call.data
    return False

@bot.callback_query_handler(func=callback_filter)
def callback_inline(call: types.CallbackQuery):
    global correct_translation, question_word
    user_id = call.from_user.id
    if user_id not in user_stats:
        user_stats[user_id] = {'correct_count': 0, 'incorrect_count': 0}
    
    try:
        data = call.data.split('_')
        selected_word, given_translation = data[0], data[1]
        
        if (display_mode == "uk_to_en" and any(word['en'] == selected_word and word['ua'] == given_translation for word in words)) or \
           (display_mode == "en_to_uk" and any(word['ua'] == selected_word and word['en'] == given_translation for word in words)):
            user_stats[user_id]['correct_count'] += 1
            bot.send_message(call.message.chat.id, f"✅ вірно, {correct_translation} - {question_word}")
        else:
            user_stats[user_id]['incorrect_count'] += 1
            bot.send_message(call.message.chat.id, f"❌ невірно, {correct_translation} - {question_word}")
        
        # Відправка нового слова
        send_new_word(call.message.chat.id)
        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print(f"Error handling callback: {e}")  # Діагностика помилки

# Хендлер для обробки текстових повідомлень
@bot.message_handler(func=lambda message: True)
def handle_message(message: types.Message):
    global display_mode
    user_id = message.from_user.id
    if user_id not in user_stats:
        user_stats[user_id] = {'correct_count': 0, 'incorrect_count': 0}
    
    # if {user_stats[user_id]['correct_count']} == 7:
    #     bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEM9jtnC94AAfCheYWtxNfF68T_k0qiK7IAAnEAA_cCyA95CsT0_beIyzYE')

    if message.text == '📊 Ваші результати':
        bot.send_message(message.chat.id, f"Вірні відповіді: {user_stats[user_id]['correct_count']}\nНевірні відповіді: {user_stats[user_id]['incorrect_count']}")
    # elif message.text == '🗑️ Очистити статистику':
    #     user_stats[user_id] = {'correct_count': 0, 'incorrect_count': 0}
    #     bot.send_message(message.chat.id, "Cтатистику очищено!")
    elif message.text == '🔄 Змінити режим':
        display_mode = "en_to_uk" if display_mode == "uk_to_en" else "uk_to_en"
        bot.send_message(message.chat.id, f"Режим змінено на {'англійська до українська' if display_mode == 'en_to_uk' else 'українська до англійська'}")
        send_new_word(message.chat.id)
    elif message.text == '📈 Загальні результати':
        total_stats = ""
        for user_id, stats in user_stats.items():
            # Отримуємо ім'я користувача за його ID
            user = bot.get_chat(user_id)
            user_name = user.first_name
            total_stats += f"Користувач:\n{user_name}, Вірно: {stats['correct_count']}, Невірно: {stats['incorrect_count']}\n"
        
        bot.send_message(message.chat.id, total_stats if total_stats else "Поки що немає статистики.")

# Запуск процесу поллінгу нових апдейтів
if __name__ == '__main__':
    bot.infinity_polling()