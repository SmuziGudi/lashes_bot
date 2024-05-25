import sqlite3 as sq
from create_bot import bot
import datetime
import calendar
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re

base = sq.connect('ari_bot.db')
cur = base.cursor()

def sql_start():   
 
    if base:
        print('База данных подключена')
    cur.execute('CREATE TABLE IF NOT EXISTS users(CHAT_ID INTEGER, Number INTEGER, Name TEXT, usl TEXT, Date TEXT, Time TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS gragh(date TEXT, weekend TEXT, time_10am TEXT, time_1pm TEXT, time_4pm TEXT, time_7pm TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS users_data(CHAT_ID INTEGER, Number INTEGER, Name TEXT)')
    base.commit()

today = datetime.date.today()


def chatid(message):
    chat_id = []
    for i in cur.execute('SELECT * FROM users WHERE CHAT_ID = ?', tuple([message])).fetchall():
        chat_id.append(i[4])
        chat_id.append(i[5])
    return chat_id
def client_search(message):
    user = []
    for i in cur.execute('SELECT * FROM users_data WHERE CHAT_ID = ?', tuple([message])).fetchall():
        user.append(i[0])
        user.append(i[1])
        user.append(i[2])
        return user
# def number(message):
#     for i in cur.execute('SELECT * FROM users WHERE Number = ?', tuple([message])).fetchall():
#         return i

def reset_date():
    for i in cur.execute('SELECT * FROM users WHERE CHAT_ID = ?').fetchall():
        cur.execute('UPDATE gragh SET weekend = ? WHERE date = ?', ('n', i[0]))
        base.commit()

async def sql_add_month():
    cur.execute('DELETE FROM gragh')
    for i in range(1, calendar.monthrange(today.year, today.month)[1] + 1):
        date = f'{i}-{today.month}'
        # cur.execute('INSERT INTO gragh VALUES(?, ?, ?, ?, ?, ?)', (date, 'n', 'n', 'n', 'n', 'n', ))
        cur.execute('INSERT INTO gragh VALUES(?, ?, ?, ?, ?, ?)', (date, 'n', 'n', 'n', 'n', 'n', ))
    base.commit()
    for j in range(1, calendar.monthrange(today.year, today.month+1)[1] + 1):
        date_n = f'{j}-{today.month+1}'
        # cur.execute('INSERT INTO gragh VALUES(?, ?, ?, ?, ?, ?)', (date_n, 'n', 'n', 'n', 'n', 'n', ))
        cur.execute('INSERT INTO gragh VALUES(?, ?, ?, ?, ?, ?)', (date_n, 'n', 'n', 'n', 'n', 'n', ))    
    base.commit()

#след месяц
btn_next = InlineKeyboardButton(text='➡️', callback_data='next')
btn_prev = InlineKeyboardButton(text='⬅️', callback_data='prev')
btn_back = InlineKeyboardButton(text='Назад', callback_data='back')
def nextmonth_day():
    nm_day = InlineKeyboardMarkup(row_width=5, resize_keyboard=True)
    btn_day = []
    for i in cur.execute("SELECT * FROM gragh WHERE weekend = ?", ("n", )).fetchall():
        td = re.split('-', i[0])
        if int(td[0]) >= 1 and int(td[1]) >= today.month+1:
            btn_day.append(InlineKeyboardButton(text=str(i[0]), callback_data=f'day_{str(i[0])}'))
        else:
            continue    
    nm_day = nm_day.add(*btn_day).row(btn_prev) 
    del btn_day
    return nm_day

#День

def day_btn():
    day_markup = InlineKeyboardMarkup(row_width=5, resize_keyboard=True)
    btn_day = []
    for i in cur.execute("SELECT * FROM gragh WHERE weekend = ?", ("n",)).fetchall():
        td = re.split('-', i[0])
        if int(td[0]) >= today.day and int(td[1]) != today.month+1:
            btn_day.append(InlineKeyboardButton(text=str(i[0]), callback_data=f'day_{str(i[0])}'))
        else:
            continue
    
    day_markup = day_markup.add(*btn_day).row(btn_next) 
    del btn_day
    return day_markup

async def delete_date(message):
    for date in cur.execute('SELECT * FROM users WHERE CHAT_ID = ?', tuple([message])).fetchall():
        date_m = date[4]
        time = date[5]
        if time == '10am - 1pm':
            cur.execute(f'UPDATE gragh SET time_10am = ? WHERE date = ?', ('n', date_m))
        if time == '1pm - 4pm':
            cur.execute(f'UPDATE gragh SET time_1pm = ? WHERE date = ?', ('n', date_m))
        if time == '4pm - 7pm':
            cur.execute(f'UPDATE gragh SET time_4pm = ? WHERE date = ?', ('n', date_m))
        if time == '7pm - 10pm':
            cur.execute(f'UPDATE gragh SET time_7pm = ? WHERE date = ?', ('n', date_m))
        base.commit()
    cur.execute('DELETE FROM users WHERE CHAT_ID = ?', tuple([message]))
    base.commit()
    
#Время
def time_btn(message):
    time_markup = InlineKeyboardMarkup(row_width=4, resize_keyboard=True)
    btn_time = []
    for j in cur.execute("SELECT * FROM gragh WHERE date = ?", tuple([message])).fetchall():
        if j[2] == 'y' and j[3] == 'y' and j[4] == 'y' and j[5] == 'y':
            cur.execute('UPDATE gragh SET weekend = ? WHERE date = ?', ('y', j[0]))
            base.commit()
            break
        if j[2] == 'n':
            btn_time.append(InlineKeyboardButton(text='10am - 1pm', callback_data='time_10am - 1pm'))
        if j[3] == 'n':
            btn_time.append(InlineKeyboardButton(text='1pm - 4pm', callback_data='time_1pm - 4pm'))
        if j[4] == 'n':
            btn_time.append(InlineKeyboardButton(text='4pm - 7pm', callback_data='time_4pm - 7pm'))
        if j[5] == 'n':
            btn_time.append(InlineKeyboardButton(text='7pm - 10pm', callback_data='time_7pm - 10pm'))
        
    time_markup = time_markup.add(*btn_time).row(btn_back)
    del btn_time
    return time_markup

# cur.execute('UPDATE gragh SET time_10am = ? WHERE date = ?', ('y', j[0]))

async def sql_add_command(state):
    async with state.proxy() as data:
        hat_id = data['chat_id']
        number = data['number']
        name = data['name']
        cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
        if cur.execute('SELECT * FROM users_data WHERE CHAT_ID = ?', tuple([hat_id])).fetchone() is None:
            cur.execute('INSERT INTO users_data VALUES (?, ?, ?)', tuple([hat_id, number, name]))
        base.commit()
        if data["time"] == '10am - 1pm':
            cur.execute('UPDATE gragh SET time_10am = ? WHERE date = ?', ('y', data["date"]))
        if data["time"] == '1pm - 4pm':
            cur.execute('UPDATE gragh SET time_1pm = ? WHERE date = ?', ('y', data["date"]))
        if data["time"] == '4pm - 7pm':
            cur.execute('UPDATE gragh SET time_4pm = ? WHERE date = ?', ('y', data["date"]))
        if data["time"] == '7pm - 10pm':
            cur.execute('UPDATE gragh SET time_7pm = ? WHERE date = ?', ('y', data["date"]))
        base.commit()
        chat_id = 692604698 # я
        chat_id_a = 955818676 # ари
        message_id = data['chat_id']
        await bot.send_message(chat_id = chat_id_a, text = f'---Новый клиент на: {data["date"]}---\n---Номер телефона: {data["number"]}---\n---Имя: {data["name"]}---\n---Chat_id_Пользователя: {message_id}---\n---Время: {data["time"]}---\n---Услуга: {data["usl"]}---', reply_markup=None)
        await bot.send_message(chat_id = chat_id, text = f'---Новый клиент на: {data["date"]}---\n---Номер телефона: {data["number"]}---\n---Имя: {data["name"]}---\n---Chat_id_Пользователя: {message_id}---\n---Время: {data["time"]}---\n---Услуга: {data["usl"]}---', reply_markup=None)

async def sql_add_weekend(message):
    cur.execute('UPDATE gragh SET weekend = ? WHERE date = ?', ('y', message))
    base.commit()

async def sql_read_command(message):
    answer = []
    for ret in cur.execute("SELECT * FROM users WHERE Date = ?", tuple([message])).fetchall():
        answer.append(f'CHAT_ID: {ret[0]}\nNumber: {ret[1]}\nName: {ret[2]}\nDate: {ret[3]}\nTime: {ret[4]}')
    return answer
async def sql_read_weekends(message):
    for ret in cur.execute("SELECT * FROM gragh WHERE weekend = ?", ('y',)).fetchall():
        await bot.send_message(message.from_user.id, f'Выходной: {ret[0]}')
        base.commit()
