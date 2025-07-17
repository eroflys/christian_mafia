import telebot
import sqlite3
import random


bot = telebot.TeleBot('7783453529:AAHmV2EnzWwnzNaWNqzyRXkJpMqH7_awkYI')
templates = {
    5: [1, 1, 1, 2, 5],
    6: [1, 1, 2, 2, 4, 5],
    7: [1, 1, 1, 2, 2, 4, 5],
    8: [1, 1, 1, 2, 2, 4, 5, 6],
    9: [1, 1, 1, 2, 2, 3, 4, 5, 6],
    10: [1, 1, 1, 1, 2, 2, 3, 4, 5, 6],
    11: [1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7],
    12: [1, 1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7]
}
roles = {
    1: 'Овца',
    2: 'Волк',
    3: 'Отец лжи',
    4: 'Молитвенник',
    5: 'Пророк',
    6: 'Далида',
    7: 'Змей'
}
images = {
    1: 'https://i.postimg.cc/D0cxx6gd/1.png',
    2: 'https://i.postimg.cc/rwHQZKSb/2.png',
    3: 'https://i.postimg.cc/HsBS5SjT/3.png',
    4: 'https://i.postimg.cc/MZ03ZZSM/4.png',
    5: 'https://i.postimg.cc/X7VHrMj2/5.png',
    6: 'https://i.postimg.cc/jS2MhzJP/6.png',
    7: 'https://i.postimg.cc/SsCTMkYP/7.png'
}


def showing_cards(message):
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    keyboard = telebot.types.InlineKeyboardMarkup()
    usr = templates[int(message.text)]
    random.shuffle(usr)
    usr = [str(i) for i in usr]
    status = message.text + '-' + '_'.join(usr) + '-0' + '-0'
    cur.execute('UPDATE chats SET status = 2 WHERE chat_id = ?', (message.chat.id, ))
    keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️",
                                       callback_data='left'), telebot.types.InlineKeyboardButton(text="Показать",
                                       callback_data='show'), telebot.types.InlineKeyboardButton(text="➡️",
                                       callback_data='right'))
    mes_id = bot.send_photo(message.chat.id, 'https://i.postimg.cc/HWhLvmrK/8.png', caption='Скрыто. Нажмите показать! 1/' + message.text,  reply_markup=keyboard, ).message_id
    cur.execute('INSERT INTO messages (message_id, status, chat_id) VALUES (?, ?, ?)', (mes_id, status, message.chat.id))
    con.commit()
    con.close()


@bot.callback_query_handler(func=lambda call: call.data == 'left')
def mv_left(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️",
                                                    callback_data='left'),
                 telebot.types.InlineKeyboardButton(text="Показать",
                                                    callback_data='show'), telebot.types.InlineKeyboardButton(text="➡️",
                                                                                                              callback_data='right'))
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    message = call.message
    status = cur.execute('SELECT status FROM messages WHERE message_id = ?', (message.message_id, )).fetchall()[0][0]
    if status.split('-')[-1] != '0':
        status = f'{'-'.join(status.split('-')[:-2])}-0-{int(status.split('-')[-1]) - 1}'
        cur.execute('UPDATE messages SET status = ? WHERE message_id = ?', (status, message.message_id))
        con.commit()
        media = telebot.types.InputMediaPhoto(media='https://i.postimg.cc/HWhLvmrK/8.png')
        bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption=f'Скрыто. Нажмите показать! {int(status.split('-')[-1]) + 1}/{status.split('-')[0]}', reply_markup=keyboard)
    con.close()


@bot.callback_query_handler(func=lambda call: call.data == 'right')
def mv_right(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️",
                                                    callback_data='left'),
                 telebot.types.InlineKeyboardButton(text="Показать",
                                                    callback_data='show'), telebot.types.InlineKeyboardButton(text="➡️",
                                                                                                              callback_data='right'))
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    message = call.message
    status = cur.execute('SELECT status FROM messages WHERE message_id = ?', (message.message_id,)).fetchall()[0][0]
    if int(status.split('-')[-1]) + 1 < int(status.split('-')[0]):
        status = f'{'-'.join(status.split('-')[:-2])}-0-{int(status.split('-')[-1]) + 1}'
        cur.execute('UPDATE messages SET status = ? WHERE message_id = ?', (status, message.message_id))
        con.commit()
        media = telebot.types.InputMediaPhoto(media='https://i.postimg.cc/HWhLvmrK/8.png')
        bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id,
                                 caption=f'Скрыто. Нажмите показать! {int(status.split('-')[-1]) + 1}/{status.split('-')[0]}', reply_markup=keyboard)

    con.close()


@bot.callback_query_handler(func=lambda call: call.data == 'show')
def show_hide(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️",
                                                    callback_data='left'),
                 telebot.types.InlineKeyboardButton(text="Показать",
                                                    callback_data='show'), telebot.types.InlineKeyboardButton(text="➡️",
                                                                                                              callback_data='right'))
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    message = call.message
    status = cur.execute('SELECT status FROM messages WHERE message_id = ?', (message.message_id,)).fetchall()[0][0]
    number = int(status.split('-')[1].split('_')[int(status.split('-')[-1])])
    if status.split('-')[-2] == '0':
        status = f'{'-'.join(status.split('-')[:-2])}-1-{int(status.split('-')[-1])}'
        cur.execute('UPDATE messages SET status = ? WHERE message_id = ?', (status, message.message_id))
        con.commit()
        media = telebot.types.InputMediaPhoto(media=images[number])
        bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id,
                                 caption=f'{roles[number]} {int(status.split('-')[-1]) + 1}/{status.split('-')[0]}', reply_markup=keyboard)
    else:
        status = f'{'-'.join(status.split('-')[:-2])}-0-{int(status.split('-')[-1])}'
        cur.execute('UPDATE messages SET status = ? WHERE message_id = ?', (status, message.message_id))
        con.commit()
        media = telebot.types.InputMediaPhoto(media='https://i.postimg.cc/HWhLvmrK/8.png')
        bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id,
                                 caption=f'Скрыто. Нажмите показать! {int(status.split('-')[-1]) + 1}/{status.split('-')[0]}', reply_markup=keyboard)

    con.close()


@bot.message_handler(commands=['start'])
def start(message):
    conn  = sqlite3.connect('status.db')
    cur = conn.cursor()
    chat_ids = cur.execute('SELECT chat_id FROM chats').fetchall()
    if (message.chat.id,) not in chat_ids:
        cur.execute('INSERT INTO chats (chat_id, status) VALUES (?, 1)', (message.chat.id, ))
        conn.commit()
        bot.send_message(message.chat.id, 'Выберите количество игроков (от 5 до 12)')
    else:
        cur.execute('UPDATE chats SET status = 1 WHERE chat_id = ?', (message.chat.id, ))
        conn.commit()
        bot.send_message(message.chat.id, 'Выберите количество игроков (от 5 до 12)')
    conn.close()


@bot.message_handler(content_types=['text'])
def text_handle(message):
    conn  = sqlite3.connect('status.db')
    cur = conn.cursor()
    status = cur.execute('SELECT status FROM chats WHERE chat_id = ?', (message.chat.id, )).fetchall()
    if len(status) == 0:
        # start(message)

        conn.close()
        return
    if status[0][0] == 1:
        if not message.text.isdigit():
            bot.send_message(message.chat.id, 'Введено не число, попробуй ещё раз')
        else:
            if 5 > int(message.text) or int(message.text) > 12:
                bot.send_message(message.chat.id, 'Введено число вне диапазона (от 5 до 12). Попробуй снова')
            else:
                showing_cards(message)
    else:
        pass
    conn.close()


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()