#TODO: колбек кнопки "редактировать" запускает сценарий collection_edit_handlers
# Состояние бота меняется FSM: collection_editing
# Пользователь получает кнопки “Добавить новую пару” и “Активировать/деактивировать коллекцию”
# Пользователь получает сообщение с элементами (парами) коллекции, реализовано пагинацией:
# В сообщениие объект: элемент 1, кнопки инлайн клавиатуры: <<Предыдущая, удалить, повернуть, изменить, Следующая>>

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from .collection_review_router import collections_review_router
from bot_set.bot_states import BotStates
from bot_set.bot_object import cart_flipper_bot
from keyboards.collection_edit_kb import get_collection_edit_menu_kb
from bot_set.cards_paginator_class import CardsPaginator


@collections_review_router.callback_query(F.data == "collection_edit", StateFilter(BotStates.collections_review))
async def edit_collection_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    #вызывает сценарий collection_edit_handlers
    await state.set_state(BotStates.collection_editing)
    await callback_data.answer(text="Редактировать коллекцию 🟩")

    data = await state.get_data()
    cur_coll_id = data["coll_pag_inst"].current_collection_id

    spec_cards_pag_inst = CardsPaginator(telegram_id=callback_data.from_user.id,
                                         mode="specific", collection_id=cur_coll_id)

    #TODO: вернуть пагинацией список карточек из выбранной коллекции + ikb
    await cart_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=spec_cards_pag_inst.start(),
                                        reply_markup=get_collection_edit_menu_kb())
    await state.set_data({"spec_cards_pag_inst": spec_cards_pag_inst})
