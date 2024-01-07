#TODO: Если пользователь просит развернуть карточку, то в сообщении изменяется объект на Элемент 2

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot_set.bot_states import BotStates
from .education_mode_router import education_mode_router


@education_mode_router.callback_query(F.data == "развернуть", StateFilter(BotStates.teaching))
async def flip_cart_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    pass
