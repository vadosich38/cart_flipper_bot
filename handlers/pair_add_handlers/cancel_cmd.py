#TODO: Если пользователь отменяет добавление пары, состояние бота меняется
# FSM: collection_editing и возвращается к списку пар в коллекции.

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram import F

from bot_set.bot_states import BotStates
from .pair_add_router import pair_add_router


@pair_add_router.message(F.text.lower == "отменить 🔴", StateFilter(BotStates.get_first_elem_new_pair_adding,
                                                                   BotStates.get_second_elem_new_pair_adding,
                                                                   BotStates.set_mirror_mode_new_pair_adding))
async def cancel_pair_adding(message: Message, state: FSMContext) -> None:
    await state.set_state(BotStates.collection_editing)
    #TODO: возвращается к сценарию collection_editing
