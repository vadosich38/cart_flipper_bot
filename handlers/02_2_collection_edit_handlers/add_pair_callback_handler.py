#TODO: Кнопка “Добавить новую пару”:
# Состояние бота меняется FSM: pair_adding
# Пользователь получает кнопку “Отменить”
# запускается сценарий 02_02_01_pair_add_handlers

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from .collection_edit_router import collection_edit_router
from bot_set.bot_states import BotStates
from keyboards.cancel_kb import get_cancel_kb
from bot_set.bot_object import cart_flipper_bot


@collection_edit_router.callback_query(F.data == "add_new_card",
                                       StateFilter(BotStates.collection_editing))
async def add_new_paar_callback(callback_data: CallbackQuery, state: FSMContext):
    #запускает сценарий 02_02_01_pair_add_handlers
    await state.set_state(BotStates.get_first_elem_new_pair_adding)
    await callback_data.answer(text="Добавляем новую карточку 🟢")
    await cart_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text="Пришлите первый элемент карточки 📂",
                                        reply_markup=get_cancel_kb())
