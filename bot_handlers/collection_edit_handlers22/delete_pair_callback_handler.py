# Кнопка “Удалить” выполняет команду удаления пары из коллекции.

from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .collection_edit_router import collection_edit_router
from bot_set.bot_states import BotStates
from DBPackage.DBclass import DBMethods
from bot_set.bot_object import card_flipper_bot
from bot_set.spec_coll_cards_paginator import SpecCollCardsPaginator
from keyboards.collection_edit_paginator_ikb import get_collection_edit_menu_ikb
from bot_set.data_formats_handlers import send_card_element
from bot_set.bot_object import card_flipper_bot


@collection_edit_router.callback_query(F.data == "delete_pair", StateFilter(BotStates.collection_editing))
async def pair_delete_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    # Удаляет карточку из коллекции
    data = await state.get_data()
    DBMethods.delete_card_by_id(card_id=data["spec_coll_pag_inst"].cur_card_id)
    await callback_data.answer(text="Пара удалена 🟢")

    # Создает новый экзмепляр класса пагинации карточек указанной коллекции
    spec_coll_pag_inst = SpecCollCardsPaginator(collection_id=data["cur_coll_id"])

    # Удаляем старое сообщение
    await card_flipper_bot.delete_message(chat_id=callback_data.from_user.id,
                                          message_id=callback_data.message.message_id)

    if spec_coll_pag_inst.card_values:
        cur_card = spec_coll_pag_inst.start()
        # Возвращает новый список карточек колекции пагинацией
        await send_card_element(user_id=callback_data.from_user.id,
                                card_value=cur_card[0],
                                card_value_type=cur_card[1],
                                keyboard=get_collection_edit_menu_ikb())
        # Обновляет в памяти экземпляр класса
        await state.update_data({"spec_coll_pag_inst": spec_coll_pag_inst})
    else:
        await state.clear()
        await state.set_data({"cur_coll_id": data["cur_coll_id"]})
        await state.set_state(BotStates.collection_editing)
        await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                            text="Вы опустошили коллекцию! 🫣\nВы можете добавить новые карточки ➕",
                                            reply_markup=get_collection_edit_menu_ikb(collection_is_empy=True))
