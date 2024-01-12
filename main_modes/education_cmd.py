from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot_set.bot_states import BotStates
from keyboards.cards_paginator_ikb import get_cards_paginator_ikb as cards_pag_ikb
from keyboards.back_to_main_menu import get_return_in_main_menu_kb as return_to_main_rkb
from bot_set.routers import education_cmd_router
from bot_set.cards_paginator_class import CardsPaginator


@education_cmd_router.message(F.text.lower() == "учиться 🧑‍🏫")
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
    cards_pag_inst = CardsPaginator(telegram_id=message.from_user.id)
    value = cards_pag_inst.start()
    if value:
        await message.answer(value, reply_markup=cards_pag_ikb())
        await state.set_data({'paginator_instance': cards_pag_inst})
    else:
        await state.clear()
        await message.answer('Empty Collection', reply_markup=return_to_main_rkb())
        await state.set_state(BotStates.main_menu)

