from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import StateFilter
from aiogram import Router

from bot_set.bot_states import BotStates
from keyboards.cards_paginator_ikb import get_cards_paginator_ikb as cards_pag_ikb
from bot_set.cards_paginator_class import CardsPaginator
from bot_set.data_formats_handlers import send_card_element
from keyboards.main_menu_kb import get_main_kb
from loader import logger
education_cmd_router = Router()


@education_cmd_router.message(F.text.lower() == "учиться 🧑‍🏫", StateFilter(BotStates.main_menu))
async def education_cmd(message: Message, state: FSMContext) -> None:
    """
    Handler for the "Learn" command.
    Args:
        message (Message): Incoming message.
        state (FSMContext): State context.
    Returns:
        None
    """
    await state.set_state(BotStates.teaching)
    logger.debug('Creating paginator instance')
    cards_pag_inst = CardsPaginator(telegram_id=message.from_user.id)

    if cards_pag_inst.card_values:
        card_value = cards_pag_inst.start()
        send_card_element(user_id=message.from_user.id,
                          card_value=card_value[0],
                          card_value_type=card_value[1],
                          keyboard=cards_pag_ikb())
        await state.set_data({'paginator_instance': cards_pag_inst})
    else:
        await state.clear()
        await state.set_state(BotStates.main_menu)
        await message.answer(text='У вас нет коллекция для изучения 🧑‍🏫\n\nАктивируйте коллекции или создайте новую ✅',
                             reply_markup=get_main_kb())
