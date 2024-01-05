#TODO: Кнопка “Добавить новую пару”:
# Состояние бота меняется FSM: paar_adding
# Пользователь получает кнопку “Отменить”
# запускается сценарий pair_add_handlers

from aiogram import F
from aiogram.types import Message

from .collection_edit_router import collection_edit_router


@collection_edit_router.message(F.text.lower() == "добавить новую пару")
async def add_new_paar_handler(message: Message):
    pass
