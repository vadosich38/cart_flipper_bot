# Кнопка “Отменить” отменяет добавление новой коллекции или пары в нее, если коллекция уже создана.
# Состояние бота меняется FSM: collection и возвращает к списку коллекций, запуская сценаарий collections_review_handlers2

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import asyncio

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates
from bot_set.collections_paginator_class import CollectionsPaginator
from keyboards.collections_paginator_ikb import get_collections_paginator_ikb


@collection_add_router.message(F.text.lower() == "отменить 🔴",
                               StateFilter(BotStates.collection_adding_get_name))
async def collection_add_cmd_handler(message: Message, state: FSMContext):
    await state.set_state(BotStates.collections_review)
    await message.answer(text="Вы отменили добавление новой коллекции 🟥")

    coll_pag_inst = CollectionsPaginator(telegram_id=message.from_user.id)
    await asyncio.sleep(2)
    await message.edit_text(text=coll_pag_inst.start(),
                            reply_markup=get_collections_paginator_ikb())

    await state.set_data({"coll_pag_inst": coll_pag_inst})
