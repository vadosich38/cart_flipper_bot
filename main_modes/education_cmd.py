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
from DBPackage.DBclass import DBMethods
from datetime import datetime

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
    #проверяем является ли нынешнее время позже, чем то, до которого должна длиться пауза.
    next_lesson_at = DBMethods.get_next_lesson(telegram_id=message.from_user.id)
    if next_lesson_at < datetime.now():
        await state.set_state(BotStates.teaching)
        logger.debug('Creating paginator instance')
        active_collection_card_list = DBMethods.get_active_collections_cards(telegram_id=message.from_user.id)
        if active_collection_card_list:
            cards_pag_inst = CardsPaginator(active_collection_card_list)
            card_value = cards_pag_inst.start()
            await send_card_element(user_id=message.from_user.id,
                                    card_value=card_value[0],
                                    card_value_type=card_value[1],
                                    keyboard=cards_pag_ikb())
            await state.set_data({'paginator_instance': cards_pag_inst})
        else:
            await state.clear()
            await state.set_state(BotStates.main_menu)
            await message.answer(text='У вас нет активных коллекциий 🧑‍🏫\n\nАктивируйте коллекции✅',
                                 reply_markup=get_main_kb())
    else:
        await message.answer(text="Вам еще рано повторять урок ❌\n\n"
                                  "После каждого урока нужно отдыхать не меньше 20 минут."
                                  "В противном случае система запоминания не будет работать эффективно 🫣\n\n",
                             reply_markup=get_main_kb())
