# Принимается первый элмент или остается без изменений.
# Пользователь получает сообщение: “Второй элемент пары: …,
# пришлите на что его изменить или нажмите кнопку “Оставить без изменений”.

from .edit_pair_router import edit_pair_router
from bot_set.bot_states import BotStates
from bot_set.data_formats_handlers import data_formats_handler_to_edit
from DBPackage.DBclass import DBMethods
from bot_set.data_formats_handlers import send_card_element
from keyboards.pair_edit_keyboard import get_pair_edit_kb
from bot_set.bot_object import card_flipper_bot

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter


@edit_pair_router.message(F.text, StateFilter(BotStates.pair_editing_change_first_elem))
async def get_first_elem(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    cur_card_id = data["spec_coll_pag_inst"].cur_card_id

    #пересохраняет первый элемент
    #здесь использован метод форматирования данных для записи в БД
    data_formats_handler_to_edit(message=message, card_id=cur_card_id, elem_numm=1)
    await message.answer(text="Первый элемент успешно изменен! 🟩\nХотите изменить второй элемент карточки?")

    await state.set_state(BotStates.pair_editing_change_second_elem)

    cur_card = DBMethods.get_card_by_id(card_id=cur_card_id)
    send_card_element(user_id=message.from_user.id,
                      card_value=cur_card[3],
                      card_value_type=cur_card[4],
                      keyboard=get_pair_edit_kb())


@edit_pair_router.message(F.data == "no_changes", StateFilter(BotStates.pair_editing_change_first_elem))
async def first_elem_leave_unchanged(callback_data: CallbackQuery, state: FSMContext) -> None:
    await callback_data.answer(text="Первый элемент остается без изменений! 🟩")
    await state.set_state(BotStates.pair_editing_change_second_elem)
    card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                  text="Измените второй элемент карточки ⬇️")

    data = await state.get_data()
    cur_card_id = data["spec_coll_pag_inst"].cur_card_id

    cur_card = DBMethods.get_card_by_id(card_id=cur_card_id)
    send_card_element(user_id=callback_data.from_user.id,
                      card_value=cur_card[3],
                      card_value_type=cur_card[4],
                      keyboard=get_pair_edit_kb())
