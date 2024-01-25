# Пользователь получает сообщение: “Пришлите первый элемент пары”. Пользователь присылает. Данные записываются.

from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .pair_add_router import pair_add_router
from bot_set.bot_states import BotStates
from keyboards.cancel_kb import get_cancel_kb
from bot_set.data_formats_handlers import data_formats_handler_to_write


@pair_add_router.message(StateFilter(BotStates.get_first_elem_new_pair_adding))
async def get_first_elem(message: Message, state: FSMContext) -> None:
    formatted_data = data_formats_handler_to_write(message=message)

    await state.update_data({"first_elem_value": formatted_data["value"],
                             "first_elem_type": formatted_data["value_type"]})

    await state.set_state(BotStates.get_second_elem_new_pair_adding)
    await message.answer(text="Пришлите второй элемент карточки 📂",
                         reply_markup=get_cancel_kb())

