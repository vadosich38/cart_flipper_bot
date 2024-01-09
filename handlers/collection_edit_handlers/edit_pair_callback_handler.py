#TODO: Кнопка “Изменить” позволяет изменить выбранную пару
# вызывает сценарий pair_edit_handlers
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


#TODO: заполнить фильтр
@collection_edit_router.callback_query(F.data == "",
                                       StateFilter(BotStates.collection_editing))
async def edit_pair_callback(callback_data: CallbackQuery, state: FSMContext) -> None:
    #TODO: вызывает сценарий pair_edit_handlers
    # присылает первый элемент редактируемой карточки и приглашает ее изменить, прикреплена инлайн клавиатура с кнопкой 'оставить без изменений'
    # также нужно прислать обычную клавиатуру с кнопкой отмены реждактирования пары
    await callback_data.answer(text="Редактировать пару 🟢")
    await state.set_state(BotStates.pair_editing_change_first_elem)
    pass
