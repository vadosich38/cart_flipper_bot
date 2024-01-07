#TODO: Кнопка “Повернуть” изменяет сообщение и показывает пользователю “Элемент 2”.

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram import F

from bot_set.bot_states import BotStates
from .collection_edit_router import collection_edit_router


#TODO: заполнить фильтр
@collection_edit_router.callback_query(F.data == "",
                                       StateFilter(BotStates.collection_editing))
async def flip_pair_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    #TODO присылает разворот карточки
    pass
