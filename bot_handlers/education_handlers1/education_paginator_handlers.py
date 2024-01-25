from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import StateFilter

from bot_set.bot_states import BotStates
from keyboards.cards_paginator_ikb import get_cards_paginator_ikb as pag_ikb
from keyboards.back_to_main_menu import get_return_in_main_menu_kb as return_to_main_rkb
from bot_set.routers import education_cmd_router
from bot_set.data_formats_handlers import send_card_element


@education_cmd_router.callback_query(F.data == 'paginator_show', StateFilter(BotStates.teaching))
async def paginator_card_show(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for showing the current card second value.
    Args:
        callback_data (CallbackQuery): Callback data.
        state (FSMContext): State context.
    Returns:
        None
    """
    data = await state.get_data()
    cards_pag_inst = data['paginator_instance']
    card_value = cards_pag_inst.show()

    send_card_element(user_id=callback_data.from_user.id,
                      card_value=card_value[0],
                      card_value_type=card_value[1],
                      keyboard=pag_ikb())


@education_cmd_router.callback_query(F.data == 'paginator_not_learned', StateFilter(BotStates.teaching))
async def paginator_card_not_learned(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for 'not learned' event.
    Args:
        callback_data (CallbackQuery): Callback data.
        state (FSMContext): State context.
    Returns:
        None
    """
    data = await state.get_data()
    cards_pag_inst = data['paginator_instance']
    card_value = cards_pag_inst.not_learned

    send_card_element(user_id=callback_data.from_user.id,
                      card_value=card_value[0],
                      card_value_type=card_value[1],
                      keyboard=pag_ikb())


@education_cmd_router.callback_query(F.data == 'paginator_learned', StateFilter(BotStates.teaching))
async def paginator_card_learned(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for marking the current card as learned and proceed to next.
    Args:
        callback_data (CallbackQuery): Callback data.
        state (FSMContext): State context.
    Returns:
        None
    """
    data = await state.get_data()
    cards_pag_inst = data['paginator_instance']
    card_value = cards_pag_inst.set_learned()

    if card_value:
        send_card_element(user_id=callback_data.from_user.id,
                          card_value=card_value[0],
                          card_value_type=card_value[1],
                          keyboard=pag_ikb())
    else:
        await state.clear()
        await callback_data.answer('Все карточки изучены! Вы молодец 🏆', reply_markup=return_to_main_rkb())
        await state.set_state(BotStates.main_menu)


#TODO: здесь правльно указана callback data в фильтре?
@education_cmd_router.callback_query(F.data == 'paginator_menu', StateFilter(BotStates.teaching))
async def learning_exit(callback_data: CallbackQuery, state: FSMContext) -> None:
    """
    Callback handler for exiting the learning mode. Clear FSM cache and changes state to main_menu.
    Args:
        callback_data (CallbackQuery): Callback data.
        state (FSMContext): State context.
    Returns:
        None
    """
    await callback_data.answer(text="Закончить обучение 🟢")
    await state.clear()
    await state.set_state(BotStates.main_menu)
