# вызоваа команды /cancel (Вернуться в главное меню) вовзращает пользователя в главное меню бота
# состояние бота очищается

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_review_router import collections_review_router
from bot_set.bot_states import BotStates
from bot_set.texts import bot_texts
from keyboards.main_menu_kb import get_main_kb
from bot_set.bot_object import card_flipper_bot


@collections_review_router.callback_query(F.data == "collections_paginator_menu",
                                          StateFilter(BotStates.collections_review))
async def collections_menu_cancel(callback_data: CallbackQuery, state: FSMContext) -> None:
    await callback_data.answer(text="Вернуться в главное меню 🟩")
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=bot_texts["return_in_main_menu"],
                                        reply_markup=get_main_kb())
    await state.clear()
