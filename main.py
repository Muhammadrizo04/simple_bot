import re
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import CallbackQuery

TOKEN = "YOUR_BOT_TOKEN"
MAIN_GROUP_ID = YOUR_GROUP_ID  # ID главной группы

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь соответствия филиалов и групп
FILIAL_GROUPS = {
    "YOUR_GROUP_NAME": YOUR_GROUP_ID,  # ID группы для feed up
    "YOUR_GROUP_NAME": -YOUR_GROUP_ID,  # ID группы для oqtepa
    # Добавляй другие филиалы
}

@dp.message()
async def debug_messages(message: types.Message):
    print(f"Получено сообщение из чата {message.chat.id}: {message.text}")


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
        if line.strip().startswith("Yaqin filial:"):
            filial = line.replace("Yaqin filial:", "").strip().lower()
            break

    if filial:
        print(f"✅ Филиал найден: {filial}")
        group_id = FILIAL_GROUPS.get(filial)

        if group_id:
            print(f"📤 Отправляю заказ в группу {group_id}...")
            await bot.send_message(
                chat_id=group_id,
                text=text
            )
            print("✅ Сообщение отправлено!")
        else:
            print("⚠️ Филиал не найден в FILIAL_GROUPS!")
    else:
        print("🚨 Не удалось найти филиал в сообщении!")


# ✅ Обработчик inline-кнопок (в любой группе)
@dp.callback_query()
async def handle_callback(query: CallbackQuery):
    await query.answer(f"Вы нажали: {query.data}")
    await bot.send_message(query.message.chat.id, f"Обработан клик: {query.data}")


async def main():
    await dp.start_polling(bot)  # ✅ Запускаем бота


if __name__ == "__main__":
    asyncio.run(main())  # 🚀 Запускаем бота