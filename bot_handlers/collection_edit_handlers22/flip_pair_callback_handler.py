# Кнопка “Повернуть” изменяет сообщение и показывает пользователю “Элемент 2”.

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram import F

from bot_set.bot_states import BotStates
from .collection_edit_router import collection_edit_router
from bot_set.bot_object import card_flipper_bot
from keyboards.collection_edit_paginator_ikb import get_collection_edit_menu_ikb


@collection_edit_router.callback_query(F.data == "flipp_cart", StateFilter(BotStates.collection_editing))
async def flip_pair_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    await callback_data.answer(text="Развернруть 🔁")
    data = await state.get_data()
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=data["spec_coll_pag_inst"].show(),
                                        reply_markup=get_collection_edit_menu_ikb(data["cur_coll_id"]))
