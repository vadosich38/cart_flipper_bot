# колбек кнопки "редактировать" запускает сценарий collection_edit_handlers22
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
from bot_set.bot_object import card_flipper_bot
from keyboards.collection_edit_paginator_ikb import get_collection_edit_menu_ikb
from bot_set.spec_coll_cards_paginator import SpecCollCardsPaginator
from bot_set.data_formats_handlers import send_card_element


@collections_review_router.callback_query(F.data == "collection_edit", StateFilter(BotStates.collections_review))
async def edit_collection_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    #вызывает сценарий collection_edit_handlers22
    await state.set_state(BotStates.collection_editing)
    await callback_data.answer(text="Редактировать коллекцию 🟩")
    data = await state.get_data()
    # Получаем инстанс класса пагинатора коллекций, из него получаем параметр равный id текущей коллекции
    cur_coll_id = data["coll_pag_inst"].current_collection_id
    # Записываем айди коллекции в память
    await state.update_data({"new_coll_id": cur_coll_id})


    spec_coll_pag_inst = SpecCollCardsPaginator(collection_id=cur_coll_id)
    await card_flipper_bot.delete_message(chat_id=callback_data.from_user.id,
                                          message_id=callback_data.message.message_id)

    if spec_coll_pag_inst.card_values:
        #возвращаем пагинацией список карточек из выбранной коллекции
        # + ikb с кнопками функциональности работы с редактированием коллекции
        cur_card = spec_coll_pag_inst.start()

        await send_card_element(user_id=callback_data.from_user.id,
                                card_value=cur_card[0],
                                card_value_type=cur_card[1],
                                keyboard=get_collection_edit_menu_ikb())

    else:
        await card_flipper_bot.send_message(chat_id=callback_data.from_user.id,
                                            text="В этой коллекции еще нет карточек! 🫣\nВы можете добавить их сейчас ➕",
                                            reply_markup=get_collection_edit_menu_ikb(collection_is_empy=True))
    await state.set_data({"spec_coll_pag_inst": spec_coll_pag_inst, "cur_coll_id": cur_coll_id})

