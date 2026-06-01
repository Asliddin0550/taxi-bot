import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

=====================

CONFIG

=====================

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Tokenni Koyeb Environment Variables ga qo'yasiz

ADMIN_ID = 7067809903

CLIENT_GROUP_ID = -1002228149448
DISPATCH_GROUP_ID = -1003952071411

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

=====================

STATES

=====================

class Order(StatesGroup):
from_where = State()
to_where = State()
people = State()
date = State()
time = State()
phone = State()

=====================

CLIENT GROUP HANDLER

=====================

@dp.message(F.chat.id == CLIENT_GROUP_ID)
async def client_group_handler(message: Message):

if message.voice:
    return

if not message.text:
    return

text = message.text.lower()

spam_words = [
    "fargona", "margilon", "toshloq", "qoshtepa",
    "damas", "tel", "+998", "qirg'iziston", "reklama"
]

if any(w in text for w in spam_words):
    return

client_words = [
    "taxi", "kerak", "necha", "odam",
    "bor", "shohimardon", "buyurtma", "salom", "assalom"
]

if any(w in text for w in client_words):
    await message.answer(
        "🚕 Buyurtma berish uchun botga kiring @Shohmardontaxi_bot"
    )

=====================

START (PRIVATE ONLY)

=====================

@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
if message.chat.type != "private":
return

await message.answer("📍 Qayerdan ketasiz?")
await state.set_state(Order.from_where)

=====================

FROM WHERE

=====================

@dp.message(Order.from_where)
async def from_where(message: Message, state: FSMContext):
await state.update_data(from_where=message.text)

await message.answer("🏔 Qayerga borasiz?")
await state.set_state(Order.to_where)

=====================

TO WHERE

=====================

@dp.message(Order.to_where)
async def to_where(message: Message, state: FSMContext):
await state.update_data(to_where=message.text)

await message.answer("👤 Necha kishi?")
await state.set_state(Order.people)

=====================

PEOPLE

=====================

@dp.message(Order.people)
async def people(message: Message, state: FSMContext):
await state.update_data(people=message.text)

await message.answer("📅 Ketish sanasi?")
await state.set_state(Order.date)

=====================

DATE

=====================

@dp.message(Order.date)
async def date(message: Message, state: FSMContext):
await state.update_data(date=message.text)

await message.answer("🕒 Ketish vaqti?")
await state.set_state(Order.time)

=====================

TIME

=====================

@dp.message(Order.time)
async def time(message: Message, state: FSMContext):
await state.update_data(time=message.text)

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

await message.answer("📞 Telefon raqamingizni yuboring:", reply_markup=kb)
await state.set_state(Order.phone)

=====================

FINAL ORDER

=====================

@dp.message(Order.phone)
async def phone(message: Message, state: FSMContext):
data = await state.get_data()

phone = message.contact.phone_number if message.contact else message.text

text = f"""

🚕 YANGI BUYURTMA!

📍 QAYERDAN: {data['from_where']}
🏔 QAYERGA: {data['to_where']}
👤 KISHI SONI: {data['people']}
📅 SANA: {data['date']}
🕒 VAQT: {data['time']}
📞 TELEFON: {phone}

✅ Buyurtma qabul qilindi!
"""

await bot.send_message(ADMIN_ID, text)
await bot.send_message(DISPATCH_GROUP_ID, text)

await message.answer("✅ Rahmat! Buyurtmangiz qabul qilindi 🚕")
await state.clear()

=====================

RUN

=====================

async def main():
await dp.start_polling(bot)

if __name__ == "__main__":
asyncio.run(main())
