from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot_set.texts import bot_texts
from keyboards.main_menu_kb import get_main_kb

start_router = Router()


@start_router.message(CommandStart)
async def start_cmd(message: Message) -> None:
    await message.delete()
    await message.answer(text=bot_texts["start_text"],
                         reply_markup=get_main_kb())
