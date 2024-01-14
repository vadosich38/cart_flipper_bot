#TODO: С помощью кнопок “<<Предыдущая” и “Следующая>>” пользователь листает список пар в коллекции.

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram import F

from bot_set.bot_states import BotStates
from .collection_edit_router import collection_edit_router


#TODO: заполнить фильтр
@collection_edit_router.callback_query(F.data == "",
                                       StateFilter(BotStates.collection_editing))
async def previous_pair_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    #TODO: присылает предыдущую карточку
    pass
