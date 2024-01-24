# Принимается первый элмент или остается без изменений.
# Пользователь получает сообщение: “Второй элемент пары: …,
# пришлите на что его изменить или нажмите кнопку “Оставить без изменений”.

from .edit_pair_router import edit_pair_router
from bot_set.bot_states import BotStates

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter


@edit_pair_router.message(F.text, StateFilter(BotStates.pair_editing_change_first_elem))
async def get_first_elem(message: Message, state: FSMContext) -> None:
    #TODO: пересохраняет первый элемент
    await message.answer(text="Первый элемент успешно изменен! 🟩")
    await state.set_state(BotStates.pair_editing_change_second_elem)
    #TODO: присылает второй элемент и предлагает его изменить
    pass


@edit_pair_router.message(F.data == "оставить без изменений", StateFilter(BotStates.pair_editing_change_first_elem))
async def first_elem_leave_unchanged(message: Message, state: FSMContext) -> None:
    await message.answer(text="Первый элемент остается без изменений! 🟩")
    await state.set_state(BotStates.pair_editing_change_second_elem)
    #TODO: присылает второй элемент и предлагает его изменить прикрепленной клавитаруой с кнопкой 'оставить без изменений'
    pass
