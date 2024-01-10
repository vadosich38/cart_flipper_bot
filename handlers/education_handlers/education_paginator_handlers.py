from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import StateFilter
from bot_set.bot_states import BotStates
from keyboards.paginator_ikb import get_cards_paginator_ikb as pag_ikb
from keyboards.back_to_main_menu import get_return_in_main_menu_kb as return_to_main_rkb
from bot_set.routers import education_cmd_router

@education_cmd_router.callback_query(F.data == 'paginator_show', StateFilter(BotStates.teaching))
async def process_paginator_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for showing the current card second value.
    Args:
        callback_data (CallbackQuery): Callback data.
        state (FSMContext): State context.
    Returns:
        None
    """
    data = await state.get_data()
    pag_inst = data['paginator_instance']
    await callback_data.answer(pag_inst.show(), reply_markup=pag_ikb(True))


@education_cmd_router.callback_query(F.data == 'paginator_not_learned', StateFilter(BotStates.teaching))
async def process_paginator_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for 'not learned' event.
    Args:
        callback_data (CallbackQuery): Callback data.
        state (FSMContext): State context.
    Returns:
        None
    """
    data = await state.get_data()
    pag_inst = data['paginator_instance']
    await callback_data.answer(pag_inst.not_learned, reply_markup=pag_ikb())


@education_cmd_router.callback_query(F.data == 'paginator_learned', StateFilter(BotStates.teaching))
async def process_paginator_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for marking the current card as learned and proceed to next.
    Args:
        callback_data (CallbackQuery): Callback data.
        state (FSMContext): State context.
    Returns:
        None
    """
    data = await state.get_data()
    pag_inst = data['paginator_instance']
    value = pag_inst.set_learned()
    if value:
        await callback_data.answer(value, reply_markup=pag_ikb())
    else:
        await state.set_data({})
        await callback_data.answer('All cards is learned', reply_markup=return_to_main_rkb())
        await state.set_state(BotStates.main_menu)


@education_cmd_router.callback_query(F.data == 'paginator_exit', StateFilter(BotStates.teaching))
async def process_paginator_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for exiting the learning mode. Clear FSM cache and changes state to main_menu.
    Args:
        callback_data (CallbackQuery): Callback data.
        state (FSMContext): State context.
    Returns:
        None
    """
    await state.set_data({})
    await state.set_state(BotStates.main_menu)
