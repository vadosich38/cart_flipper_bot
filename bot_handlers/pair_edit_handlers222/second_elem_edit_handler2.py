#Принимается второй элмент или остается без изменений.
# Изменения записываются с указанием формата данных: изображение, текст, видео, аудио.
# Пользователь получает сообщение об успешном редактировании пары и возвращается к списку пар коллекции,
# меняет состояние бота FSM: collection_editing.
from .edit_pair_router import edit_pair_router
from bot_set.bot_states import BotStates
from bot_set.data_formats_handlers import data_formats_handler_to_edit
from bot_set.spec_coll_cards_paginator import SpecCollCardsPaginator
from bot_set.bot_object import card_flipper_bot
from keyboards.collection_edit_paginator_ikb import get_collection_edit_menu_ikb
from bot_set.data_formats_handlers import send_card_element

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery


@edit_pair_router.message(StateFilter(BotStates.pair_editing_change_second_elem))
async def get_second_elem(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    cur_card_id = data["spec_coll_pag_inst"].cur_card_id

    # пересохраняет второй элемент
    # здесь использован метод форматирования данных для записи в БД
    data_formats_handler_to_edit(message=message, card_id=cur_card_id, elem_num=2)
    await message.answer(text="Второй элемент успешно изменен! Ваша карточка обновлена! 🟩")

    await state.set_state(BotStates.collection_editing)
    # Получаем инстанс класса пагинатора коллекций, из него получаем параметр равный id текущей коллекции
    cur_coll_id = data["spec_coll_pag_inst"].collection_id

    # Обновляем инстанс пагинатора коллекции
    spec_coll_pag_inst = SpecCollCardsPaginator(collection_id=cur_coll_id)

    # возвращаем пагинацией список карточек из выбранной коллекции
    # + ikb с кнопками функциональности работы с редактированием коллекции
    cur_card = spec_coll_pag_inst.start()
    await send_card_element(user_id=message.from_user.id,
                            card_value=cur_card[0],
                            card_value_type=cur_card[1],
                            keyboard=get_collection_edit_menu_ikb())

    await state.set_data({"spec_coll_pag_inst": spec_coll_pag_inst, "cur_coll_id": cur_coll_id})
    #присылает список карточек коллекции и возвращается к сценарию collection_editing


@edit_pair_router.callback_query(F.data == "no_changes", StateFilter(BotStates.pair_editing_change_second_elem))
async def second_elem_leave_unchanged(callback_data: CallbackQuery, state: FSMContext) -> None:
    await callback_data.answer(text="Второй элемент остается без изменений! Ваша карточка обновлена! 🟩")
    await state.set_state(BotStates.collection_editing)
    data = await state.get_data()

    # присылает список карточек коллекции и возвращается к сценарию collection_editing
    # Получаем инстанс класса пагинатора коллекций, из него получаем параметр равный id текущей коллекции
    cur_coll_id = data["spec_coll_pag_inst"].collection_id

    # Обновляем инстанс пагинатора коллекции
    spec_coll_pag_inst = SpecCollCardsPaginator(collection_id=cur_coll_id)

    # возвращаем пагинацией список карточек из выбранной коллекции
    # + ikb с кнопками функциональности работы с редактированием коллекции
    cur_card = spec_coll_pag_inst.start()

    await send_card_element(user_id=callback_data.from_user.id,
                            card_value=cur_card[0],
                            card_value_type=cur_card[1],
                            keyboard=get_collection_edit_menu_ikb())
    await state.set_data({"spec_coll_pag_inst": spec_coll_pag_inst, "cur_coll_id": cur_coll_id})

