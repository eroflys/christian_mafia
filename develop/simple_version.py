# from telegram import Update
# from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import time
import re
import telebot
import sqlite3
from collections import defaultdict
from pyexpat.errors import messages
import random
# from requests import get, post
# from datetime import datetime
# from telethon.sync import TelegramClient
# from telethon.sync import TelegramClient
# from telethon import functions, types
import io

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


def showing_cards(message):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    keyboard = telebot.types.InlineKeyboardMarkup()
    usr = templates[int(message.text)]
    random.shuffle(usr)
    status = message.text + '-' + '_'.join(usr) + '-0'
    cur.execute('UPDATE chats SET status = 2 WHERE chat_id = ?', (message.chat.id, ))
    keyboard.add(telebot.types.InlineKeyboardButton(text="⬅️",
                                       callback_data='left'), telebot.types.InlineKeyboardButton(text="Показать/скрыть",
                                       callback_data='show'), telebot.types.InlineKeyboardButton(text="➡️",
                                       callback_data='right'))
    mes_id = bot.send_photo(message.chat.id, 'im.webp', caption='Скрыто. Нажмите показать!',  reply_markup=keyboard, ).message_id
    cur.execute('INSERT INTO messages (message_id, status, chat_id) VALUES (?, ?, ?)', (mes_id, status, message.chat.id))
    con.commit()
    con.close()


@bot.callback_query_handler(func=lambda call: call.data == 'left')
def mv_left(call):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    message = call.message
    status = cur.execute('SELECT status FROM message WHERE message_id = ?', (message.message_id, )).fetchall()[0]
    if status.split('-')[-1] != '0':
        # if int(status.split('-')[-1]) + 1 < int(status.split('-')[0]):
        status = f'{'-'.join(status.split('-')[:-1])}-{int(status.split('-')[-1]) - 1}'
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption='Скрыто. Нажмите показать!')
    con.close()


@bot.callback_query_handler(func=lambda call: call.data == 'right')
def mv_right(call):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    message = call.message
    status = cur.execute('SELECT status FROM message WHERE message_id = ?', (message.message_id,)).fetchall()[0]
    if int(status.split('-')[-1]) + 1 < int(status.split('-')[0]):
        status = f'{'-'.join(status.split('-')[:-1])}-{int(status.split('-')[-1]) + 1}'
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id,
                                 caption='Скрыто. Нажмите показать!')
    con.close()


@bot.callback_query_handler(func=lambda call: call.data == 'show')
def show_hide


@bot.message_handler(content_types=['text'])
def text_handle(message):
    conn  = sqlite3.connect('example.db')
    cur = conn.cursor()
    status = cur.execute('SELECT status FROM chats WHERE chat_id = ?', (message.chat.id, )).fetchall()[0]
    if status == 1:
        if not message.text.isalpha():
            bot.send_message(message.chat.id, 'Введено не число, попробуй ещё раз')
        else:
            if 5 > int(message.text) or int(message.text) > 12:
                bot.send_message(message.chat.id, 'Введено число вне диапазона (от 5 до 12). Попробуй снова')
            else:
                showing_cards(message)
    else:
        pass
    conn.close()


@bot.message_handler(commands=['start'])
def start(message):
    conn  = sqlite3.connect('example.db')
    cur = conn.cursor()
    chat_ids = cur.execute('SELECT chat_id FROM chats').fetchall()
    if message.chat.id not in chat_ids:
        cur.execute('INSERT INTO chats (chat_id, status) VALUES (?, 1)', (message.chat.id, ))
        conn.commit()
        bot.send_message(message.chat.id, 'Выберите количество игроков (от 5 до 12)')
    else:
        status = cur.execute('SELECT status FROM chats WHERE chat_id = ?', (message.chat.id, )).fetchall()[0]
        if status == 1:
            bot.send_message(message.chat.id, 'Выберите количество игроков (от 5 до 12)')
    conn.close()


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()