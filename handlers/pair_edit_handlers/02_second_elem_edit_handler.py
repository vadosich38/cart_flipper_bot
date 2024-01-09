#TODO: Принимается второй элмент или остается без изменений.
# Изменения записываются с указанием формата данных: изображение, текст, видео, аудио.
# Пользователь получает сообщение об успешном редактировании пары и возвращается к списку пар коллекции,
# меняет состояние бота FSM: collection_editing.
from .edit_pair_router import edit_pair_router
from bot_set.bot_states import BotStates

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message


@edit_pair_router.message(StateFilter(BotStates.pair_editing_change_second_elem))
async def get_second_elem(message: Message, state: FSMContext) -> None:
    #TODO: пересохраняет второй элемент
    await message.answer(text="Второй элемент успешно изменен! Ваша карточка обновлена! 🟩")
    await state.set_state(BotStates.collection_editing)
    #TODO: присылает список карточек коллекции и возвращается к сценарию collection_editing
    pass


@edit_pair_router.message(F.text.lower("оставить без изменений"), StateFilter(BotStates.pair_editing_change_second_elem))
async def first_elem_leave_unchanged(message: Message, state: FSMContext) -> None:
    await message.answer(text="Второй элемент остается без изменений! Ваша карточка обновлена! 🟩")
    await state.set_state(BotStates.collection_editing)
    #TODO: присылает список карточек коллекции и возвращается к сценарию collection_editing
    pass

