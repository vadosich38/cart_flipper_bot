#TODO: хендлер принимает имя коллекции и записывает его
# Пользователь получает сообщение: Имя вашей коллекции…, хотите активировать ее?

from aiogram import F
from aiogram.types import Message

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates


@collection_add_router.message(F.text, len(F.text) < 25)
async def get_collection_name_handler(message: Message):
    pass


@collection_add_router.message(F.text, len(F.text) > 25)
async def get_collection_name_error_handler(message: Message):
    pass
