from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from DBPackage.DBclass import DBMethods


from bot_set.texts import bot_texts
from keyboards.main_menu_kb import get_main_kb
from bot_set.bot_states import BotStates

start_router = Router()


@start_router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext) -> None:
    await message.delete()
    DBMethods.add_user(telegram_id=message.from_user.id)
    await state.set_state(BotStates.main_menu)
    await message.answer(text=bot_texts["start_text"],
                         reply_markup=get_main_kb())
