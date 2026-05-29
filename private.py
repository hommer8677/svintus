import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from aiogram import F, types
from aiogram.filters import Command, CommandStart

from config import add_player, get_players, ReturnObject

private_router = Router()
private_router.message.filter(F.chat.type == "private")

@private_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Это бот для игры в \"Свинтус\" c друзьями!\n"
                         "Чтобы присоединиться к игре введи код комнаты: ")
@private_router.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Правила игры в \"Свинтус\": \n")
    pass
@private_router.message(F.text.isdigit())
async def join_room(message: types.Message, bot: Bot):
    username = message.from_user.username or message.from_user.first_name
    res: ReturnObject = add_player(username, int(message.text))
    await message.answer(res.message)
    players: dict = get_players(str(res.chat_id))
    if len(players) == 8 and username in players.keys(): await bot.send_message(chat_id=res.chat_id, text="В комнате максимальное количество игроков\nМожно начинать игру")