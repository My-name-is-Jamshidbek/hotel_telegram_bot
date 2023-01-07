import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from config import *
from buttons import *
from database import *
from states import *



bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#START
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id, "Iltimos menyuni tanlang:", reply_markup=markup_main_menu)

#MAIN MENU
@dp.message_handler()
async def handle_text(message: types.Message):
    if message.text.lower() == "Ma'lumot".lower():
        # send information about the guesthouse
        about = hotel_about()
        await bot.send_message(message.chat.id, f"Nomi: {about[1]}.\nManzil: {about[2]}.\nHaqida: {about[3]}")
    elif message.text.lower() == "Xona bron qilish".lower():
        # send instructions for booking a room
        await bot.send_message(message.chat.id, "Kirish vaqti: yyyy-oo-kk",reply_markup=markup_cancelled)
        await State_book_a_room.check_in_date.set()
    elif message.text.lower() == "Ovqat buyurtma".lower():
        await bot.send_message(message.from_user.id, "Ovqatni tanlang:", reply_markup=menu_food)
        await state_food_order.name.set()
    elif message.text.lower() == "Xona hizmati".lower():
        # send instructions for requesting housekeeping services
        await bot.send_message(message.from_user.id, "Hona hizmat turini tanlang:", reply_markup=menu_housekeeping)
        await state_housekeeping.name.set()
    elif message.text.lower() == "Adminga savol".lower():
        # send instructions for asking the administrator a question
        await bot.send_message(message.chat.id, "Adminga yo'llamoqchi bo'lgan savolingizni jo'nating:",reply_markup=markup_cancelled)
        await state_ask_adminstration.ask.set()

#ASK THE ADMINSTRATIONS
@dp.message_handler(content_types=types.ContentType.TEXT,state=state_ask_adminstration.ask)
async def ask_admin(message:types.Message,state:FSMContext):
    if message.text == "Orqaga":
        await message.answer("Asosiy menyu:",reply_markup=markup_main_menu)
        await state.finish()
    else:
        await bot.send_message(chat_id=ADMIN_ID,text="Yangi savol:\n"+message.text,reply_markup=ask_the_admin(msg_id=message.message_id,user_id=message.from_user.id))
        await message.answer("Savol adminga yo'llandi.",reply_markup=markup_main_menu)
        await state.finish()

#REQUEST ADMIN
@dp.callback_query_handler()
async def handle_housekeeping_request(query: types.CallbackQuery,state:FSMContext):
    if query.data.startswith("answer_"):
        msg_id,user_id = query.data.split("_")[1:]
        await state.update_data(msg_id = msg_id,user_id=user_id)
        await query.message.answer("JAvobni kiriting:")
        await state_answer_admin.answer.set()

@dp.message_handler(content_types=types.ContentType.TEXT,state = state_answer_admin.answer)
async def answer_admin(message:types.Message,state:FSMContext):
    text = message.text
    data = await state.get_data()
    msg_id = data.get("msg_id")
    user_id = data.get("user_id")

    await bot.send_message(chat_id=user_id,reply_to_message_id=msg_id,text=text)
    await message.answer("Javob foydalanuvchiga yetkazildi.")

#HOUSEKEEPING
@dp.message_handler(content_types=types.ContentType.TEXT,state=state_housekeeping.name)
async def name_food_input(message:types.Message,state:FSMContext):
    if message.text == "Orqaga":
        await message.answer("Asosiy menyu:",reply_markup=markup_main_menu)
        await state.finish()
    else:
        await state.update_data(name = message.text)
        await message.answer("Hona raqami:",reply_markup=markup_cancelled)
        await state_housekeeping.room.set()
@dp.message_handler(content_types=types.ContentType.TEXT,state=state_housekeeping.room)
async def name_food_input(message:types.Message,state:FSMContext):
    if message.text == "Orqaga":
        await message.answer("Asosiy menyu:",reply_markup=markup_main_menu)
        await state.finish()
    else:
        data = await state.get_data()
        name = data.get("name")
        await bot.send_message(ADMIN_ID,f"Hona hizmatiga buyurtma:\nTuri: {name}\nHona: {message.text}\nTo'liq ism: {message.from_user.full_name}")
        await message.answer("Buyurtma uchun rahmat.",reply_markup=markup_main_menu)
        await state.finish()

#FOOD ORDER
@dp.message_handler(content_types=types.ContentType.TEXT,state=state_food_order.name)
async def name_food_input(message:types.Message,state:FSMContext):
    if message.text == "Orqaga":
        await message.answer("Asosiy menyu:", reply_markup=markup_main_menu)
        await state.finish()
    else:
        await state.update_data(name = message.text)
        await message.answer("Hona raqami:",reply_markup=markup_cancelled)
        await state_food_order.room.set()
@dp.message_handler(content_types=types.ContentType.TEXT,state=state_food_order.room)
async def name_food_input(message:types.Message,state:FSMContext):
    if message.text == "Orqaga":
        await message.answer("Asosiy menyu:",reply_markup=markup_main_menu)
        await state.finish()
    else:
        data = await state.get_data()
        name = data.get("name")
        await bot.send_message(ADMIN_ID,f"Yangi ovqat buyurtmasi:\nOvqat: {name}\nHona: {message.text}\nTo'liq ism: {message.from_user.full_name}")
        await message.answer("Buyurtma uchun rahmat.",reply_markup=markup_main_menu)
        await state.finish()

#BOOK A ROM
@dp.message_handler(content_types=types.ContentType.TEXT,state=State_book_a_room.check_in_date)
async def check_in_date(message:types.Message,state:FSMContext):
    if message.text == "Orqaga":
        await message.answer("Asosiy menyu:",reply_markup=markup_main_menu)
        await state.finish()
    else:
        if len(message.text) == 10 and len(message.text.split("-")) == 3:
            await state.update_data(check_in_date = message.text)
            await message.answer("Chiqish vaqti: yyyy-oo-kk")
            await State_book_a_room.check_out_date.set()
        else:
            await message.answer("Kiritilgan malumot noto'g'ri!")
@dp.message_handler(content_types=types.ContentType.TEXT,state=State_book_a_room.check_out_date)
async def check_in_date(message:types.Message,state:FSMContext):
    if message.text == "Orqaga":
        await message.answer("Asosiy menyu:",reply_markup=markup_main_menu)
        await state.finish()
    else:
        if len(message.text) == 10 and len(message.text.split("-")) == 3:
            await state.update_data(check_out_date = message.text)
            data = await state.get_data()
            check_in_date = data.get("check_in_date")
            check_out_date = message.text
            if check_out_date.split("-")[0].isdigit() and check_out_date.split("-")[1].isdigit() and check_out_date.split("-")[2].isdigit() and check_in_date.split("-")[0].isdigit() and check_in_date.split("-")[1].isdigit() and check_in_date.split("-")[2].isdigit():
                try:
                    rooms = find_unbookings(query={"check_in_date":check_in_date,"check_out_date":check_out_date})
                    await message.answer("Iltimos hona raqamini kiriting:",reply_markup=markup_rooms(rooms))
                    await State_book_a_room.room_number.set()
                except:
                    await message.answer("Kiritilgan malumot noto'g'ri!",reply_markup=markup_main_menu)
                    await state.finish()
            else:
                await message.answer("Kiritilgan malumot noto'g'ri!",reply_markup=markup_main_menu)
                await state.finish()
        else:
            await message.answer("Kiritilgan malumot noto'g'ri!",reply_markup=markup_main_menu)
            await state.finish()
@dp.message_handler(content_types=types.ContentType.TEXT,state=State_book_a_room.room_number)
async def room_number_input(message:types.Message,state:FSMContext):
    if message.text == "Orqaga":
        await message.answer("Asosiy menyu:",reply_markup=markup_main_menu)
        await state.finish()
    else:
        if len(message.text.split()) == 2:
            data = await state.get_data()
            check_in_date = data.get("check_in_date")
            check_out_date = data.get("check_out_date")
            if message.text.split()[0].isdigit() and find_tek_unbookings(query={"check_in_date":check_in_date,"check_out_date":check_out_date,"num_rooms":int(message.text.split()[0])}):
                try:
                    insert_booking(booking={"check_in_date":check_in_date,"check_out_date":check_out_date,"num_rooms":int(message.text.split()[0]),"tg_id":str(message.from_user.id)})
                    await message.answer("Hona bron ilindi.", reply_markup=markup_main_menu)
                    await state.finish()
                except:
                    await message.answer("hona bron qilinmadi.",reply_markup=markup_main_menu)
                    await state.finish()
            else:
                await message.answer("Kiritilgan malumot noto'g'ri!", reply_markup=markup_main_menu)
                await state.finish()
        else:
            await message.answer("Kiritilgan malumot noto'g'ri!", reply_markup=markup_main_menu)
            await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
