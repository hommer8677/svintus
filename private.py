import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from aiogram import F, types
from aiogram.filters import Command, CommandStart

private_router = Router()
private_router.message.filter(F.chat.type == "private")

@private_router.message(CommandStart)
async def start(message: types.Message):
    await message.answer("Это бот для игры в \"Свинтус\" c друзьями!\n"
                         "Чтобы присоединиться к игре введи код комнаты: ")
@private_router.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Правила игры в \"Свинтус\": \n")
    pass
@private_router.message(F.text.isdigit())
async def join_room(message: types.Message):
    print('это цифры')
    await message.answer("Вы присоединились к комнате с кодом: " + message.text)