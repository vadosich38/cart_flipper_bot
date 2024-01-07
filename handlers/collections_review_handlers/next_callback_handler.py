# TODO: С помощью кнопок “<<Предыдущая” и “Следующая>>” пользователь листает список коллекций.

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_review_router import collections_review_router
from bot_set.bot_states import BotStates


@collections_review_router.callback_query(F.data == "следующая>>", StateFilter(BotStates.collections_review))
async def next_collection_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    await callback_data.answer(text="Следующая 🟢")
    pass
