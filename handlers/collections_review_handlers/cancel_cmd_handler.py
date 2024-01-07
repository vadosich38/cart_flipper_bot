#TODO: вызоваа команды /cancel (Вернуться в главное меню) вовзращает пользователя в главное меню бота
# состояние бота очищается

from aiogram import F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_review_router import collections_review_router
from bot_set.bot_states import BotStates
from bot_set.texts import bot_texts
from keyboards.main_menu_kb import get_main_kb


@collections_review_router.message(F.text.lower() == "вернуться в главное меню 🟥",
                                   StateFilter(BotStates.collections_review))
async def collections_menu_cancel(message: Message, state: FSMContext) -> None:
    await message.answer(text=bot_texts["return_in_main_menu"],
                         reply_markup=get_main_kb())
    await state.clear()
