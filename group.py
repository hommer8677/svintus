import asyncio, json, random

from aiogram import Bot, Dispatcher, Router
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats
from aiogram import F, types
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import code_generate, append_group, get_players, stop_register, get_register_status

group_router = Router()
group_router.message.filter(F.chat.type.in_({"group", "supergroup"}))

@group_router.message(Command("game"))
async def create_code(message: types.Message):
    code = code_generate()
    chat_id = str(message.chat.id)

    res = append_group(chat_id, code)
    if(res != 1): text = f"Регистрация уже идёт! Код игры: <code>{res}</code>"
    else: text = f"Комната создана! Код комнаты: <code>{code}</code>"
    players = get_players(chat_id)
    text += f"\n\nЗарегестрированых участников: {len(players)}"
    if players:
        text += "".join(['\n@'+i for i in players.keys()])

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="🏁 Завершить регистрацию (Админ)", 
        callback_data="stop_reg" # Ключ, который мы будем ловить при нажатии
    ))
    return await message.answer(
        text, 
        reply_markup=builder.as_markup(), # Прикрепляем кнопку
        disable_notification=True, 
        parse_mode='HTML'
    )

@group_router.message(Command("stop"))
async def stop(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    user_id = message.from_user.id

    players: dict = get_players(str(chat_id))
    if len(players) in {0,1}: return await message.answer("В игре зарегестрировано недостаточно учаcтников")
    if get_register_status(str(chat_id)): return await message.answer("Регистрация уже закрыта")

    member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if member.status not in ["administrator", "creator"]:
        return await message.answer(
            "❌ Только администратор группы может завершить регистрацию!"
        )

    stop_register(str(chat_id))
    
    players_mentions = "".join([f"\n@{name}" for name in players.keys()])
    await message.answer(
        f"🏁 Регистрация завершена администратором!\n"
        f"Игроков в игре: {len(players)}.{players_mentions} \nРассылаю карты в ЛС..."
    )
    for name, p_id in players.items():
        try:
            await bot.send_message(
                chat_id=p_id,
                text=f"🎮 Игра начата администратором чата!\nВаши карты: [Раздача]"
            )
        except Exception as e:
            #print(f"Не удалось написать игроку {name}: {e}")
            pass

@group_router.callback_query(F.data == "stop_reg")
async def handle_stop_registration(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    if get_register_status(str(chat_id)): return await callback.message("Регистрация уже закрыта", show_allert=True)

    member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if member.status not in ["administrator", "creator"]:
        return await callback.answer(
            "❌ Только администратор группы может завершить регистрацию!", 
            show_alert=True # Покажет всплывающее окошко по центру экрана
        )
    
    players_dict = get_players(str(chat_id))
    players_mentions = "".join([f"\n@{name}" for name in players_dict.keys()])
    if len(players_dict) < 2:
        return await callback.answer(
            "❌ Нельзя начать игру! Нужно минимум 2 игрока.", 
            show_alert=True
        )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        f"🏁 Регистрация завершена администратором!\n"
        f"Игроков в игре: {len(players_dict)}.{players_mentions} \nРассылаю карты в ЛС..."
    )
    for name, p_id in players_dict.items():
        try:
            await bot.send_message(
                chat_id=p_id,
                text=f"🎮 Игра начата администратором чата!\nВаши карты: [Раздача]"
            )
        except Exception as e:
            #print(f"Не удалось написать игроку {name}: {e}")
            pass
    stop_register(str(chat_id))
    await callback.answer()