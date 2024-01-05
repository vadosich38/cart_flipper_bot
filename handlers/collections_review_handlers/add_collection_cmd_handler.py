#TODO: Меняет состояние бота FSM: collection_adding
# вызывает сценарий collection_add_handlers
# Пользователь приглашается ввести имя коллекции и получает кнопку “Отменить”.

from aiogram import F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot_set.bot_states import BotStates
from .collection_review_router import collections_review_router


@collections_review_router.message(F.text.lower() == "Добавить новую коллекцию",
                                   StateFilter(BotStates.collections_review))
async def add_new_collection_cmd(message: Message, state: FSMContext) -> None:
    await state.set_state(BotStates.collection_adding)
    pass
