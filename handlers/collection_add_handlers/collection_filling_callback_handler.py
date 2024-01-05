#TODO: Да –– меняет состояние бота  FSM: paar_adding и вызывает сценарий pair_add_handlers
# Нет –– меняет состояние бота FSM: collection и возвращает к списку коллекций.

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates


@collection_add_router.callback_query(F.data == "filling", StateFilter(BotStates.collection_adding))
async def collection_filling_callback(callback_data: CallbackQuery, state: FSMContext):
    pass


@collection_add_router.callback_query(F.data == "not_filling", StateFilter(BotStates.collection_adding))
async def collection_not_filling_callback(callback_data: CallbackQuery, state: FSMContext):
    pass
