import asyncio, json, random

from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from aiogram import F, types
from aiogram.filters import Command, CommandStart

from config import *

group_router = Router()
group_router.message.filter(F.chat.type.in_({"group", "supergroup"}))

@group_router.message(Command("game"))
async def create_code(message: types.Message):
    code = code_generate()
    chat_id = str(message.chat.id)

    res = append_group(chat_id, code)
    if(res != 1): return await message.answer(f"Игра уже началась! Код игры: <code>{res}</code>", parse_mode='HTML')
    await message.answer(f"Комната создана! Код комнаты: <code>{code}</code>", parse_mode='HTML')