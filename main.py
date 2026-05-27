import os, asyncio, logging
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from aiogram import F, types

from private import private_router
from group import group_router

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def setup_bot_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[BotCommand(command="start", description="Запуск бота")],
        scope=BotCommandScopeAllPrivateChats()
    )
    await bot.set_my_commands(
        commands=[
            BotCommand(command="game", description="Начать игру")
        ],
        scope=BotCommandScopeAllGroupChats()
    )

async def main():
    dp.include_routers(private_router, group_router)
    await setup_bot_commands(bot)
    await dp.start_polling(bot)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
    except Exception:
        logging.exception("Бот остановлен из-за ошибки")
        raise