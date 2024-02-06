# После выбора режима “Коллекции” Состояние бота меняется FSM: collections,
# запускается сценарий collections_review_handlers2
# в пользователь получает кнопку
# “Добавить новую коллекцию” и “Вернуться в главное меню” и сообщение с списком коллекций, реализованный пагинацией
# с прикрепленной инлайн клавиатурой с кнопками: <<Предыдущая, Редактировать, Следующая>>

from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from bot_set.bot_states import BotStates
from keyboards.collections_paginator_ikb import get_collections_paginator_ikb
from bot_set.collections_paginator_class import CollectionsPaginator
from keyboards.create_first_collection_ikb import get_button_create_first_collection


collections_cmd_router = Router()


@collections_cmd_router.message(F.text.lower() == "коллекции 📜", StateFilter(BotStates.main_menu))
async def collections_cmd(message: Message, state: FSMContext) -> None:
    await state.set_state(BotStates.collections_review)
    coll_pag_inst = CollectionsPaginator(telegram_id=message.from_user.id)

    if coll_pag_inst.all_collections:
        collection_id = coll_pag_inst.current_collection_id
        await message.answer(text=coll_pag_inst.start(),
                             reply_markup=get_collections_paginator_ikb(collection_id=collection_id))

        await state.set_data({"coll_pag_inst": coll_pag_inst})
    else:
        await message.answer(text="У вас еще нет ниодной коллекции 🙈\nСоздайте свою первую коллекцию!",
                             reply_markup=get_button_create_first_collection())
