from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

button_contact = KeyboardButton(text='Поделиться контактом', request_contact=True, one_time_keyboard=True)

but_add = KeyboardButton(text='/Добавить')
but_del = KeyboardButton(text='/Обзор')
but_update = KeyboardButton(text='/Обновить')
btn_check = KeyboardButton(text='/запись')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin.add(but_add, but_del, but_update, btn_check)

kb_contact = ReplyKeyboardMarkup(resize_keyboard=True).add(button_contact)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

button_yes = InlineKeyboardButton(text='Да', callback_data='yes')
button_no = InlineKeyboardButton(text='Нет', callback_data='no')

kb_yesNo = InlineKeyboardMarkup(row_width=1).add(button_yes, button_no)


btn_delete = InlineKeyboardButton(text='🗑 Usun', callback_data='delete')
kb_delete = InlineKeyboardMarkup(row_width=1).add(btn_delete)

btn_lam = InlineKeyboardButton(text='Laminace a barvení řas✨', callback_data='usl_lam')
btn_bar = InlineKeyboardButton(text='Barvení obočí ✨', callback_data='usl_bar')
btn_pro = InlineKeyboardButton(text='Prodloužení řas✨', callback_data='usl_pro')
btn_lam_ob = InlineKeyboardButton(text='Laminace a barvení obočí ✨', callback_data='usl_lam_ob')
btn_back = InlineKeyboardButton(text='◀️', callback_data='back_usl')
btn_date = InlineKeyboardButton(text='✅', callback_data='date_usl')

card_markup = InlineKeyboardMarkup(row_width=1).add(btn_date, btn_back)
usl_markup = InlineKeyboardMarkup(row_width=1).add(btn_lam, btn_bar, btn_pro, btn_lam_ob)