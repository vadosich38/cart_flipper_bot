#TODO: Меняет состояние бота FSM: collection_adding
# вызывает сценарий 02_1_collection_add_handlers
# Пользователь приглашается ввести имя коллекции и получает кнопку “Отменить”.

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot_set.bot_states import BotStates
from bot_set.texts import bot_texts
from .collection_review_router import collections_review_router
from keyboards.cancel_kb import get_cancel_kb
from bot_set.bot_object import cart_flipper_bot


@collections_review_router.callback_query(F.data == "add_new_collection",
                                          StateFilter(BotStates.collections_review))
async def add_new_collection_cmd(callback_data: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BotStates.collection_adding_get_name)
    await callback_data.answer(text="Добавить новую коллекцию 🟩")
    await cart_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=bot_texts["send_new_collection_name"],
                                        reply_markup=get_cancel_kb())
