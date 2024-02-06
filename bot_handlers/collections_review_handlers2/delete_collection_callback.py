from .collection_review_router import collections_review_router
from bot_set.bot_states import BotStates
from DBPackage.DBclass import DBMethods
from bot_set.bot_object import card_flipper_bot
from keyboards.create_first_collection_ikb import get_button_create_first_collection
from keyboards.collections_paginator_ikb import get_collections_paginator_ikb
from bot_set.collections_paginator_class import CollectionsPaginator

from aiogram.filters import StateFilter
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


@collections_review_router.callback_query(F.data == "del_collection", StateFilter(BotStates.collections_review))
async def delete_collection_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    await callback_data.answer("Коллекция и все ее карточки удалены ✅", show_alert=True)
    data = await state.get_data()
    cur_collection_id = data["coll_pag_inst"].current_collection_id

    DBMethods.delete_collection_by_id(collection_id=cur_collection_id)
    await card_flipper_bot.delete_message(chat_id=callback_data.from_user.id,
                                          message_id=callback_data.message.message_id)
    #cоздаем новый экземпляр класса пагинатора коллекций после удаления одной коллекции
    #возвращается к collection_review_handlers_2
    coll_pag_inst = CollectionsPaginator(telegram_id=callback_data.from_user.id)

    if coll_pag_inst.all_collections:
        collection_id = coll_pag_inst.current_collection_id
        await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                            text=coll_pag_inst.start(),
                                            reply_markup=get_collections_paginator_ikb(collection_id=collection_id))

        await state.set_data({"coll_pag_inst": coll_pag_inst})
    else:
        await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                            text="У вас еще нет ниодной коллекции 🙈\nСоздайте свою первую коллекцию!",
                                            reply_markup=get_button_create_first_collection())
