import functools
import logging
import os
import random
import sqlite3
from contextlib import closing

import telebot
from telebot.apihelper import ApiTelegramException

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(name)s: %(message)s')
log = logging.getLogger('bible_mafia')

TOKEN = os.getenv('BOT_TOKEN', '')  # можно вписать токен прямо сюда строкой
if not TOKEN:
    raise SystemExit('Не задан токен бота: впиши его в TOKEN или задай переменную окружения BOT_TOKEN')


class BotExceptionHandler(telebot.ExceptionHandler):
    """Любая необработанная ошибка внутри telebot логируется, поллинг продолжает работать."""

    def handle(self, exception):
        log.error('Ошибка telebot: %s', exception)
        return True


bot = telebot.TeleBot(TOKEN, exception_handler=BotExceptionHandler())

DB_PATH = 'status.db'

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

MAIN_CAPTION = '''Добро пожаловать в мир "*Библейской Мафии*" – захватывающей игры, где Церковь и Тьма сойдутся в битве лжи и правды, доверия и хитрости, света и тьмы\\!

Здесь ты окажешься в самом центре противостояния Овец и Волков, где каждый ход имеет значение, а истинные намерения скрыты за маской\\.

Готов ли ты бросить вызов\\?

Для начала, ты можешь ознакомиться с правилами игры, ролями и способностями\\.

✨ *Что умеет этот бот:*
📖 *Правила игры:* Узнай общую суть и особенности\\.
🎭 *Роли и способности:* Изучи каждого персонажа и его уникальные действия\\.
🏆 *Как победить\\?:* Разберись с условиями победы для каждой стороны\\.
🔢 *Начать игру:* Собери друзей и окунись в мир "Библейской Мафии"\\!

Нажми на кнопку ниже или используй меню, чтобы начать свое приключение\\! 👇'''

RULES_CAPTION = '''📖 *Правила игры “Библейская Мафия”*

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
Пусть победит сильнейший\\! ✨'''

ROLES_CAPTION = '*Подробное описание каждой роли и ее способности в игре*'

HOW_WIN_CAPTION = '''🏆 *Как одержать победу?*

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
Истинное коварство превзошло всех — он играл только за себя и победил\\!'''

START_CAPTION = '''*Пришло время начать игру*\\! 🎲

Первый шаг в нашей "Библейской Мафии" – это *распределение ролей*\\. Каждый из вас получит свою уникальную роль, которая определит ваши цели и способности в этой захватывающей битве\\.

Но прежде чем мы сможем это сделать, мне нужно узнать, *сколько игроков собралось за вашим столом*\\.

Ведущий, пожалуйста, выберите количество участников: *от 5 до 12 человек*\\.

Просто выберите число, соответствующее количеству игроков, и мы продолжим\\! 👇'''

CARDS_INTRO_CAPTION = '''*Время получить свою роль*\\! 🤫

Теперь, когда количество игроков выбрано, пришло время узнать, кем вы будете в этой игре\\!

*Как это работает*:
1\\. Бот по очереди будет показывать каждому игроку его роль\\.
2\\. Передавайте телефон друг другу по кругу\\.
3\\. Когда телефон окажется у вас, внимательно ознакомьтесь со своей ролью и способностями\\. Запомните их, ведь только вы будете знать, кто вы на самом деле\\!
4\\. После того как вы прочтете и запомните свою роль, нажмите стрелку вправо \\(➡️\\), чтобы передать телефон следующему игроку\\.
5\\. Важно: Не называйте свою роль вслух и не показывайте её другим\\! Сохраняйте интригу\\.

Готовы? Тогда начинаем\\! Передавайте телефон первому игроку\\!'''

FINISH_CAPTION = '''Роли распределены\\! ✨

Теперь каждый из вас знает свою тайную роль в этой игре\\. Помните: доверие — это роскошь, а подозрение — ваш главный инструмент\\.

*Да начнется же битва Света и Тьмы*\\!

Наступает ночь\\.\\.\\. Засыпает Церковь\\. Просыпается Тьма\\.'''


# ---------- БД: таблицы создаются сами, любая ошибка логируется и не роняет бота ----------

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        conn.execute('CREATE TABLE IF NOT EXISTS chats (chat_id INTEGER PRIMARY KEY, status TEXT, main_mes INTEGER)')
        conn.execute('CREATE TABLE IF NOT EXISTS messages (message_id INTEGER PRIMARY KEY, status TEXT, chat_id INTEGER)')


def db_run(query, params=()):
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn, conn:
            conn.execute(query, params)
        return True
    except sqlite3.Error:
        log.exception('Ошибка БД: %s | %s', query, params)
        return False


def db_fetchone(query, params=()):
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            return conn.execute(query, params).fetchone()
    except sqlite3.Error:
        log.exception('Ошибка БД: %s | %s', query, params)
        return None


def get_chat_status(chat_id):
    row = db_fetchone('SELECT status FROM chats WHERE chat_id = ?', (chat_id,))
    return None if row is None or row[0] is None else str(row[0])


def set_chat_status(chat_id, status):
    if db_fetchone('SELECT 1 FROM chats WHERE chat_id = ?', (chat_id,)) is None:
        db_run('INSERT INTO chats (chat_id, status, main_mes) VALUES (?, ?, NULL)', (chat_id, status))
    else:
        db_run('UPDATE chats SET status = ? WHERE chat_id = ?', (status, chat_id))


def get_message_status(message_id):
    row = db_fetchone('SELECT status FROM messages WHERE message_id = ?', (message_id,))
    return None if row is None or row[0] is None else str(row[0])


def set_message_status(message_id, chat_id, status):
    if db_fetchone('SELECT 1 FROM messages WHERE message_id = ?', (message_id,)) is None:
        db_run('INSERT INTO messages (message_id, status, chat_id) VALUES (?, ?, ?)', (message_id, status, chat_id))
    else:
        db_run('UPDATE messages SET status = ? WHERE message_id = ?', (status, message_id))


# ---------- безопасные вызовы Telegram ----------

def tg_call(func, *args, **kwargs):
    """Вызов Telegram API, который никогда не роняет обработчик."""
    try:
        return func(*args, **kwargs)
    except ApiTelegramException as e:
        # повторное нажатие кнопки на том же экране — это не ошибка
        if 'message is not modified' not in str(e):
            log.warning('Telegram API (%s): %s', getattr(func, '__name__', func), e)
    except Exception:
        log.exception('Сбой вызова %s', getattr(func, '__name__', func))
    return None


def show_screen(chat_id, message_id, image, caption, keyboard):
    media = telebot.types.InputMediaPhoto(media=image)
    tg_call(bot.edit_message_media, media=media, chat_id=chat_id, message_id=message_id)
    tg_call(bot.edit_message_caption, chat_id=chat_id, message_id=message_id, caption=caption,
            reply_markup=keyboard, parse_mode='MarkdownV2')


def kb(*rows):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for row in rows:
        keyboard.add(*[telebot.types.InlineKeyboardButton(text=text, callback_data=data) for text, data in row])
    return keyboard


def safe_message_handler(func):
    @functools.wraps(func)
    def wrapper(message):
        try:
            func(message)
        except Exception:
            log.exception('Ошибка в обработчике %s', func.__name__)
    return wrapper


def safe_callback_handler(func):
    @functools.wraps(func)
    def wrapper(call):
        try:
            func(call)
        except Exception:
            log.exception('Ошибка в обработчике %s', func.__name__)
        finally:
            try:
                bot.answer_callback_query(call.id)  # убираем «часики» на кнопке
            except Exception:
                pass
    return wrapper


# ---------- статус раздачи карт: 'N-r1_r2_..._rN-<показана ли карта>-<номер игрока>' ----------

def parse_card_status(status):
    try:
        total_s, order_s, shown_s, idx_s = str(status).split('-')
        total, idx = int(total_s), int(idx_s)
        order = order_s.split('_')
    except (ValueError, TypeError):
        return None
    if len(order) != total or not 0 <= idx < total:
        return None
    return total, order, shown_s == '1', idx


def build_card_status(total, order, shown, idx):
    return '{}-{}-{}-{}'.format(total, '_'.join(order), '1' if shown else '0', idx)


def hidden_caption(total, idx):
    return 'Скрыто\\. Нажмите показать\\! {}/{}'.format(idx + 1, total)


def card_keyboard(total, idx):
    if idx + 1 >= total:
        return kb([('Показать', 'show'), ('✅', 'finish')])
    return kb([('Показать', 'show'), ('➡️', 'right')])


def main_menu_keyboard():
    return kb(
        [('правила', 'rules'), ('роли и способности', 'roles')],
        [('как победить', 'how_win'), ('начать игру', 'start_game')],
    )


def main_start(message):
    sent = tg_call(bot.send_photo, message.chat.id, images['main'], caption=MAIN_CAPTION,
                   reply_markup=main_menu_keyboard(), parse_mode='MarkdownV2')
    if sent is None:
        return
    row = db_fetchone('SELECT main_mes FROM chats WHERE chat_id = ?', (message.chat.id,))
    if row is None:
        db_run('INSERT INTO chats (chat_id, status, main_mes) VALUES (?, ?, ?)',
               (message.chat.id, '1', sent.message_id))
    else:
        if row[0] is not None:
            tg_call(bot.unpin_chat_message, message.chat.id, row[0])
            tg_call(bot.delete_message, message.chat.id, row[0])
        db_run('UPDATE chats SET status = ?, main_mes = ? WHERE chat_id = ?',
               ('1', sent.message_id, message.chat.id))
    if tg_call(bot.pin_chat_message, message.chat.id, sent.message_id, disable_notification=True):
        tg_call(bot.delete_message, message.chat.id, sent.message_id + 1)  # служебное сообщение «закрепил»


def showing_cards(message):
    """Старый текстовый сценарий выбора числа игроков (сейчас не используется)."""
    num = int(message.text)
    if num not in templates:
        return
    order = [str(i) for i in templates[num]]
    random.shuffle(order)
    sent = tg_call(bot.send_photo, message.chat.id, images[8], caption=hidden_caption(num, 0),
                   reply_markup=card_keyboard(num, 0), parse_mode='MarkdownV2')
    if sent is None:
        return
    set_chat_status(message.chat.id, '2')
    set_message_status(sent.message_id, message.chat.id, build_card_status(num, order, False, 0))


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
@safe_callback_handler
def main_menu(call):
    show_screen(call.message.chat.id, call.message.message_id, images['main'], MAIN_CAPTION, main_menu_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == 'rules')
@safe_callback_handler
def rules(call):
    keyboard = kb(
        [('главное меню', 'main_menu'), ('роли и способности', 'roles')],
        [('как победить', 'how_win'), ('начать игру', 'start_game')],
    )
    show_screen(call.message.chat.id, call.message.message_id, images['rules'], RULES_CAPTION, keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'roles')
@safe_callback_handler
def roles_menu(call):  # переименовано: раньше функция затеняла словарь roles
    keyboard = kb(
        [('главное меню', 'main_menu'), ('правила', 'rules')],
        [('как победить', 'how_win'), ('начать игру', 'start_game')],
    )
    show_screen(call.message.chat.id, call.message.message_id, images['roles'], ROLES_CAPTION, keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'how_win')
@safe_callback_handler
def how_win(call):
    keyboard = kb(
        [('главное меню', 'main_menu'), ('правила', 'rules')],
        [('роли и способности', 'roles'), ('начать игру', 'start_game')],  # было how_win: кнопка вела сама на себя
    )
    show_screen(call.message.chat.id, call.message.message_id, images['how_win'], HOW_WIN_CAPTION, keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'start_game')
@safe_callback_handler
def start_game(call):
    message = call.message
    keyboard = kb(
        [(str(n), '{}_players'.format(n)) for n in (5, 6, 7, 8)],
        [(str(n), '{}_players'.format(n)) for n in (9, 10, 11, 12)],
    )
    sent = tg_call(bot.send_photo, message.chat.id, images['start'], caption=START_CAPTION,
                   reply_markup=keyboard, parse_mode='MarkdownV2')
    if sent is not None:
        set_chat_status(message.chat.id, '{}_2'.format(sent.message_id))


@bot.callback_query_handler(func=lambda call: len(str(call.data).split('_')) == 2 and str(call.data).split('_')[1] == 'players')
@safe_callback_handler
def start_game_p(call):
    message = call.message
    num_part = str(call.data).split('_')[0]
    if not num_part.isdigit() or int(num_part) not in templates:
        return
    keyboard = kb([('начать', 'give_cards')])
    tg_call(bot.edit_message_caption, chat_id=message.chat.id, message_id=message.message_id,
            caption=CARDS_INTRO_CAPTION, reply_markup=keyboard, parse_mode='MarkdownV2')
    set_chat_status(message.chat.id, '{}_{}'.format(message.message_id, num_part))


@bot.callback_query_handler(func=lambda call: call.data == 'give_cards')
@safe_callback_handler
def give_cards(call):
    message = call.message
    status = get_chat_status(message.chat.id) or ''
    parts = status.split('_')
    if len(parts) != 2 or not parts[1].isdigit() or int(parts[1]) not in templates:
        tg_call(bot.answer_callback_query, call.id, 'Игра не найдена, нажмите «начать игру» заново')
        return
    num = int(parts[1])
    order = [str(i) for i in templates[num]]  # копия: раньше shuffle перемешивал сам шаблон
    random.shuffle(order)
    show_screen(message.chat.id, message.message_id, images[8], hidden_caption(num, 0), card_keyboard(num, 0))
    set_message_status(message.message_id, message.chat.id, build_card_status(num, order, False, 0))


@bot.callback_query_handler(func=lambda call: call.data == 'finish')
@safe_callback_handler
def finish(call):
    message = call.message
    tg_call(bot.delete_message, message.chat.id, message.message_id)
    db_run('DELETE FROM messages WHERE message_id = ?', (message.message_id,))
    row = db_fetchone('SELECT main_mes FROM chats WHERE chat_id = ?', (message.chat.id,))
    if row is None or row[0] is None:
        return
    keyboard = kb(
        [('главное меню', 'main_menu'), ('правила', 'rules')],
        [('роли и способности', 'roles'), ('как победить', 'how_win')],
        [('начать игру', 'start_game')],
    )
    show_screen(message.chat.id, row[0], images['start'], FINISH_CAPTION, keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'left')
@safe_callback_handler
def mv_left(call):
    message = call.message
    parsed = parse_card_status(get_message_status(message.message_id))
    if parsed is None:
        return
    total, order, _, idx = parsed
    if idx <= 0:
        return
    idx -= 1
    set_message_status(message.message_id, message.chat.id, build_card_status(total, order, False, idx))
    show_screen(message.chat.id, message.message_id, images[8], hidden_caption(total, idx), card_keyboard(total, idx))


@bot.callback_query_handler(func=lambda call: call.data == 'right')
@safe_callback_handler
def mv_right(call):
    message = call.message
    parsed = parse_card_status(get_message_status(message.message_id))
    if parsed is None:
        return
    total, order, _, idx = parsed
    if idx + 1 >= total:
        return
    idx += 1
    set_message_status(message.message_id, message.chat.id, build_card_status(total, order, False, idx))
    show_screen(message.chat.id, message.message_id, images[8], hidden_caption(total, idx), card_keyboard(total, idx))


@bot.callback_query_handler(func=lambda call: call.data == 'show')
@safe_callback_handler
def show_hide(call):
    message = call.message
    parsed = parse_card_status(get_message_status(message.message_id))
    if parsed is None:
        return
    total, order, shown, idx = parsed
    try:
        number = int(order[idx])
    except (ValueError, IndexError):
        return
    if number not in des or number not in images:
        return
    keyboard = card_keyboard(total, idx)
    set_message_status(message.message_id, message.chat.id, build_card_status(total, order, not shown, idx))
    if shown:
        show_screen(message.chat.id, message.message_id, images[8], hidden_caption(total, idx), keyboard)
    else:
        caption = '{}\n{}/{}'.format(des[number], idx + 1, total)
        show_screen(message.chat.id, message.message_id, images[number], caption, keyboard)


@bot.message_handler(commands=['start'])
@safe_message_handler
def start(message):
    tg_call(bot.delete_message, message.chat.id, message.message_id)
    main_start(message)


@bot.message_handler(content_types=['text'])
@safe_message_handler
def text_handle(message):
    known_chat = get_chat_status(message.chat.id) is not None
    tg_call(bot.delete_message, message.chat.id, message.message_id)
    if not known_chat:
        main_start(message)


def main():
    init_db()
    log.info('Бот запущен')
    bot.infinity_polling(timeout=30, long_polling_timeout=30, logger_level=logging.ERROR)


if __name__ == '__main__':
    main()
