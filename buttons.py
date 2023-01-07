from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

markup_main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
markup_main_menu.add("Ma'lumot","Xona bron qilish","Ovqat buyurtma","Xona hizmati","Adminga savol")

menu_housekeeping = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
menu_housekeeping.add("To'shakni tahlash","Sochiqlarni almashtiring","Xonani tozalash","Orqaga")

menu_food = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
menu_food.add("Pizza", "Hamburger", "Salad","Orqaga")

markup_cancelled = types.ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
markup_cancelled.add("Orqaga")

def markup_rooms(rooms):
    btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in rooms:
        t = f"{i[3]} xona"
        btn.add(types.KeyboardButton(t))
    btn.add(types.KeyboardButton("Orqaga"))
    return btn

def ask_the_admin(msg_id,user_id):
    ask_admin_markup = InlineKeyboardMarkup()
    ask_admin_markup.add(InlineKeyboardButton("Javob berish", callback_data="answer_"+str(msg_id)+"_"+str(user_id)))
    return ask_admin_markup