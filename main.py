import re
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery

TOKEN = "7111396804:AAH9_Y1mKMdBxMAva_s9jMOe_1hMjTge5VY"
MAIN_GROUP_ID = -4624059660  # ID главной группы

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь соответствия филиалов и групп
FILIAL_GROUPS = {
    "feed up": -1002190451115,  # ID группы для feed up
    "yuboring": -1002190451115,  # ID группы для feed up
    "PAYITAHT RESTAURANT": -4758720469,  # ID группы для oqtepa
    # Добавляй другие филиалы
}

@dp.message()
async def process_order(message: types.Message):
    text = message.text

    if not text:
        return  # Если текста нет, игнорируем

    print(f"🔍 Полученный текст:\n{text}")

    # Проверяем, если сообщение от бота, но не переслано
    if message.from_user and message.from_user.is_bot:
        print("🤖 Сообщение от другого бота, обрабатываю...")

    lines = text.split("\n")
    filial = None

    for line in lines:
        if line.strip().startswith("Do'stlaringizga"):
            filial = "yuboring"
            break

    if filial:
        print(f"✅ Филиал найден: {filial}")
        group_id = FILIAL_GROUPS.get(filial)

        if group_id:
            print(f"📤 Отправляю заказ в группу {group_id}...")
            # Форвардим сообщение вместе с инлайн кнопками
            await message.forward(chat_id=group_id)
            print("✅ Сообщение переслано!")
        else:
            print("⚠️ Филиал не найден в FILIAL_GROUPS!")
    else:
        print("🚨 Не удалось найти филиал в сообщении!")

@dp.callback_query()
async def handle_callback(query: CallbackQuery):
    await query.answer(f"Вы нажали: {query.data}")
    await bot.send_message(query.message.chat.id, f"Обработан клик: {query.data}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

