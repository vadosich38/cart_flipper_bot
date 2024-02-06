# Пользователь получает сообщение "Ваша пара имеет обратное значение?":
# да – добавляется 2 пары (зеркальные), нет - одна.
# Пользователь получает уведомление об успешном добавлении пары.
# состояние бота меняется на FSM: collection_edit_handlers22
# пользователь возвращается в меню редактирвоания коллекции и запускается сценарий collection_edit_handlers22

from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from .pair_add_router import pair_add_router
from bot_set.bot_states import BotStates
from bot_set.bot_object import card_flipper_bot
from DBPackage.DBclass import DBMethods
from bot_set.collections_paginator_class import CollectionsPaginator
from keyboards.collections_paginator_ikb import get_collections_paginator_ikb
import asyncio


@pair_add_router.callback_query(F.data == "yes", StateFilter(BotStates.set_mirror_mode_new_pair_adding))
async def set_mirror_mode(callback_data: CallbackQuery, state: FSMContext) -> None:
    #производится запись карточки два раза зеркально (элемент1 == элемент2 и элемент2 == элемент1)
    await callback_data.answer(text="Добавить карточку зеркально 🟢")
    #удаляем старое сообщение
    await card_flipper_bot.delete_message(chat_id=callback_data.from_user.id,
                                          message_id=callback_data.message.message_id)
    data = await state.get_data()
    print(f"first_elem_value: {data["first_elem_value"]}, first_elem_type: {data["first_elem_type"]},"
          f"second_elem_value: {data["second_elem_value"]}, second_elem_type: {data["second_elem_type"]}")
    # First card adding
    DBMethods.add_card_by_collection_id(collection_id=data["cur_coll_id"],
                                        card_value_1=data["first_elem_value"], value1_type=data["first_elem_type"],
                                        card_value_2=data["second_elem_value"], value2_type=data["second_elem_type"])
    # Second card adding
    DBMethods.add_card_by_collection_id(collection_id=data["cur_coll_id"],
                                        card_value_1=data["second_elem_value"], value1_type=data["second_elem_type"],
                                        card_value_2=data["first_elem_value"], value2_type=data["first_elem_type"])
    await callback_data.answer(text="Карточка добавлена зеркально! 🟩", show_alert=True)
    await state.set_state(BotStates.collections_review)

    coll_pag_inst = CollectionsPaginator(telegram_id=callback_data.from_user.id)
    collection_id = coll_pag_inst.current_collection_id

    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=coll_pag_inst.start(),
                                        reply_markup=get_collections_paginator_ikb(collection_id=collection_id))

    await state.set_data({"coll_pag_inst": coll_pag_inst})
    #возврат к сценарию collections_review


@pair_add_router.callback_query(F.data == "no", StateFilter(BotStates.set_mirror_mode_new_pair_adding))
async def set_no_mirror_mode(callback_data: CallbackQuery, state: FSMContext) -> None:
    #производится запись карточки один раз (элемент1 == элемент2)
    await callback_data.answer(text="Добавить карточку 🟢")
    #удаляем старое сообщение
    await card_flipper_bot.delete_message(chat_id=callback_data.from_user.id,
                                          message_id=callback_data.message.message_id)

    data = await state.get_data()

    # Card adding
    DBMethods.add_card_by_collection_id(collection_id=data["cur_coll_id"],
                                        card_value_1=data["first_elem_value"], value1_type=data["first_elem_type"],
                                        card_value_2=data["second_elem_value"], value2_type=data["second_elem_type"])

    await callback_data.answer(text="Карточка добавлена! 🟩", show_alert=True)
    await state.set_state(BotStates.collections_review)

    coll_pag_inst = CollectionsPaginator(telegram_id=callback_data.from_user.id)
    collection_id = coll_pag_inst.current_collection_id

    await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                        text=coll_pag_inst.start(),
                                        reply_markup=get_collections_paginator_ikb(collection_id=collection_id))

    await state.set_data({"coll_pag_inst": coll_pag_inst})
    # возврат к сценарию collections_review
