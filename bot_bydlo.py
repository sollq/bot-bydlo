import asyncio
from g4f.client import AsyncClient
from g4f.Provider import Aichatos
from aiogram import Router, Bot, Dispatcher, F, types
from config import BOT_TOKEN, DONT_UNDERSTAND_MESSAGE, GPT_MODEL, TIMER_INTERVAL, SYSTEM_MESSAGE, YOUR_USERNAME

router = Router(name=__name__)
lock = asyncio.Lock()

async def response_gpt(message):
    await asyncio.sleep(1)
    client = AsyncClient(provider=Aichatos)
    try:
        completion = await client.chat.completions.create(
            model=GPT_MODEL,
            messages=message,
        )

        return completion.choices[0].message.content

    except Exception as ex:
        print(f"Error during GPT response generation: {ex}")
        return None

@router.business_message(F.text)
@router.message(F.text)
async def handler_message(message: types.Message):
    async with lock:
        await (100)
        user_id = message.chat.id
        print(f"Received message from {user_id}: {message.text}")
        if message.from_user.username == YOUR_USERNAME:
            return None
       
        
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": message.text}
        ]

        response = await response_gpt(messages)

        if response is None:
            await message.answer(DONT_UNDERSTAND_MESSAGE)
        else:
            print(f"Response sent to chat: {response}")
            await message.answer(response)
        
        await asyncio.sleep(TIMER_INTERVAL)

async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
