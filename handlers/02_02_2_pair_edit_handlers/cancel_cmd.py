#TODO: команда "Отменить" отменяет редактирование, меняет состояние бота на FSM: collection_editing
# и возвращает пользователя к списку пар коллекции.

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram import F

from bot_set.bot_states import BotStates
from .edit_pair_router import edit_pair_router


@edit_pair_router.message(F.text.lower == "отменить 🔴", StateFilter(BotStates.pair_editing_change_first_elem,
                                                                    BotStates.pair_editing_change_second_elem))
async def cancel_pair_editing(message: Message, state: FSMContext) -> None:
    await state.set_state(BotStates.collection_editing)
    #TODO: возвращается к сценарию collection_editing
