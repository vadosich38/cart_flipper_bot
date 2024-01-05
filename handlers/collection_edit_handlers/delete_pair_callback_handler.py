#TODO: Кнопка “Удалить” выполняет команду удаления пары из коллекции.

from aiogram.types import CallbackQuery
from aiogram import F

from .collection_edit_router import collection_edit_router


@collection_edit_router.callback_query(F.data == "Удалить")
async def paar_delete_callback(callback_data: CallbackQuery) -> None:
    pass
