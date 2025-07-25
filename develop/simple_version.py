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
des = {
    1: '''🐑 *Овца*
🎯 Цель: Победить Тьму и защитить Церковь\\.
🌙 Ночью: Ты мирно спишь\\.
💡 Задача:
Днем активно участвуй в обсуждениях, выявляй Волков и голосуй за изгнание тех, кто сеет ложь\\.
Ты — сердце Церкви, и твоя наблюдательность может спасти всех\\!''',
    2: '''🐺 *Волк*
🎯 Цель: Избавление от Церкви\\.
🌙 Ночью: Совместно с другими Волками выбираешь жертву для исключения\\.
💡 Задача:
Днем притворяйся овцой, запутывай обсуждения, направляй подозрения на невинных\\.
Ночью — действуй решительно, чтобы Тьма восторжествовала\\!''',
    3: '''🕷 *Отец Лжи*
🎯 Цель: Руководить Волками и найти Пророка\\.
🌙 Ночью:
 1\\. Совместно с Волками избавляешься от овец\\.
 2\\. Проверяешь игрока: Пророк ли он\\?
💡 Задача:
Ты — лидер Тьмы\\.
Днем плети интриги и обманывай, чтобы сбить Церковь с толку\\.
Ночью — координируй действия и ищи тех, кто мешает твоим планам\\!''',
    4: '''🙏 *Молитвенник*
🎯 Цель: Защитить игрока\\.
🌙 Ночью: Исцеляешь одного игрока \\(нельзя исцелять себя 2 ночи подряд\\)\\.
💡 Задача:
Днем внимательно слушай, чтобы понять, кто нуждается в помощи\\.
Ночью — выбирай, кого защитить от зла\\.
Ты — надежда Церкви, твои молитвы спасают жизни\\!''',
    5: '''🗣 *Пророк*
🎯 Цель: Найти Волков\\.
🌙 Ночью: Проверяешь игрока — Волк он или нет\\?
💡 Задача:
Днем используй свои знания, чтобы направить Церковь на верный путь\\.
Ночью — ищи тех, кто скрывается под маской\\.
Твое видение — ключ к победе Света\\!''',
    6: '''💃 *Далида*
🎯 Цель: Блокировать действия, нарушать планы\\.
🌙 Ночью:
Выбираешь 1 игрока и блокируешь его способности\\.
На следующий день он не может голосовать, но и за него голосовать нельзя\\.
💡 Задача:
Днем будь незаметной, но влиятельной\\.
Ночью — блокируй ключевых игроков, чтобы создавать хаос и запутывать обе стороны\\.
Твоя хитрость способна перевернуть игру\\!''',
    7: '''🐍 *Змей*
🎯 Цель: Остаться последним живым\\.
🌙 Ночью: Исключаешь одного игрока отдельно от Волков\\.
💡 Задача:
Днем плети интриги и порождай подозрения, оставаясь в тени\\.
Ночью — исключай всех, кто мешает тебе выжить\\.
Ты играешь только за себя, и твоя выгода — превыше всего\\!'''
}
images = {
    1: 'https://i.postimg.cc/D0cxx6gd/1.png',
    2: 'https://i.postimg.cc/rwHQZKSb/2.png',
    3: 'https://i.postimg.cc/HsBS5SjT/3.png',
    4: 'https://i.postimg.cc/MZ03ZZSM/4.png',
    5: 'https://i.postimg.cc/X7VHrMj2/5.png',
    6: 'https://i.postimg.cc/jS2MhzJP/6.png',
    7: 'https://i.postimg.cc/SsCTMkYP/7.png',
    8: 'https://i.postimg.cc/N0KPSzT5/6.png',
    'main': 'https://i.postimg.cc/529bDbnp/photo-2025-07-19-18-40-50.jpg',
    'rules': 'https://i.postimg.cc/qMwdsW4K/2.png',
    'roles': 'https://i.postimg.cc/8CJQV5Wd/3.png',
    'how_win': 'https://i.postimg.cc/FzqL3V2G/4.png',
    'start': 'https://i.postimg.cc/m280zMyN/5.png'
}


def main_start(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="правила", callback_data='rules'),
                 telebot.types.InlineKeyboardButton(text="роли и способности", callback_data='roles')
                 )
    keyboard.add(telebot.types.InlineKeyboardButton(text="как победить", callback_data='how_win'),
                 telebot.types.InlineKeyboardButton(text="начать игру", callback_data='start_game')
                 )
    mes_id = bot.send_photo(message.chat.id, images['main'], caption='''Добро пожаловать в мир "*Библейской Мафии*" – захватывающей игры, где Церковь и Тьма сойдутся в битве лжи и правды, доверия и хитрости, света и тьмы\\!

Здесь ты окажешься в самом центре противостояния Овец и Волков, где каждый ход имеет значение, а истинные намерения скрыты за маской\\.

Готов ли ты бросить вызов\\?

Для начала, ты можешь ознакомиться с правилами игры, ролями и способностями\\.

✨ *Что умеет этот бот:*
📖 *Правила игры:* Узнай общую суть и особенности\\.
🎭 *Роли и способности:* Изучи каждого персонажа и его уникальные действия\\.
🏆 *Как победить\\?:* Разберись с условиями победы для каждой стороны\\.
🔢 *Начать игру:* Собери друзей и окунись в мир "Библейской Мафии"\\!

Нажми на кнопку ниже или используй меню, чтобы начать свое приключение\\! 👇''',
                   reply_markup=keyboard, parse_mode='MarkdownV2', ).message_id
    conn = sqlite3.connect('status.db')
    cur = conn.cursor()
    chat_ids = cur.execute('SELECT chat_id FROM chats').fetchall()
    if (message.chat.id,) not in chat_ids:
        cur.execute('INSERT INTO chats (chat_id, status, main_mes) VALUES (?, 1, ?)', (message.chat.id, mes_id))
        conn.commit()
        bot.pin_chat_message(message.chat.id, mes_id, disable_notification=True)
        bot.delete_message(message.chat.id, mes_id + 1)
    else:
        old_mes = cur.execute('SELECT main_mes FROM chats WHERE chat_id = ?', (message.chat.id, )).fetchall()[0][0]
        bot.unpin_chat_message(message.chat.id, old_mes)
        bot.delete_message(message.chat.id, old_mes)
        cur.execute('UPDATE chats SET status = 1, main_mes = ? WHERE chat_id = ?', (mes_id, message.chat.id))
        conn.commit()
        bot.pin_chat_message(message.chat.id, mes_id, disable_notification=True)
        bot.delete_message(message.chat.id, mes_id + 1)
    conn.close()

def showing_cards(message):
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    keyboard = telebot.types.InlineKeyboardMarkup()
    usr = templates[int(message.text)]
    random.shuffle(usr)
    usr = [str(i) for i in usr]
    status = message.text + '-' + '_'.join(usr) + '-0' + '-0'
    cur.execute('UPDATE chats SET status = 2 WHERE chat_id = ?', (message.chat.id, ))
    keyboard.add(telebot.types.InlineKeyboardButton(text="Показать",
                                       callback_data='show'), telebot.types.InlineKeyboardButton(text="➡️",
                                       callback_data='right'))
    mes_id = bot.send_photo(message.chat.id, images[8], caption='Скрыто\\. Нажмите показать\\! 1/' + message.text,  reply_markup=keyboard, parse_mode='MarkdownV2').message_id
    cur.execute('INSERT INTO messages (message_id, status, chat_id) VALUES (?, ?, ?)', (mes_id, status, message.chat.id))
    con.commit()
    con.close()


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def main_menu(call):
    message = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="правила", callback_data='rules'),
                 telebot.types.InlineKeyboardButton(text="роли и способности", callback_data='roles')
                 )
    keyboard.add(telebot.types.InlineKeyboardButton(text="как победить", callback_data='how_win'),
                 telebot.types.InlineKeyboardButton(text="начать игру", callback_data='start_game')
                 )
    media = telebot.types.InputMediaPhoto(media=images['main'])
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=media)
    bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption='''Добро пожаловать в мир "*Библейской Мафии*" – захватывающей игры, где Церковь и Тьма сойдутся в битве лжи и правды, доверия и хитрости, света и тьмы\\!

Здесь ты окажешься в самом центре противостояния Овец и Волков, где каждый ход имеет значение, а истинные намерения скрыты за маской\\.

Готов ли ты бросить вызов\\?

Для начала, ты можешь ознакомиться с правилами игры, ролями и способностями\\.

✨ *Что умеет этот бот:*
📖 *Правила игры:* Узнай общую суть и особенности\\.
🎭 *Роли и способности:* Изучи каждого персонажа и его уникальные действия\\.
🏆 *Как победить\\?:* Разберись с условиями победы для каждой стороны\\.
🔢 *Начать игру:* Собери друзей и окунись в мир "Библейской Мафии"\\!

Нажми на кнопку ниже или используй меню, чтобы начать свое приключение\\! 👇''', reply_markup=keyboard, parse_mode='MarkdownV2')


@bot.callback_query_handler(func=lambda call: call.data == 'rules')
def rules(call):
    message = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="главное меню", callback_data='main_menu'),
                 telebot.types.InlineKeyboardButton(text="роли и способности", callback_data='roles')
                 )
    keyboard.add(telebot.types.InlineKeyboardButton(text="как победить", callback_data='how_win'),
                 telebot.types.InlineKeyboardButton(text="начать игру", callback_data='start_game')
                 )
    media = telebot.types.InputMediaPhoto(media=images['rules'])
    bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id)
    bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption='''📖 *Правила игры “Библейская Мафия”*

Это командная психологическая игра, где участники делятся на две стороны: Церковь \\(Овцы\\) и Тьма \\(Волки\\)\\.

🔄 *Ход игры:*

*1\\. Начало:*
Игроки не знают ролей друг друга\\. Бот случайным образом распределяет роли между участниками\\.

*2\\. Ночь:*
 • Волки и Отец Лжи — выбирают жертву\\.
 • Далида — блокирует одного игрока\\.
 • Отец Лжи — проверяет, является ли выбранный игрок Пророком\\.
 • Змей — исключает одного игрока из игры\\.
 • Молитвенник — исцеляет одного игрока\\.
 • Пророк — проверяет игрока: Волк он или нет\\.

*3\\. День:*
 • Игроки обсуждают произошедшее и делятся подозрениями\\.
 • Все голосуют, кого изгнать\\.
 • Игрок, набравший наибольшее количество голосов, покидает игру\\.

⚠️ *Особенности:*
 • Если Волки и Змей выбрали одну и ту же цель, она покидает игру даже при попытке исцеления\\.
 • Если Волки исключают Далиду — она уходит\\.
 • Если Волки исключают игрока, которого блокировала Далида — оба покидают игру\\.

Это битва доверия и хитрости, света и тьмы\\.
Пусть победит сильнейший\\! ✨''', reply_markup=keyboard,
                             parse_mode='MarkdownV2')


@bot.callback_query_handler(func=lambda call: call.data == 'roles')
def roles(call):
    message = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="главное меню", callback_data='main_menu'),
                 telebot.types.InlineKeyboardButton(text="правила", callback_data='rules')
                 )
    keyboard.add(telebot.types.InlineKeyboardButton(text="как победить", callback_data='how_win'),
                 telebot.types.InlineKeyboardButton(text="начать игру", callback_data='start_game')
                 )
    media = telebot.types.InputMediaPhoto(media=images['roles'])
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=media)
    bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption='''*Подробное описание каждой роли и ее способности в игре*''', reply_markup=keyboard,
                             parse_mode='MarkdownV2')

@bot.callback_query_handler(func=lambda call: call.data == 'how_win')
def how_win(call):
    message = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="главное меню", callback_data='main_menu'),
                 telebot.types.InlineKeyboardButton(text="правила", callback_data='rules')
                 )
    keyboard.add(telebot.types.InlineKeyboardButton(text="как победить", callback_data='how_win'),
                 telebot.types.InlineKeyboardButton(text="начать игру", callback_data='start_game')
                 )
    media = telebot.types.InputMediaPhoto(media=images['how_win'])
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=media)
    bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption='''🏆 *Как одержать победу?*

В этой игре побеждает не самый сильный, а самый проницательный, хитрый и внимательный\\. Каждая роль стремится к своей уникальной цели\\. Победа — за теми, кто исполнит её первым\\!

✨ *Победа Церкви \\(Овцы\\)*
Церковь побеждает, когда все Волки 🐺 и Змей 🐍 изгнаны из игры\\.
Свет восторжествовал, истина победила ложь\\!

🌑 *Победа Волков*
Волки побеждают, если их число становится равным или превышает количество оставшихся Овец\\.
Тьма поглотила невинных — зло взяло верх\\!

🐍 *Победа Змея*
Змей побеждает, если он:
 • остаётся один на один с любым игроком, или становится единственным выжившим\\.
Истинное коварство превзошло всех — он играл только за себя и победил\\!''', reply_markup=keyboard,
                             parse_mode='MarkdownV2')

@bot.callback_query_handler(func=lambda call: call.data == 'start_game')
def start_game(call):
    message = call.message
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="5", callback_data='5_players'),
                 telebot.types.InlineKeyboardButton(text="6", callback_data='6_players'),
                 telebot.types.InlineKeyboardButton(text="7", callback_data='7_players'),
                 telebot.types.InlineKeyboardButton(text="8", callback_data='8_players')
                 )
    keyboard.add(telebot.types.InlineKeyboardButton(text="9", callback_data='9_players'),
                 telebot.types.InlineKeyboardButton(text="10", callback_data='10_players'),
                 telebot.types.InlineKeyboardButton(text="11", callback_data='11_players'),
                 telebot.types.InlineKeyboardButton(text="12", callback_data='12_players')
                 )
    mes_id = bot.send_photo(message.chat.id, images['start'], caption='''*Пришло время начать игру*\\! 🎲  

Первый шаг в нашей "Библейской Мафии" – это *распределение ролей*\\. Каждый из вас получит свою уникальную роль, которая определит ваши цели и способности в этой захватывающей битве\\.  

Но прежде чем мы сможем это сделать, мне нужно узнать, *сколько игроков собралось за вашим столом*\\.  

Ведущий, пожалуйста, выберите количество участников: *от 5 до 12 человек*\\.  

Просто выберите число, соответствующее количеству игроков, и мы продолжим\\! 👇''', reply_markup=keyboard, parse_mode='MarkdownV2', ).message_id
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    cur.execute('UPDATE chats SET status = ? WHERE chat_id = ?', (str(mes_id) + '_2', message.chat.id))
    con.commit()
    con.close()

@bot.callback_query_handler(func=lambda call: (len(str(call.data).split('_')) == 2 and str(call.data).split('_')[1] == 'players'))
def start_game_p(call):
    message = call.message
    num_pla = int(str(call.data).split('_')[0])
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="начать", callback_data='give_cards'))
    bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption='''*Время получить свою роль*\\! 🤫

Теперь, когда количество игроков выбрано, пришло время узнать, кем вы будете в этой игре\\!

*Как это работает*:
1\\. Бот по очереди будет показывать каждому игроку его роль\\.
2\\. Передавайте телефон друг другу по кругу\\.
3\\. Когда телефон окажется у вас, внимательно ознакомьтесь со своей ролью и способностями\\. Запомните их, ведь только вы будете знать, кто вы на самом деле\\!
4\\. После того как вы прочтете и запомните свою роль, нажмите стрелку вправо \\(➡️\\), чтобы передать телефон следующему игроку\\.
5\\. Важно: Не называйте свою роль вслух и не показывайте её другим\\! Сохраняйте интригу\\.

Готовы? Тогда начинаем\\! Передавайте телефон первому игроку\\!''', reply_markup=keyboard, parse_mode='MarkdownV2')
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    cur.execute('UPDATE chats SET status = ? WHERE chat_id = ?', (str(message.message_id) + '_' + str(num_pla), message.chat.id))
    con.commit()
    con.close()

@bot.callback_query_handler(func=lambda call: call.data == 'give_cards')
def give_cards(call):
    message = call.message
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    num = (str(cur.execute('SELECT status FROM chats WHERE chat_id = ?', (message.chat.id,)).fetchall()[0][0]).split('_')[1])
    keyboard = telebot.types.InlineKeyboardMarkup()
    usr = templates[int(num)]
    random.shuffle(usr)
    usr = [str(i) for i in usr]
    mes_id = int(str(cur.execute('SELECT status FROM chats WHERE chat_id = ?', (message.chat.id, )).fetchall()[0][0]).split('_')[0])
    status = num + '-' + '_'.join(usr) + '-0' + '-0'
    keyboard.add(telebot.types.InlineKeyboardButton(text="Показать",
                                       callback_data='show'), telebot.types.InlineKeyboardButton(text="➡️",
                                       callback_data='right'))
    media = telebot.types.InputMediaPhoto(media=images[8])
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=media)
    bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption='', reply_markup=keyboard, parse_mode='MarkdownV2')
    cur.execute('INSERT INTO messages (message_id, status, chat_id) VALUES (?, ?, ?)', (mes_id, status, message.chat.id))
    con.commit()
    con.close()

@bot.callback_query_handler(func=lambda call: call.data == 'finish')
def finish(call):
    message = call.message
    bot.delete_message(message.chat.id, message.message_id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton(text="главное меню", callback_data='main_menu'),
                 telebot.types.InlineKeyboardButton(text="правила", callback_data='rules')
                 )
    keyboard.add(telebot.types.InlineKeyboardButton(text="роли и способности", callback_data='roles'),
                telebot.types.InlineKeyboardButton(text="как победить", callback_data='how_win')
                 )
    keyboard.add(telebot.types.InlineKeyboardButton(text="начать игру", callback_data='start_game'))
    conn = sqlite3.connect('status.db')
    cur = conn.cursor()
    mes_to_change = cur.execute('SELECT main_mes FROM chats WHERE chat_id = ?', (message.chat.id,)).fetchall()[0][0]
    media = telebot.types.InputMediaPhoto(media=images['start'])
    bot.edit_message_media(chat_id=message.chat.id, message_id=mes_to_change, media=media)
    bot.edit_message_caption(chat_id=message.chat.id, message_id=mes_to_change, caption='''Роли распределены\\! ✨

Теперь каждый из вас знает свою тайную роль в этой игре\\. Помните: доверие — это роскошь, а подозрение — ваш главный инструмент\\.

*Да начнется же битва Света и Тьмы*\\!

Наступает ночь\\.\\.\\. Засыпает Церковь\\. Просыпается Тьма\\.''', reply_markup=keyboard,
                             parse_mode='MarkdownV2')


@bot.callback_query_handler(func=lambda call: call.data == 'left')
def mv_left(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    message = call.message
    status = cur.execute('SELECT status FROM messages WHERE message_id = ?', (message.message_id, )).fetchall()[0][0]
    if status.split('-')[-1] != '0':
        if status.split('-')[-1] == '1':
            keyboard.add(telebot.types.InlineKeyboardButton(text="Показать",
                                                            callback_data='show'),
                         telebot.types.InlineKeyboardButton(text="➡️",
                                                            callback_data='right'))
        else:
            keyboard.add(#telebot.types.InlineKeyboardButton(text="⬅️",
                                                         #   callback_data='left'),
                         telebot.types.InlineKeyboardButton(text="Показать",
                                                            callback_data='show'),
                         telebot.types.InlineKeyboardButton(text="➡️",
                                                            callback_data='right'))

        status = f'{'-'.join(status.split('-')[:-2])}-0-{int(status.split('-')[-1]) - 1}'
        cur.execute('UPDATE messages SET status = ? WHERE message_id = ?', (status, message.message_id))
        con.commit()
        media = telebot.types.InputMediaPhoto(media=images[8])
        bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption=f'Скрыто\\. Нажмите показать\\! {int(status.split('-')[-1]) + 1}/{status.split('-')[0]}', reply_markup=keyboard, parse_mode='MarkdownV2')
    con.close()


@bot.callback_query_handler(func=lambda call: call.data == 'right')
def mv_right(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    message = call.message
    status = cur.execute('SELECT status FROM messages WHERE message_id = ?', (message.message_id,)).fetchall()[0][0]
    if int(status.split('-')[-1]) + 1 < int(status.split('-')[0]):
        if int(status.split('-')[-1]) + 2 == int(status.split('-')[0]):
            keyboard.add(#telebot.types.InlineKeyboardButton(text="⬅️",
                                                          #  callback_data='left'),
                         telebot.types.InlineKeyboardButton(text="Показать",
                                                            callback_data='show'),
                         telebot.types.InlineKeyboardButton(text="✅",
                                                            callback_data='finish'))
        else:
            keyboard.add(#telebot.types.InlineKeyboardButton(text="⬅️",
                                                            #callback_data='left'),
                         telebot.types.InlineKeyboardButton(text="Показать",
                                                            callback_data='show'),
                         telebot.types.InlineKeyboardButton(text="➡️",
                                                            callback_data='right'))

        status = f'{'-'.join(status.split('-')[:-2])}-0-{int(status.split('-')[-1]) + 1}'
        cur.execute('UPDATE messages SET status = ? WHERE message_id = ?', (status, message.message_id))
        con.commit()
        media = telebot.types.InputMediaPhoto(media=images[8])
        bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id,
                                 caption=f'Скрыто\\. Нажмите показать\\! {int(status.split('-')[-1]) + 1}/{status.split('-')[0]}', reply_markup=keyboard, parse_mode='MarkdownV2')

    con.close()


@bot.callback_query_handler(func=lambda call: call.data == 'show')
def show_hide(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    con = sqlite3.connect('status.db')
    cur = con.cursor()
    message = call.message
    status = cur.execute('SELECT status FROM messages WHERE message_id = ?', (message.message_id,)).fetchall()[0][0]
    number = int(status.split('-')[1].split('_')[int(status.split('-')[-1])])
    if int(status.split('-')[-1]) == 0:
        keyboard.add(telebot.types.InlineKeyboardButton(text="Показать",
                                                        callback_data='show'),
                     telebot.types.InlineKeyboardButton(text="➡️",
                                                        callback_data='right'))
    elif int(status.split('-')[-1]) + 1 == int(status.split('-')[0]):
        keyboard.add(#telebot.types.InlineKeyboardButton(text="⬅️",
                                                        #callback_data='left'),
                     telebot.types.InlineKeyboardButton(text="Показать",
                                                        callback_data='show'),
                     telebot.types.InlineKeyboardButton(text="✅",
                                                        callback_data='finish'))
    else:
        keyboard.add(#telebot.types.InlineKeyboardButton(text="⬅️",
                                                        #callback_data='left'),
                     telebot.types.InlineKeyboardButton(text="Показать",
                                                        callback_data='show'),
                     telebot.types.InlineKeyboardButton(text="➡️",
                                                        callback_data='right'))

    if status.split('-')[-2] == '0':
        status = f'{'-'.join(status.split('-')[:-2])}-1-{int(status.split('-')[-1])}'
        cur.execute('UPDATE messages SET status = ? WHERE message_id = ?', (status, message.message_id))
        con.commit()
        media = telebot.types.InputMediaPhoto(media=images[number])
        bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id,
                                 caption=f'{des[number]}\n{int(status.split('-')[-1]) + 1}/{status.split('-')[0]}', reply_markup=keyboard, parse_mode='MarkdownV2')
    else:
        status = f'{'-'.join(status.split('-')[:-2])}-0-{int(status.split('-')[-1])}'
        cur.execute('UPDATE messages SET status = ? WHERE message_id = ?', (status, message.message_id))
        con.commit()
        media = telebot.types.InputMediaPhoto(media=images[8])
        bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id)
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id,
                                 caption=f'Скрыто\\. Нажмите показать\\! {int(status.split('-')[-1]) + 1}/{status.split('-')[0]}', reply_markup=keyboard, parse_mode='MarkdownV2')

    con.close()


@bot.message_handler(commands=['start'])
def start(message):
    bot.delete_message(message.chat.id, message.message_id)
    main_start(message)


@bot.message_handler(content_types=['text'])
def text_handle(message):
    conn  = sqlite3.connect('status.db')
    cur = conn.cursor()
    status = cur.execute('SELECT status FROM chats WHERE chat_id = ?', (message.chat.id, )).fetchall()
    if len(status) > 0:
        bot.delete_message(message.chat.id, message.message_id)
    else:
        bot.delete_message(message.chat.id, message.message_id)
        main_start(message)
    # if status[0][0] == 2:
    #     if not message.text.isdigit():
    #         bot.send_message(message.chat.id, 'Введено не число, попробуй ещё раз')
    #     else:
    #         if 5 > int(message.text) or int(message.text) > 12:
    #             bot.send_message(message.chat.id, 'Введено число вне диапазона (от 5 до 12). Попробуй снова')
    #         else:
    #             showing_cards(message)
    # elif status[0][0] == 1:
    #     bot.delete_message(message.chat.id, message.message_id)
    # else:
    #     main_start(message)
    conn.close()


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()