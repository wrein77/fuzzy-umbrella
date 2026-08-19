import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8120622662:AAFuzc5aDdeIVsx4wDr5R3_QI8P8lY5egNA"
ADMIN_ID = 6131629843

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="✉️ Написать сообщение",
                callback_data="feedback"
            )]
        ]
    )

    await message.answer(
        "Привет! 👋\n\n"
        "Здесь можно отправить сообщение владельцу бота.",
        reply_markup=keyboard
    )


@dp.callback_query(F.data == "feedback")
async def feedback(callback):
    await callback.message.answer(
        "✍️ Напиши своё сообщение одним сообщением.\n"
        "Я передам его владельцу."
    )
    await callback.answer()


@dp.message(F.text)
async def receive_message(message: Message):
    if message.from_user.id == ADMIN_ID:
        # Ответ админа пользователю через Reply
        if message.reply_to_message:
            original = message.reply_to_message

            if original.forward_from:
                user_id = original.forward_from.id

                try:
                    await bot.send_message(
                        user_id,
                        f"💬 Ответ:\n\n{message.text}"
                    )
                    await message.answer("✅ Ответ отправлен.")
                except Exception:
                    await message.answer(
                        "❌ Не удалось отправить сообщение пользователю."
                    )
        return

    user = message.from_user

    text = (
        "📩 Новое сообщение\n\n"
        f"👤 Пользователь: {user.full_name}\n"
        f"🆔 ID: {user.id}\n"
        f"🔗 Username: @{user.username if user.username else 'нет'}\n\n"
        f"💬 Сообщение:\n{message.text}"
    )

    await bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

    await bot.send_message(
        ADMIN_ID,
        text
    )

    await message.answer("✅ Сообщение отправлено!")


async def main():
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
