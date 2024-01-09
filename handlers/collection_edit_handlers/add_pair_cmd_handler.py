#TODO: Кнопка “Добавить новую пару”:
# Состояние бота меняется FSM: pair_adding
# Пользователь получает кнопку “Отменить”
# запускается сценарий pair_add_handlers

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from .collection_edit_router import collection_edit_router
from bot_set.bot_states import BotStates
from keyboards.cancel_kb import get_cancel_kb


@collection_edit_router.message(F.text.lower() == "добавить новую карточку 📂",
                                StateFilter(BotStates.collection_editing))
async def add_new_paar_handler(message: Message, state: FSMContext):
    #запускает сценарий pair_add_handlers
    await state.set_state(BotStates.get_first_elem_new_pair_adding)
    await message.answer(text="Пришлите первый элемент карточки 📂",
                         reply_markup=get_cancel_kb())
