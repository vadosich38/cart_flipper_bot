#TODO: После выбора режима “Коллекции” Состояние бота меняется FSM: collections,
# запускается сценарий 2_collections_review_handlers
# в пользователь получает кнопку
# “Добавить новую коллекцию” и “Вернуться в главное меню” и сообщение с списком коллекций, реализованный пагинацией
# с прикрепленной инлайн клавиатурой с кнопками: <<Предыдущая, Редактировать, Следующая>>

from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot_set.bot_states import BotStates
from keyboards.collections_paginator_ikb import get_collections_paginator_ikb
from bot_set.collections_paginator_class import CollectionsPaginator
collections_cmd_router = Router()


@collections_cmd_router.message(F.text.lower() == "коллекции 📜")
async def collections_cmd(message: Message, state: FSMContext) -> None:
    await state.set_state(BotStates.collections_review)
    coll_pag_inst = CollectionsPaginator(telegram_id=message.from_user.id)

    await message.answer(text=coll_pag_inst.start(),
                         reply_markup=get_collections_paginator_ikb())

    await state.set_data({"coll_pag_inst": coll_pag_inst})
