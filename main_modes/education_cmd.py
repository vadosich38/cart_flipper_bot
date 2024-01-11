from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import StateFilter
from bot_set.bot_states import BotStates
from keyboards.paginator_ikb import get_cards_paginator_ikb as pag_ikb
from keyboards.back_to_main_menu import get_return_in_main_menu_kb as return_to_main_rkb
from bot_set.routers import education_cmd_router
from bot_set.paginator_class import Paginator


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
    pag_inst = Paginator(message.from_user.id)
    value = pag_inst.start()
    if value:
        await message.answer(value, reply_markup=pag_ikb())
        await state.set_data({'paginator_instance': pag_inst})
    else:
        await state.set_data({})
        await message.answer('Empty Collection', reply_markup=return_to_main_rkb())
        await state.set_state(BotStates.main_menu)

