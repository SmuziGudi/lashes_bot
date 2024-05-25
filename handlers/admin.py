from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqlite_db
from handlers import client
from keyboards import admin_kb, client_kb 
from datetime import date
import re

todays = date.today()
month_mass = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
class FSMAdmin(StatesGroup):
    chat_id = State()
    number = State()
    name = State()
    usl = State()
    date = []
    time = State()


#@dp.message_handler(text='Запись на приём', state=None)
async def sql_client(message: types.Message, state: FSMContext):
    chat_id = sqlite_db.chatid(message.chat.id)
    user = sqlite_db.client_search(message.chat.id)
    if chat_id:
        await message.answer(f'Ваша запись:\nДата: {chat_id[0]}\nВремя: {chat_id[1]}', reply_markup=admin_kb.kb_delete)
    else:
        if user:
            async with state.proxy() as data:
                data['chat_id'] = user[0]
                data['number'] = user[1]
                data['name'] = user[2]
            await message.answer('Выберите услугу', reply_markup=admin_kb.usl_markup)
        else:
            await FSMAdmin.number.set()
            await message.answer('Поделитесь контактом для дальнейшей записи', reply_markup=admin_kb.kb_contact)

async def sql_client_number(message: types.Message, state: FSMContext):
    number = message.contact.phone_number
    async with state.proxy() as data:
        data['chat_id'] = message.chat.id
        data['number'] = number
        data['name'] = message.contact.first_name
    await message.answer(f"Записал ваш номер: {number}\n{message.contact.first_name}")
    await message.answer('Выберите услугу', reply_markup=admin_kb.usl_markup)
    await FSMAdmin.next()
    await FSMAdmin.next()

async def usl(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer('Выберите услугу', reply_markup=admin_kb.usl_markup)
    await callback_query.answer()

async def usl_card(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await callback_query.message.delete()
        if callback_query.data == 'usl_lam':
            data['usl'] = 'Laminace a barvení řas✨'
            await callback_query.message.answer_photo(photo=open('img/resn1.png', 'rb'), caption='Laminace a barvení řas✨', reply_markup=admin_kb.card_markup)
            await callback_query.answer()
        elif callback_query.data == 'usl_bar':
            data['usl'] = 'Barvení obočí ✨'
            await callback_query.message.answer_photo(photo=open('img/resn2.jpg', 'rb'), caption='Barvení obočí ✨', reply_markup=admin_kb.card_markup)
            await callback_query.answer()
        elif callback_query.data == 'usl_pro':
            data['usl'] = 'Prodloužení řas✨'
            await callback_query.message.answer_photo(photo=open('img/resn3.jpg', 'rb'), caption='Prodloužení řas✨', reply_markup=admin_kb.card_markup)
            await callback_query.answer()
        elif callback_query.data == 'usl_lam_ob':
            data['usl'] = 'Laminace a barvení obočí✨'
            await callback_query.message.answer_photo(photo=open('img/resn4.jpg', 'rb'), caption='Laminace a barvení obočí✨', reply_markup=admin_kb.card_markup)
            await callback_query.answer()
        await FSMAdmin.next()

async def main_menu_date(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    month = month_mass[todays.month-1]
    day_markup = sqlite_db.day_btn()
    await callback_query.message.answer(f'Cейчас {month} выбирай число', reply_markup=day_markup)
    await callback_query.answer()

async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data:
        await callback_query.answer()
        c_d = re.split('day_', callback_query.data)
        c_d = c_d[1]
        async with state.proxy() as data:
            data['date'] = str(c_d)
        time_markup = sqlite_db.time_btn(c_d)
        await callback_query.message.edit_text(f'Отлично, на {c_d} есть свободные окна, выбирай время', reply_markup=time_markup)
        await FSMAdmin.next()
    else:
        await bot.send_message(callback_query.from_user.id, 'Выбери дату')
        await callback_query.answer() 
async def time_client(callback_query: types.CallbackQuery, state: FSMContext):
    t_d = re.split('time_', callback_query.data)
    t_d = t_d[1]
    async with state.proxy() as data:
        data['time'] = str(t_d)
        date_cl = data['date']
    await callback_query.message.edit_text(f'Отлично, записал тебя на {t_d}, \nДата: {date_cl}\nАриша свяжется с тобой чтобы подтвердить запись', reply_markup=None)
    await callback_query.message.answer(f'Ваша запись:\nДата: {date_cl}\nВремя: {t_d}\nУслуга: {data["usl"]}', reply_markup=admin_kb.kb_delete)

    await sqlite_db.sql_add_command(state)
    await state.finish()

async def delete_client(callback_query: types.CallbackQuery):
    await sqlite_db.delete_date(callback_query.message.chat.id)
    await callback_query.message.edit_text('Запись удалена', reply_markup=client_kb.markup_write)

#Отмена записи
#@dp.message_handler(text='Отмена', state='*')
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Запись отменена')
#Регистрируем хендлеры
@dp.callback_query_handler(lambda c: c.data == 'write')
async def write(call: types.CallbackQuery, state: FSMContext):
    await sql_client(call.message, state)
    await call.answer()

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(sql_client_number, content_types=types.ContentType.CONTACT, state=FSMAdmin.number)
    dp.register_message_handler(main_menu_date, state=FSMAdmin.number)
    dp.register_message_handler(cancel, state='*', text=('отмена', 'Отмена'))

async def next(callback_query: types.CallbackQuery):
    nm_day = sqlite_db.nextmonth_day()
    await callback_query.message.edit_text(f'✨příští měsíc✨', reply_markup=nm_day)

def register_callback_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(sql_client, lambda c: c.data == 'rest', state=None)
    dp.register_callback_query_handler(next, lambda c: c.data == 'next', state='*')
    dp.register_callback_query_handler(main_menu_date, lambda c: c.data == 'prev', state='*')
    dp.register_callback_query_handler(main_menu_date, lambda c: c.data == 'back', state='*')
    dp.register_callback_query_handler(main_menu_date, lambda c: c.data == 'date_usl', state='*')
    dp.register_callback_query_handler(usl, lambda c: c.data == 'back_usl', state='*')
    dp.register_callback_query_handler(usl_card, lambda c: c.data.startswith('usl_'), state='*')
    dp.register_callback_query_handler(process_callback, lambda c: c.data.startswith('day'), state="*")
    dp.register_callback_query_handler(time_client, lambda c: c.data.startswith('time'), state="*")