#TODO: Если пользователь нажимает “Не знаю”, пара переносится в конец списка. Сообщение изменяется на следующую пару.

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from bot_set.bot_states import BotStates
from .education_mode_router import education_mode_router


@education_mode_router.callback_query(F.data == "не знаю", StateFilter(BotStates.teaching))
async def i_dont_know_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    pass
