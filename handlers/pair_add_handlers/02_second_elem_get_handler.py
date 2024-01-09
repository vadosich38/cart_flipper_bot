#TODO: Пользователь получает сообщение: “Пришлите второй элемент пары”. Пользователь присылает. Данные записываются.
from .pair_add_router import pair_add_router
from bot_set.bot_states import BotStates
from keyboards.yes_no_ikb import get_yes_no_ikb
from keyboards.cancel_kb import get_cancel_kb

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message


@pair_add_router.message(StateFilter(BotStates.get_second_elem_new_pair_adding))
async def get_second_elem(message: Message, state: FSMContext) -> None:
    #TODO: смохранить второй элемент карточки из объекта сообщения
    await state.set_state(BotStates.set_mirror_mode_new_pair_adding)
    await message.answer(text="Эта карточка имеет зеркальное значение? 👁‍🗨",
                         reply_markup=get_yes_no_ikb())
    # вызов кнопки отмены повторно может не понадобится, так как первая клавиатура должна сохранят кнопку отмены!
    # await message.answer(text="Зеркальное значение значит, что при обучении карточка будет демонстрироваться с обоих "
    #                           "сторон поочередно ➿\n\nНапример, задание 1: передите Apple на русский, а задание 2: "
    #                           "переведите яблоко на английский 🧑‍🏫",
    #                      reply_markup=get_cancel_kb())
