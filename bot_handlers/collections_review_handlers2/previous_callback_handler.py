# С помощью кнопок “<<Предыдущая” и “Следующая>>” пользователь листает список коллекций.

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_review_router import collections_review_router
from bot_set.bot_states import BotStates
from bot_set.bot_object import card_flipper_bot
from keyboards.collections_paginator_ikb import get_collections_paginator_ikb


@collections_review_router.callback_query(F.data == "previous", StateFilter(BotStates.collections_review))
async def previous_collection_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    await callback_data.answer(text="Предыдущая 🟢")

    data = await state.get_data()
    coll_pag_inst = data["coll_pag_inst"]

    await card_flipper_bot.edit_message_text(text=coll_pag_inst.previous(),
                                             chat_id=callback_data.from_user.id,
                                             message_id=callback_data.message.message_id,
                                             reply_markup=get_collections_paginator_ikb())
