#TODO: да - активировать коллекцию, нет - не активировать коллекцию
# Пользователь получает сообщение: Коллекция активна/не активна. Хотите ее наполнить?

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates


@collection_add_router.callback_query(F.data == "activate", StateFilter(BotStates.collection_adding))
async def collection_activate_callback(callback_data: CallbackQuery, state: FSMContext):
    pass


@collection_add_router.callback_query(F.data == "deactivate", StateFilter(BotStates.collection_adding))
async def collection_deactivate_callback(callback_data: CallbackQuery, state: FSMContext):
    pass
