# Кнопка “Отменить” отменяет добавление новой коллекции или пары в нее, если коллекция уже создана.
# Состояние бота меняется FSM: collection и возвращает к списку коллекций, запуская сценаарий collections_review_handlers2

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import asyncio

from .collection_add_router import collection_add_router
from bot_set.bot_states import BotStates
from bot_set.collections_paginator_class import CollectionsPaginator
from keyboards.collections_paginator_ikb import get_collections_paginator_ikb
from bot_set.bot_object import card_flipper_bot
from keyboards.create_first_collection_ikb import get_button_create_first_collection


@collection_add_router.message(F.text.lower() == "отменить 🔴",
                               StateFilter(BotStates.collection_adding_get_name))
async def collection_add_cmd_handler(message: Message, state: FSMContext):
    await state.set_state(BotStates.collections_review)
    await message.answer(text="Вы отменили добавление новой коллекции 🟥"
                              "\nВы будете возвращены к просмотру ваших коллекций")

    #Получаем новый экземпляр класса пагинации коллекций
    coll_pag_inst = CollectionsPaginator(telegram_id=message.from_user.id)

    await asyncio.sleep(1)
    #Удаляем два прошлых сообщения
    await card_flipper_bot.delete_messages(chat_id=message.from_user.id,
                                           message_ids=[message.message_id-1, message.message_id])


    if coll_pag_inst.all_collections:
        collection_id = coll_pag_inst.current_collection_id
        await message.answer(text=coll_pag_inst.start(),
                             reply_markup=get_collections_paginator_ikb(collection_id=collection_id))

        await state.set_data({"coll_pag_inst": coll_pag_inst})
    else:
        await message.answer(text="У вас еще нет ниодной коллекции 🙈\nСоздайте свою первую коллекцию!",
                             reply_markup=get_button_create_first_collection())
