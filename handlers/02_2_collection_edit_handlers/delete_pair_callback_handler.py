#TODO: Кнопка “Удалить” выполняет команду удаления пары из коллекции.

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_edit_router import collection_edit_router
from bot_set.bot_states import BotStates


@collection_edit_router.callback_query(F.data == "delete_pair", StateFilter(BotStates.collection_editing))
async def paar_delete_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    await callback_data.answer(text="Пара удалена 🟢")
    data = await state.get_data()
    collection_id = data["cur_coll_id"]

    #TODO: удалить пару из коллекции
    #TODO: вернуть пагинацией оставшийся список пар в коллекции
