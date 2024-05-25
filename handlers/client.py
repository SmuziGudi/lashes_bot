from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import client_kb, admin_kb
from handlers import admin
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import date
todays = date.today()


class FSMAdmin(StatesGroup):
    date_f = State()
    weekend = State()
#start, help
async def command_start(message : types.Message):
    try:   
        await message.answer('👋Dobrý den {0},Jsem pomocník Ari. Pojďme se se mnou objednat na řasy a já ji předám tvoji objednávku🫶🏻'.format(message.from_user.first_name), reply_markup=client_kb.markup_write)
        # await bot.send_photo(message.chat.id, photo=open('handlers\img\olga.jpg', 'rb'))
        
        await message.delete()
        await bot.send_message(chat_id=955818676, text=f'Пользователь {message.from_user.first_name} зашёл в чат с ботом') # арина
        await bot.send_message(chat_id=692604698, text=f'Пользователь {message.from_user.first_name} зашёл в чат с ботом') # я
    except:
        await message.reply('Общение с ботом через ЛС: https://t.me/Ari_shki_bot')

#Информация о салоне

async def repeat_all_messages(message): # Название функции не играет никакой роли
    await message.answer(text="/start")

async def sql_read_client(message: types.Message):
    await FSMAdmin.date_f.set()
    await bot.send_message(chat_id=message.chat.id, text=f'Введи дату по которой будет производиться поиск в формате (День-Месяц)')
async def sql_read_client_date(message: types.Message, state: FSMContext): 
    try:   
        async with state.proxy() as data:
            data['date_f'] = message.text
        answer = await sqlite_db.sql_read_command(message.text)
        await bot.send_message(chat_id=message.chat.id, text=f'Вот что мне удалось найти по введенной дате')
        for i in answer:
            await message.answer(i)
        await state.finish()
    except:
        await bot.send_message(message.chat.id, text='На данную дату записей нет')
        await state.finish()
    
async def admin_def(message: types.Message):
    await message.answer(text='Что вы хотите сделать?\n\n/Добавить - добавить выходной день\n/Обзор - просмотреть выходные\n/Обновить - обновить старый и ближайший месяц\n/Запись поиск записей по дате', reply_markup=admin_kb.kb_admin)

async def weekends(message: types.Message):
    await FSMAdmin.weekend.set()
    await message.answer(f'Введи дату выходного дня в {todays.month} месяце')

async def weekends_set(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weekend'] = message.text
    try:
        await sqlite_db.sql_add_weekend(message.text)
        await state.finish()
        await message.answer('Выходной день добавлен')
    except:
        await message.answer('Некорректный тип данных попробуй ввести дату в формате (День-Mесяц)')

async def read_weekends(message: types.Message):
    await sqlite_db.sql_read_weekends(message)

async def update(message: types.Message):
    await sqlite_db.sql_add_month()
    await message.answer('Месяц обновлен')


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(admin.sql_client, text = 'Записаться', state=None)
    dp.register_message_handler(sql_read_client, commands=['Запись'])
    dp.register_message_handler(sql_read_client_date, state=FSMAdmin.date_f)
    dp.register_message_handler(admin_def, commands=['admin_ari'], state=None)
    dp.register_message_handler(weekends, commands=['добавить'])
    dp.register_message_handler(weekends_set, state=FSMAdmin.weekend)
    dp.register_message_handler(read_weekends, commands = ['Обзор'])
    dp.register_message_handler(update, commands = ['обновить'])
    dp.register_message_handler(admin.delete_client, commands=['Удалить'], state=None)
    dp.register_message_handler(repeat_all_messages, content_types=["text"])
    



async def cancel(call: types.CallbackQuery):
    await call.message.edit_text('Что вас интересует?')

def register_callback_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(admin.delete_client, lambda c: c.data == 'delete')
    dp.register_callback_query_handler(cancel, lambda c: c.data == 'cancel')
    dp.register_callback_query_handler(admin.sql_client, lambda c: c.data == 'write')
