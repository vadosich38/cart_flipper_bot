# Кнопка “Изменить” позволяет изменить выбранную пару
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

from DBPackage.DBclass import DBMethods
from bot_set.bot_states import BotStates
from .collection_edit_router import collection_edit_router
from keyboards.pair_edit_keyboard import get_pair_edit_kb
from bot_set.data_formats_handlers import send_card_element


@collection_edit_router.callback_query(F.data == "edit_pair",
                                       StateFilter(BotStates.collection_editing))
async def edit_pair_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    #вызывает сценарий 02_02_2_pair_edit_handlers
    #присылает первый элемент редактируемой карточки и приглашает ее изменить, прикреплена инлайн клавиатура
    # с кнопками 'оставить без изменений' и "отменить редактирование пары"
    await callback_data.answer(text="Редактировать пару 🟢")
    data = await state.get_data()
    # из инстанса класса получаем айди текущей карточки
    cur_card_id = data["spec_coll_pag_inst"].cur_card_id
    #TODO: вместо этого метода можно в пагинатор добавить метод "получить текущую карточку повторно"
    cur_card = DBMethods.get_card_by_id(card_id=cur_card_id)

    send_card_element(user_id=callback_data.from_user.id,
                      card_value=cur_card[1],
                      card_value_type=cur_card[2],
                      keyboard=get_pair_edit_kb())

    await state.set_state(BotStates.pair_editing_change_first_elem)
