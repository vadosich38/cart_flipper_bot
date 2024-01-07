#TODO:
# Если пользователь во время обучения вводит команду “закончить”/cancel, словарь удаляется,
# а пользователь получает соответствующее сообщение и выход в главное меню
# состояние бота очищается

from aiogram.types import Message
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .education_mode_router import education_mode_router
from bot_set.texts import bot_texts
from bot_set.bot_states import BotStates


@education_mode_router.message(F.text == bot_texts["stop_education_cmd"], StateFilter(BotStates.teaching))
async def cancel_education_mode(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.delete()
    await message.answer(text=bot_texts["return_in_main_menu"])
