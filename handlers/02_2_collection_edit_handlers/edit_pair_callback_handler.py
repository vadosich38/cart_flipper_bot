#TODO: Кнопка “Изменить” позволяет изменить выбранную пару
# вызывает сценарий 02_02_2_pair_edit_handlers
# Состояние бота меняется FSM: pair_editing
# Пользователь получает кнопку “Отменить изменения”, которая отменяет редактирование,
# меняет состояние бота FSM: collection_editing и возвращает пользователя к списку пар коллекции.
# Пользователь получает сообщение: “Первый элемент пары: …, пришлите на что его изменить
# или нажмите кнопку “Оставить без изменений”.

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram import F

from bot_set.bot_states import BotStates
from .collection_edit_router import collection_edit_router
from bot_set.bot_object import cart_flipper_bot


@collection_edit_router.callback_query(F.data == "edit_pair",
                                       StateFilter(BotStates.collection_editing))
async def edit_pair_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    #TODO: вызывает сценарий 02_02_2_pair_edit_handlers
    # присылает первый элемент редактируемой карточки и приглашает ее изменить, прикреплена инлайн клавиатура с кнопкой 'оставить без изменений'
    # также нужно прислать обычную клавиатуру с кнопкой отмены реждактирования пары
    await callback_data.answer(text="Редактировать пару 🟢")
    data = await state.get_data()
    cur_coll_id = data["cur_coll_id"]
    cur_card_id = data["spec_cards_pag_inst"].cur_card_id

    # cur_card
    # await cart_flipper_bot.send_message(chat_id=callback_data.from_user.id,
    #                                     text="",
    #                                     reply_markup=)

    await state.set_state(BotStates.pair_editing_change_first_elem)
    pass
