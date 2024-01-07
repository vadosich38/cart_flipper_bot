#TODO: Кнопка “Удалить” выполняет команду удаления пары из коллекции.

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.filters import StateFilter

from .collection_edit_router import collection_edit_router
from bot_set.bot_states import BotStates


@collection_edit_router.callback_query(F.data == "Удалить", StateFilter(BotStates.collection_editing))
async def paar_delete_callback(callback_data: CallbackQuery) -> None:
    await callback_data.answer(text="Пара удалена 🟢")
    #TODO: вернуть пагинацией оставшийся список пар в коллекции
