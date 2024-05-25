from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date


sql_client = KeyboardButton('Записаться')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(sql_client)

#Запись

markup_write = InlineKeyboardMarkup(row_width=1)
btn_write = InlineKeyboardButton(text="Записаться", callback_data="write")

markup_write.add(btn_write)


#День
markup_day = ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
btn_day = []
today = date.today()
for i in range (1, 32):
    if i == today.day:
        if today.month == 2:
            for j in range (i, 29):
                btn_day.append(KeyboardButton(text=str(j)))
                
        elif today.month % 2 == 0 and today.month != 8:
            for j in range (i, 31):
                markup_day.add(KeyboardButton(text=str(i)))
                
        else:
            for j in range (i, 32):
                markup_day.add(KeyboardButton(text=str(i)))

markup_day.add(*btn_day)





# #Время
# btn_10m = KeyboardButton('10:00')
# btn_12m = KeyboardButton('12:00')
# btn_14m = KeyboardButton('14:00')
# btn_16m = KeyboardButton('16:00')
# btn_18m = KeyboardButton('18:00')
# btn_20m = KeyboardButton('20:00')
# time_markup = ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
# time_markup.add(btn_10m, btn_12m, btn_14m, btn_16m, btn_18m, btn_20m)








# #Месяц

# markup_mouth = InlineKeyboardMarkup(row_width=4)
# btn_01 = InlineKeyboardButton(text="Январь", callback_data="01")
# btn_02 = InlineKeyboardButton(text = "Февраль", callback_data="02")
# btn_03 = InlineKeyboardButton(text="Март", callback_data="03")
# btn_04 = InlineKeyboardButton(text = "Апрель", callback_data="04")
# btn_05 = InlineKeyboardButton(text="Май", callback_data="05")
# btn_06 = InlineKeyboardButton(text = "Июнь", callback_data="06")
# btn_07 = InlineKeyboardButton(text="Июль", callback_data="07")
# btn_08 = InlineKeyboardButton(text = "Август", callback_data="08")
# btn_09 = InlineKeyboardButton(text="Сентябрь", callback_data="09")
# btn_10 = InlineKeyboardButton(text = "Октябрь", callback_data="10")
# btn_11 = InlineKeyboardButton(text="Ноябрь", callback_data="11")
# btn_12 = InlineKeyboardButton(text = "Декабрь", callback_data="12")


# markup_day_30 = ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
# markup_day_28 = ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
# btn_01 = KeyboardButton(text="1")
# btn_02 = KeyboardButton(text="2")
# btn_03 = KeyboardButton(text="3")
# btn_04 = KeyboardButton(text="4")
# btn_05 = KeyboardButton(text="5")
# btn_06 = KeyboardButton(text="6")
# btn_07 = KeyboardButton(text="7")
# btn_08 = KeyboardButton(text="8")
# btn_09 = KeyboardButton(text="9")
# btn_10 = KeyboardButton(text="10")
# btn_11 = KeyboardButton(text="11")
# btn_12 = KeyboardButton(text="12")
# btn_13 = KeyboardButton(text="13")
# btn_14 = KeyboardButton(text="14")
# btn_15 = KeyboardButton(text="15")
# btn_16 = KeyboardButton(text="16")
# btn_17 = KeyboardButton(text="17")
# btn_18 = KeyboardButton(text="18")
# btn_19 = KeyboardButton(text="19")
# btn_20 = KeyboardButton(text="20")
# btn_21 = KeyboardButton(text="21")
# btn_22 = KeyboardButton(text="22")
# btn_23 = KeyboardButton(text="23")
# btn_24 = KeyboardButton(text="24")
# btn_25 = KeyboardButton(text="25")
# btn_26 = KeyboardButton(text="26")
# btn_27 = KeyboardButton(text="27")
# btn_28 = KeyboardButton(text="28")
# btn_29 = KeyboardButton(text="29")
# btn_30 = KeyboardButton(text="30")
# btn_31 = KeyboardButton(text="31")

# markup_day_31.add(btn_01, btn_02, btn_03, btn_04, btn_05, btn_06,
#                btn_07, btn_08, btn_09, btn_10, btn_11, btn_12,
#                btn_13, btn_14, btn_15, btn_16, btn_17, btn_18, btn_19, 
#                btn_20, btn_21, btn_22, btn_23, btn_24, btn_25, btn_26,
#                btn_27, btn_28, btn_29, btn_30, btn_31)
# markup_day_30.add(btn_01, btn_02, btn_03, btn_04, btn_05, btn_06,
#                btn_07, btn_08, btn_09, btn_10, btn_11, btn_12,
#                btn_13, btn_14, btn_15, btn_16, btn_17, btn_18, btn_19, 
#                btn_20, btn_21, btn_22, btn_23, btn_24, btn_25, btn_26,
#                btn_27, btn_28, btn_29, btn_30)
# markup_day_28.add(btn_01, btn_02, btn_03, btn_04, btn_05, btn_06,
#                btn_07, btn_08, btn_09, btn_10, btn_11, btn_12,
#                btn_13, btn_14, btn_15, btn_16, btn_17, btn_18, btn_19, 
#                btn_20, btn_21, btn_22, btn_23, btn_24, btn_25, btn_26,
#                btn_27, btn_28, btn_28)
