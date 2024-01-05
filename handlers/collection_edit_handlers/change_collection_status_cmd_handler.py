#TODO: Кнопка “Активировать/деактивировать коллекцию” изменяет статус активности выбранной коллекции.

from aiogram import F
from aiogram.types import Message

from .collection_edit_router import collection_edit_router


@collection_edit_router.message(F.text.lower() == "активировать")
async def collection_activate_handler(message: Message):
    pass


@collection_edit_router.message(F.text.lower() == "деактивировать")
async def collection_deactivate_handler(message: Message):
    pass
