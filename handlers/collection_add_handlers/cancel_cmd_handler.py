#TODO: Кнопка “Отменить” отменяет добавление новой коллекции или пары в нее, если коллекция уже создана.
# Состояние бота меняется FSM: collection и возвращает к списку коллекций, запуская сценаарий collections_review_handlers

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates
from bot_set.texts import bot_texts


@collection_add_router.message(F.text.lower() == "отменить 🔴",
                               StateFilter(BotStates.collection_adding_get_name))
async def collection_add_cmd_handler(message: Message, state: FSMContext):
    await state.set_state(BotStates.collections_review)
    await message.answer(text="Вы отменили добавление новой коллекции 🟥")
    #TODO: вернуть пагинацией список коллеккций (дублируется механика хендлера main_modes -- collection_cmd

