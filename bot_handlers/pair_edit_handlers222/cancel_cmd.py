# команда "Отменить" отменяет редактирование, меняет состояние бота на FSM: collection_editing
# и возвращает пользователя к списку пар коллекции.

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram import F

from bot_set.bot_states import BotStates
from .edit_pair_router import edit_pair_router
from bot_set.spec_coll_cards_paginator import SpecCollCardsPaginator
from bot_set.bot_object import card_flipper_bot
from keyboards.collection_edit_paginator_ikb import get_collection_edit_menu_ikb


@edit_pair_router.callback_query(F.data == "cancel", StateFilter(BotStates.pair_editing_change_first_elem,
                                                                 BotStates.pair_editing_change_second_elem))
async def cancel_pair_editing(callback_data: CallbackQuery, state: FSMContext) -> None:
    # присылает список карточек коллекции и возвращается к сценарию collection_editing
    await state.set_state(BotStates.collection_editing)
    data = await state.get_data()

    # Получаем инстанс класса пагинатора коллекций, из него получаем параметр равный id текущей коллекции
    cur_coll_id = data["spec_coll_pag_inst"].collection_id

    # Обновляем инстанс пагинатора коллекции
    spec_coll_pag_inst = SpecCollCardsPaginator(collection_id=cur_coll_id)

    # возвращаем пагинацией список карточек из выбранной коллекции
    # + ikb с кнопками функциональности работы с редактированием коллекции
    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=spec_coll_pag_inst.start(),
                                        reply_markup=get_collection_edit_menu_ikb(collection_id=cur_coll_id))
    await state.set_data({"spec_coll_pag_inst": spec_coll_pag_inst, "cur_coll_id": cur_coll_id})


